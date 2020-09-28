# -*- coding: utf-8 -*-
# @File    : Helper_ftps.py
# @AUTH    : swxs
# @Time    : 2018/6/29 11:40


import ssl
import socket
import logging
from ftplib import FTP_TLS


logger = logging.getLogger("Helper_ftps")


class FTPS(FTP_TLS):
    def __init__(
        self, host='', user='', passwd='', acct='', keyfile=None, certfile=None, context=None, timeout=60
    ):  # 这里做过修改
        FTP_TLS.__init__(self, host, user, passwd, acct, keyfile, certfile, context, timeout)

    def connect(self, host='', port=0, timeout=-999):
        """Connect to host.  Arguments are:
        - host: hostname to connect to (string, default previous host)
        - port: port to connect to (integer, default previous port)
        """
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout
        try:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)
            self.af = self.sock.family
            # !这里做过修改
            self.sock = ssl.wrap_socket(self.sock, self.keyfile, self.certfile, ssl_version=ssl.PROTOCOL_TLSv1)
            # !修改结束
            self.file = self.sock.makefile('rb')
            self.welcome = self.getresp()
        except Exception as e:
            logger.exception("ftp连接失败！")
        return self.welcome

    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        self.voidcmd('TYPE I')
        conn = self.transfercmd(cmd, rest)
        try:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                conn.sendall(buf)
                if callback:
                    callback(buf)
            # shutdown ssl layer
            if isinstance(conn, ssl.SSLSocket):
                # !这里做过修改
                pass
                # !修改结束
        finally:
            conn.close()
        return self.voidresp()
