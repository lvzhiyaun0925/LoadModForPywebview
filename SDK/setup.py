# 这里使用pyz作为打包文件，采用zip算法
import os
import zipfile

from Profiles import *


def create_pyz(source_dir, output_file):
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zf.write(file_path, arcname)
                print("\t写入: {}".format(file_path))


if __name__ == '__main__':
    print("开始构建:")

    source_directory = '.'

    create_pyz(source_directory, command.__command_pyz_name__)
    print(f'构建完成')

