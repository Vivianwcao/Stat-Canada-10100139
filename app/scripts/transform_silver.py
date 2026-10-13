import csv
from re import L
import duckdb
import glob

pid = 10100139
vector_ids = [39052, 39053, 39079]
bronze_dir = "./data/bronze"
silver_dir = "./data/silver"


def transform_initial_bulk_parquet():
    vectors = ",".join(f"'v{id}'" for id in vector_ids)
    with duckdb.connect() as con:
        con.execute(f"""
        copy(
            select
                ref_date,
                geo,
                "Financial market statistics",
                VALUE,
                vector
            from read_csv('{bronze_dir}/{pid}.csv')
            where vector in ({vectors})
        )
        to '{silver_dir}/*.parquet'
        (format parquet)
        """)


def run_silver_ingestion():
    parquet_file = glob.glob(f"{silver_dir}/**/*.parquet", recursive=True)
    if not parquet_file:
        transform_initial_bulk_parquet()


if __name__ == "__main__":
    run_silver_ingestion()
