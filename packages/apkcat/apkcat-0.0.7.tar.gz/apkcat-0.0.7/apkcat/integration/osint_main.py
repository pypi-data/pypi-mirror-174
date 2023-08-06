from apkcat.integration.bazaar import bazaar_query
from apkcat.integration.triage import query_sample_id


def get_sample_id_wf(filename):
    with open(filename, "r") as f:
        for line in f.readlines():
            hash = line.rstrip()
            print(query_sample_id(hash))


if __name__ == "__main__":
    # Query the all hash value from bazaar and turn them into Triage Sample ID
    # tag_name = "irata"
    #
    # for hash_value in bazaar_query(tag_name, "tag"):
    #     print(hash_value)
    #     print(query_sample_id(hash_value))
    pass
