import os.path
import re
import sys

from androguard.core import androconf
from androguard.misc import AnalyzeAPK, AnalyzeDex

EXCLUDE_PACKAGE = {
    "Landroid/support/v4/",
    "Landroidx/",
    "Lokhttp3/",
    "Lokio/",
    "Lcom/facebook/",
    "Lcom/dropbox/",
    "Lcom/airbnb/lottie/",
}


def exclude_package(method_name):
    for exclude_p in EXCLUDE_PACKAGE:
        if exclude_p in str(method_name):
            return True
    return False


def check_is_apk(file_path):
    """
    Check the given file_path is APK or not
    :param file_path:
    :return: Ture or False
    """
    result = androconf.is_android(file_path)
    return result == "APK"


def check_is_dex(file_path):
    """
    Check the given file_path is DEX or not
    :param file_path:
    :return: Ture or False
    """
    result = androconf.is_android(file_path)
    return result == "DEX"


class APKinfo:
    def __init__(self, filepath):
        self._filepath = filepath
        self._filename = os.path.basename(filepath)

        if check_is_apk(filepath):
            self.apk, self.dvm, self.analysis = AnalyzeAPK(filepath)
        else:
            print("APK file required")

    def __repr__(self):
        return f"<Apkinfo-APK:{self.filename}>"

    @property
    def filename(self):
        """
        Return the filename of the APK.
        :return:
        """
        return self._filename

    @property
    def filesize(self, bsize=1024, unit="mb"):
        """
        Return the file size from the given file
        :return:  string of file size with preferred unit (default mb) e.g. '2.13 mb'
        """
        size_unit = {"kb": 1, "mb": 2, "gb": 3, "tb": 4, "pb": 5, "eb": 6}
        file_size = os.path.getsize(self._filepath)
        if file_size < bsize:
            re_unit = size_unit[unit] - 1
            reversed_unit = {1: "kb", 2: "mb", 3: "gb", 4: "tb", 5: "pb", 6: "eb"}
            return f"{round(file_size, 2)} {reversed_unit[re_unit]}"
        result = float(file_size)
        try:
            result /= bsize ** size_unit[unit]
            return f"{round(result, 2)} {unit}"
        except ZeroDivisionError as error:
            print(error)
            sys.exit(0)

    @property
    def permissions(self):
        pattern = re.compile("^android\.permission\.[\w]+$")
        permission = self.apk.get_permissions()
        return [item for item in permission if pattern.match(item)]

    @property
    def android_apis(self):
        """
        Return all Android native APIs from given APK.
        :return: a set of all Android native APIs MethodAnalysis
        """
        apis = set()

        for external_cls in self.analysis.get_external_classes():
            for meth_analysis in external_cls.get_methods():
                if meth_analysis.is_android_api():
                    apis.add(meth_analysis)

        return apis

    @property
    def external_methods(self):
        """
        Return all external methods from given APK.
        :return: a set of all external methods MethodAnalysis
        """
        return {
            meth_analysis
            for meth_analysis in self.analysis.get_methods()
            if not meth_analysis.is_external()
        }

    def get_strings(self):

        result = set()
        for string_analysis in self.analysis.get_strings():
            for cls_analysis in string_analysis.get_xref_from():
                class_md, dvm_md = cls_analysis
                if not exclude_package(class_md.name):
                    result.add(string_analysis.get_orig_value())

        return result

    def get_activities(self):
        return self.apk.get_activities()


class DEXinfo:
    def __init__(self, filepath):
        self._filepath = filepath
        self._filename = os.path.basename(filepath)

        if check_is_dex(filepath):
            _, _, self.analysis = AnalyzeDex(filepath)
        else:
            print("DEX file required")

    def __repr__(self):
        return f"<DEXinfo-DEX:{self.filename}>"

    @property
    def filename(self):
        """
        Return the filename of the DEX.
        :return:
        """
        return self._filename

    @property
    def filesize(self, bsize=1024, unit="mb"):
        """
        Return the file size from the given file
        :return:  string of file size with preferred unit (default mb) e.g. '2.13 mb'
        """
        size_unit = {"kb": 1, "mb": 2, "gb": 3, "tb": 4, "pb": 5, "eb": 6}
        file_size = os.path.getsize(self._filepath)
        if file_size < bsize:
            re_unit = size_unit[unit] - 1
            reversed_unit = {1: "kb", 2: "mb", 3: "gb", 4: "tb", 5: "pb", 6: "eb"}
            return f"{round(file_size, 2)} {reversed_unit[re_unit]}"
        result = float(file_size)
        try:
            result /= bsize ** size_unit[unit]
            return f"{round(result, 2)} {unit}"
        except ZeroDivisionError as error:
            print(error)
            sys.exit(0)

    @property
    def android_apis(self):
        """
        Return all Android native APIs from given DEX.
        :return: a set of all Android native APIs MethodAnalysis
        """
        apis = set()

        for external_cls in self.analysis.get_external_classes():
            for meth_analysis in external_cls.get_methods():
                if meth_analysis.is_android_api():
                    apis.add(meth_analysis)

        return apis

    @property
    def external_methods(self):
        """
        Return all external methods from given DEX.
        :return: a set of all external methods MethodAnalysis
        """
        return {
            meth_analysis
            for meth_analysis in self.analysis.get_methods()
            if not meth_analysis.is_external()
        }

    def get_strings(self):
        """
        Return all strings from given DEX
        :return: a set of all strings
        """

        result = set()
        for string_analysis in self.analysis.get_strings():
            for cls_analysis in string_analysis.get_xref_from():
                class_md, dvm_md = cls_analysis
                if not exclude_package(class_md.name):
                    result.add(string_analysis.get_orig_value())

        return result


if __name__ == "__main__":
    pass
