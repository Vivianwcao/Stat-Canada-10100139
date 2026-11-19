import duckdb
from datetime import datetime, timedelta, date
import requests
import json
import pyarrow as pa
import pyarrow.parquet as pq

pid = 10100139
silver_dir = "./data/silver"
SCHEMA = pa.schema(
    [
        ("ref_date", pa.date32()),
        ("geo", pa.string()),
        ("Financial market statistics", pa.string()),
        ("value", pa.float64()),
        ("vector", pa.int64()),
    ]
)
vector_mapper = {
    39052: "Government of Canada benchmark bond yields, 3 year",
    39053: "Government of Canada benchmark bond yields, 5 year",
    39079: "Target rate",
}


def get_latest_date():
    con = duckdb.connect()
    return con.execute(f"""
        select ref_date
        from './data/silver/{pid}*.parquet'
        order by ref_date desc
        limit 1;
    """).fetchone()[0]


def request_updates():
    url = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange"
    start_date = get_latest_date() + timedelta(1)
    end_date = date.today()
    params = {
        "vectorIds": "39052,39053,39079",
        "startRefPeriod": start_date.strftime("%Y-%m-%d"),
        "endReferencePeriod": end_date.strftime("%Y-%m-%d"),
    }
    res = requests.get(url, params=params)
    # Raise an exception if HTTP error
    res.raise_for_status()
    # Convert JSON response into Python object
    data = res.json()
    with open("data/silver/output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data


def create_parquet(data):
    rows = []
    for vector in data:
        if vector.get("status") != "SUCCESS":
            continue
        obj = vector.get("object", {})
        if obj.get("productId") != pid:
            print("wrong table fetched.")
            break
        vector_id = obj.get("vectorId")
        for x in obj.get("vectorDataPoint", []):
            value = x.get("value")
            if value is None:
                continue
            rows.append(
                {
                    "ref_date": datetime.strptime(x["refPer"], "%Y-%m-%d"),
                    "geo": "Canada",
                    "Financial market statistics": vector_mapper.get(vector_id),
                    "value": float(value),
                    "vector": vector_id,
                }
            )
    if rows:
        table = pa.Table.from_pylist(rows, schema=SCHEMA)
        ingestion_date = date.today().strftime("%Y%m%d")
        pq.write_table(table, f"data/silver/{pid}_{ingestion_date}.parquet")


if __name__ == "__main__":
    data = request_updates()
    create_parquet(data)
