import duckdb
from datetime import timedelta, date
import requests

pid = 10100139
silver_dir = "./data/silver"


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
    return data


if __name__ == "__main__":
    print(request_updates())
