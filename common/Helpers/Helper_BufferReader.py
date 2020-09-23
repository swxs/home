from requests_toolbelt import MultipartEncoder


class CancelledError(Exception):
    """
    用户取消文件上传
    """

    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)

    def __str__(self):
        return self.msg

    __repr__ = __str__


class BufferReader(MultipartEncoder):
    """
    将multipart-formdata转化为stream形式的Proxy类
    """

    def __init__(self, fields, boundary=None, callback=None, cb_args=(), cb_kwargs=None):
        self._callback = callback
        self._progress = 0
        self._cb_args = cb_args
        self._cb_kwargs = cb_kwargs or {}
        super(BufferReader, self).__init__(fields, boundary)

    def read(self, size=None):
        chunk = super(BufferReader, self).read(size)
        self._progress += int(len(chunk))
        self._cb_kwargs.update({'size': self._len, 'progress': self._progress})
        if self._callback:
            try:
                self._callback(*self._cb_args, **self._cb_kwargs)
            except Exception:  # catches exception from the callback
                raise CancelledError('The upload was cancelled.')
        return chunk
