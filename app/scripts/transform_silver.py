import csv
from re import L
import duckdb
import glob
from datetime import date

pid = 10100139
vector_ids = [39052, 39053, 39079]
bronze_dir = "data/bronze"
silver_dir = "data/silver/"


def transform_initial_bulk_parquet():
    ingestion_time = date.today().strftime("%Y%m%d")
    vectors = ",".join(f"'v{id}'" for id in vector_ids)
    with duckdb.connect() as con:
        con.execute(f"""
        copy(
            select
                ref_date::date ref_date,
                geo,
                "Financial market statistics",
                VALUE::numeric(10, 2) value,
                substring(vector, 2)::integer vector
            from read_csv('{bronze_dir}/{pid}.csv')
            where vector in ({vectors})
            and value is not null
        )
        to '{silver_dir}/{pid}_{ingestion_time}.parquet'
        (format parquet)
        """)


def run_silver_ingestion():
    parquet_file = glob.glob(f"{silver_dir}/**/{pid}.parquet", recursive=True)
    if not parquet_file:
        transform_initial_bulk_parquet()


if __name__ == "__main__":
    run_silver_ingestion()
