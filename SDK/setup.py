# 这里使用pyz作为打包文件，采用zip算法
import os
import zipfile

from Profiles import *


def init():
    if os.path.isfile(command.__command_pyz_name__):
        _ = input(r"构建文件已存在，是否替换？[y\n]")
        if _.lower() != "y":
            exit(0)
    main_file_name = f"mod_{Information.__developers__}_{Information.__version__}_{Information.__mod_name__}"

    with open("setup-temp", 'w') as file:
        file.write(main_file_name)

    return main_file_name


def create_pyz(source_dir, output_file, main_file_name):

    os.rename('main.py', main_file_name+".py")
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zf.write(file_path, arcname)
                print("\t写入: {}".format(file_path))

    os.rename(main_file_name+".py", 'main.py')


if __name__ == '__main__':
    print("开始构建:")

    source_directory = '.'

    create_pyz(source_directory, command.__command_pyz_name__, init())

    print(f'构建完成')
