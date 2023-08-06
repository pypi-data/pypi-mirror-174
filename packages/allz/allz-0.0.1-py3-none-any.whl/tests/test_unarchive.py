"""Tests for the decompress module."""
# Standard library imports
import os
import pathlib
from pathlib import Path

from allz.unarchive import Unarchive
# tar_bz_process imports
from allz.unarchive.tar_bz_process import TarBzProcess

# Current directory
HERE = pathlib.Path(__file__).resolve().parent


def test_tar_bz_process():
    """test unarchive command"""
    src_path = "./data/"
    dest_path = "/mnt/unarchive_dataset_tmp/A3D/unar_test/jumpcutter-master.tar.bz#"

    process = TarBzProcess()
    process.main(src_path, dest_path)
    assert Path.exists(Path(str(dest_path) + "/jumpcutter-master")) is True


def test_all_compress_type():
    dest_path_lst = []
    dest_file_name = 'jumpcutter.py'
    archive_dir = "/mnt/unarchive_dataset_tmp/A3D/compress"
    for archive_file in os.listdir(archive_dir):
        is_file = os.path.isfile(archive_dir + os.sep + archive_file)
        if is_file:
            src_path = "/".join([archive_dir, archive_file])
            dest_path = "/".join([archive_dir, archive_file + "#"])
            dest_path_lst.append(dest_path)
            Unarchive(src_path, dest_path)

    for dest_path in dest_path_lst:
        if os.path.exists(dest_path):
            if not os.path.exists(dest_path + "/jumpcutter-master/" + dest_file_name):
                print(str(dest_path) + f"路径下, 解压文件 {dest_file_name} 不存在")
        else:
            print(str(dest_path) + ", 路径不存在")


if __name__ == '__main__':
    test_tar_bz_process()
