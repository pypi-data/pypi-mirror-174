from apkcat.core import check_is_apk, check_is_dex, APKinfo, DEXinfo
from apkcat.integration.osint_main import get_sample_id_wf


def main(file_path, permission, activity, query):
    if check_is_apk(file_path) and permission:
        apk_analysis = APKinfo(file_path)
        for apk_permission in apk_analysis.permissions:
            print(apk_permission)
        return

    elif check_is_apk(file_path) and activity:
        apk_analysis = APKinfo(file_path)
        for act in apk_analysis.get_activities():
            print(act)

    elif check_is_apk(file_path):

        apk_analysis = APKinfo(file_path)

        for item in apk_analysis.get_strings():
            print(item)

    elif check_is_dex(file_path):
        dex_analysis = DEXinfo(file_path)

        for item in dex_analysis.get_strings():
            print(item)

    elif query:
        get_sample_id_wf(query)

    else:
        print("File Format is wrong")


if __name__ == "__main__":
    pass
