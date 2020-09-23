# -*- coding: utf-8 -*-
import os
import pandas as pd
from hdfs3 import HDFileSystem


class HdfsHelper:
    def __init__(self, host=None, port=None):
        self.hdfs = HDFileSystem(host=host, port=port)

    def chmod(self, file_path, filename, mode=0o777):
        self.hdfs.chmod("{0}/{1}".format(file_path, filename), mode)

    def chown(self, file_path, filename, owner, group):
        self.hdfs.chown("{0}/{1}".format(file_path, filename), owner, group)

    # 这个方法常用 hdfs上的文件树可以与当前的一样
    def put_file(self, file_path, filename):
        self.hdfs.put("{0}/{1}".format(file_path, filename), "/{0}".format(filename))

    def get_file(self, file_path, filename):
        self.hdfs.get("{0}/{1}".format(file_path, filename), "/{0}".format(filename))

    def read_file(self, file_path, filename):
        with self.hdfs.open("{0}/{1}".format(file_path, filename)) as f:
            bytes = f.read()
        return bytes

    def get_dataframe_by_file(self, file_path, filename, encoding="utf8", skiprows=0, nrows=0, key="table"):
        ext = os.path.splitext(filename)[1].lower()
        with self.hdfs.open("{0}/{1}".format(file_path, filename)) as f:
            if ext == '.csv':
                try:
                    df = pd.read_csv(f, encoding=encoding, skiprows=skiprows, nrows=nrows)
                except UnicodeDecodeError:
                    df = pd.read_csv(f, encoding='gb18030', skiprows=skiprows, nrows=nrows)
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(f, skiprows=skiprows, nrows=nrows)
            elif ext in ['.h5']:
                try:
                    df = pd.read_hdf(f, key=key)
                except KeyError:
                    df = pd.DataFrame()
            else:
                raise Exception('not supported yet')
        return df
