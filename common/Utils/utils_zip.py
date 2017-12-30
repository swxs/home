# encoding:utf-8

import zipfile, os, shutil


def unzip(zip_file_name, dest_dir='.'):
    """服务器端解压文件生成r_list.dat文件"""
    zf = zipfile.ZipFile(zip_file_name, 'r')
    dest_dir = dest_dir.replace('\\', '/')
    if dest_dir.endswith('/'):
        dest_dir = dest_dir[:-1]
    for filename in zf.namelist():
        fname = filename
        new_file = u'%s/%s' % (dest_dir, fname)
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


def makeArchive(fileList, archive, exclude_parent=None):
    """
    'fileList' is a list of file names - full path each name
    'archive' is the file name for the archive with a full path
    """
    if exclude_parent:
        exclude_parent = exclude_parent.replace('\\', '/')
    try:
        a = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)
        for f in fileList:
            # print "archiving file %s" % (f)
            if exclude_parent:
                newf = f.replace('\\', '/')
                arcname = newf.replace(exclude_parent, '')
                a.write(f, arcname=arcname)
            else:
                a.write(f)
        a.close()
        return True
    except Exception, ex:
        # print ex
        return False


def dirEntries(dir_name, subdir, *args):
    '''Return a list of file names found in directory 'dir_name'
    If 'subdir' is True, recursively access subdirectories under 'dir_name'.
    Additional arguments, if any, are file extensions to match filenames. Matched
        file names are added to the list.
    If there are no additional arguments, all files found in the directory are
        added to the list.
    Example usage: fileList = dirEntries(r'H:\TEMP', False, 'txt', 'py')
        Only files with 'txt' and 'py' extensions will be added to the list.
    Example usage: fileList = dirEntries(r'H:\TEMP', True)
        All files and all the files in subdirectories under H:\TEMP will be added
        to the list.
    '''
    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            if not args:
                fileList.append(dirfile)
            else:
                if os.path.splitext(dirfile)[1][1:] in args:
                    fileList.append(dirfile)
        # recursively access file names in subdirectories
        elif os.path.isdir(dirfile) and subdir:
            # print "Accessing directory:", dirfile
            fileList.extend(dirEntries(dirfile, subdir, *args))
    return fileList


def make_zip(zip_file_name, file_list, exclude_parent=None, define_parent=None):
    """
    'fileList' is a list of file names - full path each name
    'archive' is the file name for the archive with a full path
    """
    if exclude_parent:
        exclude_parent = exclude_parent.replace('\\', '/')
    if define_parent:
        define_parent = define_parent.replace('\\', '/')
    try:
        a = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        for f in file_list:
            # print "archiving file %s" % (f)
            if exclude_parent:
                newf = f.replace('\\', '/')
                if newf.find('Read me') != -1:
                    arcname = newf.replace(define_parent, '')
                else:
                    arcname = newf.replace(exclude_parent, '')
                a.write(f, arcname=arcname)
            else:
                a.write(f)
        a.close()
        return True
    except Exception, ex:
        # print ex
        return False


def copy_tree(src_dir, dst_dir):
    # android上调用distutils.dir_util.copy_tree会报错：Operation not permitted
    # 这里重新实现
    # 先备份,再覆盖
    src_dir = src_dir.replace('\\', '/')
    dst_dir = dst_dir.replace('\\', '/')
    if src_dir.endswith('/'):
        src_dir = src_dir[:-1]
    if dst_dir.endswith('/'):
        dst_dir = dst_dir[:-1]
    for root, dirs, files in os.walk(src_dir):
        for filename in files:
            fpath = root[len(src_dir) + 1:]
            new_file = '%s/%s/%s' % (dst_dir, fpath, filename)
            new_file_path = os.path.dirname(new_file)
            if not os.path.exists(new_file_path):
                os.makedirs(new_file_path)
            src_file = '%s/%s' % (root, filename)
            shutil.copyfile(src_file, new_file)


import StringIO


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


def zip_folder(folder, zipname, exclude_parent=None):
    makeArchive(dirEntries(folder, True), zipname, exclude_parent)


if __name__ == '__main__':
    folder1 = r'e:\HG\iSurveylink_A\file\attach\40'
    zipname1 = 'test.zip'
    zip_folder(folder1, zipname1, exclude_parent=r"""e:\HG\iSurveylink_A\file\attach""")
