import requests
import json
import zipfile
import glob
import io

pid = 10100139
bronze_dir = "./data/bronze"
md_url = "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata"
payload = [{"productId": pid}]
csv_url = f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en"


def get_csv_bulk():
    # get csvs in bulk (zip) - returns 2 csvs (entire table csv + metaData csv)
    res_csv = requests.get(csv_url)
    res_csv.raise_for_status()

    data = res_csv.json()
    zip_url = data.get("object")

    if object:
        res_zip = requests.get(zip_url)
        res_zip.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(res_zip.content)) as z:
            z.extractall(bronze_dir)


def run_bronze_ingestion():
    csv_file = glob.glob(f"{bronze_dir}/**/*.csv", recursive=True)
    if not csv_file:
        get_csv_bulk()


if __name__ == "__main__":
    run_bronze_ingestion()
