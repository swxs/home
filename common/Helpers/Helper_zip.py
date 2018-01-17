# encoding:utf-8

import zipfile
import os
import shutil
import StringIO
import datetime

import settings
from common.Helpers.Helper_folder import get_path_split


class ZipHelper(object):
    @classmethod
    def _get_arcname(cls, old_arcname, new_arcname):
        if old_arcname is not None:
            return os.path.join(old_arcname, new_arcname)
        else:
            return new_arcname

    @classmethod
    def zip(cls, src, dest, arcname=None):
        if os.path.isdir(src):
            for root, filepath_list, filename_list in os.walk(src):
                for filepath in filepath_list:
                    ZipHelper.zip(src=os.path.join(root, filepath),
                                  dest=dest,
                                  arcname=ZipHelper._get_arcname(arcname, filepath))
                for filename in filename_list:
                    with zipfile.ZipFile(dest, 'a', zipfile.ZIP_DEFLATED) as zf:
                        zf.write(os.path.join(root, filename),
                                 arcname=ZipHelper._get_arcname(arcname, filename))
                break
        elif os.path.isfile(src):
            filepath, filename = os.path.split(src)
            with zipfile.ZipFile(dest, 'a', zipfile.ZIP_DEFLATED) as zf:
                zf.write(src, arcname=ZipHelper._get_arcname(arcname, filename))

    @classmethod
    def zip_file(cls, file, zipname=None, exclude_parent=False):
        if not os.path.isfile(file):
            return False

        folder, filename = os.path.split(file)

        if exclude_parent:
            base_path, pathname = get_path_split(folder)
            if zipname is None:
                zipname = os.path.join(base_path, "{0}.zip".format(pathname))
            ZipHelper.zip(file, zipname, arcname=None)
        else:
            filename_base, filename_ext = os.path.splitext(filename)
            if zipname is None:
                zipname = os.path.join(folder, "{0}.zip".format(filename_base))
            ZipHelper.zip(file, zipname, arcname=None)
        return True

    @classmethod
    def zip_folder(cls, folder, zipname=None, exclude_parent=False):
        if not os.path.isdir(folder):
            return False

        base_path, pathname = get_path_split(folder)

        if zipname is None:
            zipname = os.path.join(base_path, "{0}.zip".format(pathname))

        if exclude_parent:
            ZipHelper.zip(folder, zipname, arcname=pathname)
        else:
            ZipHelper.zip(folder, zipname, arcname=None)
        return True


    @classmethod
    def unzip(cls, zipname, dest=None):
        """服务器端解压文件生成r_list.dat文件"""
        zf = zipfile.ZipFile(zipname, 'r')
        dest = dest.replace('\\', '/')
        if dest.endswith('/'):
            dest = dest[:-1]
        for filename in zf.namelist():
            fname = filename
            new_file = u'%s/%s' % (dest, fname)
            if new_file.endswith('/') or new_file.endswith('\\'):
                if not os.path.exists(new_file):
                    os.makedirs(new_file)
            else:
                filepath = os.path.split(new_file)[0]
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                try:
                    f = open(new_file, 'wb')
                except UnicodeEncodeError:
                    f = open(new_file.encode('utf8'), 'wb')
                f.write(zf.read(filename))
                f.close()


class InMemoryZip(object):
    """用法:
    imz = InMemoryZip()
    imz.append("test.txt", "Another test").append("test2.txt", "Still another")
    imz.writetofile("test.zip")
    """

    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = StringIO.StringIO()

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of
           file_contents to the in-memory zip.'''
        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def writetofile(self, filename):
        '''Writes the in-memory zip to a file.'''
        f = file(filename, "wb")
        f.write(self.read())
        f.close()


if __name__ == '__main__':
    src = os.path.join("C://", "Users", "user1", "Desktop", "user", "views.py")
    dest = os.path.join("C:", "Users", "user1", "Desktop", "user.zip")
    # ZipHelper.zip(src, dest)
    ZipHelper.zip_file(src, exclude_parent=False)
    # ZipHelper.zip_folder(src, exclude_parent=True)
