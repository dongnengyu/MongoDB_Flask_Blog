import os
import sys
import hashlib

_FILE_SLIM = (100 * 1024 * 1024)  # 100MB


def file_md5(filename):
    calltimes = 0
    hmd5 = hashlib.md5()
    fp = open(filename, "rb")
    f_size = os.stat(filename).st_size
    if f_size > _FILE_SLIM:
        while (f_size > _FILE_SLIM):
            hmd5.update(fp.read(_FILE_SLIM))
            f_size /= _FILE_SLIM
            calltimes += 1  # delete
        if (f_size > 0) and (f_size <= _FILE_SLIM):
            hmd5.update(fp.read())
    else:
        hmd5.update(fp.read())

    return (hmd5.hexdigest(), calltimes)


if __name__ == '__main__':
    filepath = "/Users/xiaomu/Desktop/women_clothing_detalis.json"
    (hvalue, ctimes) = file_md5(filepath)
    print(hvalue)
