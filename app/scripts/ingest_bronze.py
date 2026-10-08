import requests
import json
import zipfile
import io

pid = 10100139
vector_ids = (
    list(range(39050, 39058))
    + list(range(39059, 39069))
    + list(range(39070, 39075))
    + list(range(39076, 39080))
)
payload = [{"productId": pid}]
md_url = "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata"
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
            z.extractall("./data/bronze")


if __name__ == "__main__":
    get_csv_bulk()
