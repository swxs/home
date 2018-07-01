# -*- coding: utf-8 -*-

import unittest
from functools import cmp_to_key as _CmpToKey


class MyLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """

        def isTestMethod(attrname, testCaseClass=testCaseClass,
                         prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and \
                   callable(getattr(testCaseClass, attrname))

        testFnNames = list(filter(isTestMethod, dir(testCaseClass)))

        def ln(f):
            return getattr(testCaseClass, f).im_func.func_code.co_firstlineno

        if self.sortTestMethodsUsing:
            testFnNames.sort(key=_CmpToKey(lambda a, b: ln(a) - ln(b)))
        return testFnNames

"""
√1. 如何自动设置test运行顺序，不同文件按文件名，相同文件按行号

2. 如何动态切换mongodb

3. 如何测试/api/
main时运行mock的数据库
基于requests Cookie留存登录信息

4. 如何生成一部分测试代码
自动化
批量

5. 如何组织参数等信息
"""

if __name__ == "__main__":
    loader = MyLoader()
    # 构建测试用例集
    discover = loader.discover('./', pattern='*_tests.py')
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(discover)
