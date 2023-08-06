import requests

from apkcat.config import TRIAGE_TOKEN


def query_sample_id(hash_value):
    try:
        address = f"https://api.tria.ge/v0/search?query={hash_value}"
        headers = {"Authorization": f"Bearer {TRIAGE_TOKEN}"}
        triage_result = requests.get(address, headers=headers).json()

        return triage_result["data"][0]["id"]
    except KeyError as error:
        if "error" in triage_result and triage_result["error"] == "UNAUTHORIZED":
            print(triage_result["message"])
