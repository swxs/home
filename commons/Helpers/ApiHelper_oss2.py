import os
from urllib.parse import quote

import oss2


class Oss2Helper:
    def __init__(self, key_id=None, secret=None, host=None, bucket=None, root_dir='dev'):
        self.auth = oss2.Auth(key_id, secret)
        self.bucket = oss2.Bucket(self.auth, host, bucket)
        host = host.split('://', 1)[-1]
        self.host = f'https://{bucket}.{host}/'
        self.root = root_dir.strip('/')

    def _get_path(self, path):
        if path.startswith('/'):
            return f'{self.root}{path}'
        else:
            return f'{self.root}/{path}'

    def exists(self, path: str) -> bool:
        path = self._get_path(path)
        return self.bucket.object_exists(path)

    def get_file_meta(self, path: str):
        """
        获取文件元信息
        :param path:
        :return: head.last_modified, head.content_type, head.content_length

        head.last_modified: 文件最后修改时间戳，类型为int，可能是None
        head.content_type: 文件的MIME类型，可能是None
        head.content_length(bytes): Content-Length，可能是None
        """
        path = self._get_path(path)
        head = self.bucket.head_object(path)
        return head.last_modified, head.content_type, head.content_length

    def list_dir_files(self, path: str, max_keys=100) -> list:
        """
        获取目录下的所有文件
        """
        keys = []
        for obj in oss2.ObjectIterator(bucket=self.bucket, prefix=path, max_keys=max_keys):
            keys.append(obj.key)
        return keys

    def upload(self, path, data, mode: str = 'w'):
        """
        @params path: 上传路径
        @params data: 上传数据
        @params mode: 模式
        """
        path = self._get_path(path)
        if mode == 'a':
            result = self.bucket.head_object(path)
            self.bucket.append_object(path, result.content_length, data)
        elif mode == 'w':
            self.bucket.put_object(path, data)
        return True

    def download(self, path):
        """
        简介
        ----------
        下载文件

        参数
        ----------
        path :
            文件路径

        返回
        ----------

        """
        path = self._get_path(path)
        result = self.bucket.get_object(path)
        return result.read()

    def get_sign_download_path(self, path, filename, expires=3600):
        path = self._get_path(path)
        content_disposition_filename = quote(filename)
        params = {
            "response-content-disposition": f"attachment; filename*=utf-8''{content_disposition_filename}",
        }
        url = self.bucket.sign_url('GET', path, expires, slash_safe=True, headers=None, params=params)
        return url

    def delete(self, path):
        path = self._get_path(path)
        self.bucket.delete_object(path)
        return True

    def sync(self, src_path: str, dst_path: str, remove: bool = False) -> int:
        """
        简介
        ----------
        将本地文件同步到远程

        参数
        ----------
        src_path :

        dst_path :

        remove [可选]: 默认为 False


        返回
        ----------

        """
        total_length = os.path.getsize(src_path)
        part_size = oss2.determine_part_size(total_length, preferred_size=100 * 1024)

        upload_id = self.bucket.init_multipart_upload(dst_path).upload_id

        parts = []
        # 读取Excel文件并划分为多个部分进行上传
        with open(src_path, 'rb') as file:
            part_number = 1
            offset = 0
            while offset < total_length:
                num_to_upload = min(part_size, total_length - offset)

                result = self.bucket.upload_part(
                    dst_path, upload_id, part_number, oss2.SizedFileAdapter(file, num_to_upload)
                )
                parts.append(oss2.models.PartInfo(part_number, result.etag))

                offset += num_to_upload
                part_number += 1

        # 完成Multipart Upload任务
        self.bucket.complete_multipart_upload(dst_path, upload_id, parts)
        if remove:
            os.remove(src_path)
        return total_length
