import requests
from jq import jq


def bazaar_query(tag_name, type="tag", timeout=15):
    """
    Returns a list of SHA256 values for the given tag name from bazaar's query API
    """

    query_info = {
        "tag": {
            "query": "get_taginfo",
            "tag": "" + tag_name + "",
        },
        "sig": {
            "query": "get_siginfo",
            "signature": tag_name,
        },
    }

    response = requests.post(
        "https://mb-api.abuse.ch/api/v1/", data=query_info[type], timeout=timeout
    )
    json_response = response.content.decode("utf-8", "ignore")
    query = ".data[]." + "sha256_hash"

    json_response = jq(query).transform(text=json_response, text_output=True)

    return json_response.replace('"', "").split("\n")
