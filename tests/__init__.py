# -*- coding: utf-8 -*-


import os
import sys
import datetime
import unittest
import functools
from mongoengine.connection import connect


class MyLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass"""

        def isTestMethod(attrname, testCaseClass=testCaseClass, prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and callable(getattr(testCaseClass, attrname))

        testFnNames = list(filter(isTestMethod, dir(testCaseClass)))

        def ln(f):
            return getattr(testCaseClass, f).__code__.co_firstlineno

        def ln_cmp(a, b):
            return (ln(a) > ln(b)) - (ln(a) < ln(b))

        if self.sortTestMethodsUsing:
            testFnNames.sort(key=functools.cmp_to_key(ln_cmp))
        return testFnNames


def report_to_shell(suite):
    runner = unittest.TextTestRunner()

    # 执行测试
    runner.run(suite)


def report_to_html(suite):
    import HTMLTestRunner

    now = datetime.datetime.now()
    path = ""
    report_file = os.path.join(path, f"{now:%Y_%m_%d_%H_%M_%S}_report.html")

    # 执行测试
    with open(report_file, "wb") as report:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report, title=f"{now}_report")
        runner.run(suite)


REPORT_TARGET_DICT = {"html": report_to_html, "shell": report_to_shell}


def run_tests(target="shell"):
    # 定义测试集合
    suite = unittest.TestSuite()

    # 构建测试用例集
    loader = MyLoader()
    all_case = loader.discover('./', pattern='*_tests.py')
    for case in all_case:
        # 循环添加case到测试集合里面
        suite.addTests(case)

    try:
        REPORT_TARGET_DICT[target](suite)
    except Exception as e:
        print(f"{target} is failed!")
        REPORT_TARGET_DICT["shell"](suite)


def main(target):
    run_tests(target)


if __name__ == "__main__":
    main(target="shell")
