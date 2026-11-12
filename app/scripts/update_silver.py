import duckdb


pid = 10100139
silver_dir = "./data/silver"


def get_latest_date():
    con = duckdb.connect()
    res = con.execute(f"""
        select ref_date
        from './data/silver/{pid}.parquet'
        order by ref_date desc
        limit 1;
    """).fetchone()[0]

    print(res)


if __name__ == "__main__":
    get_latest_date()
