import webview
import os
import sys
import zipfile
import shutil


mods_name_list = list()
buttons = dict()


class Api(object):
    """
    一个 Pywebview API 接口
    """
    def __init__(self) -> None:
        pass

    def return_mod_name(self) -> list:
        return mods_name_list

    def click_button(self, button_name) -> any:
        return buttons[button_name]()


class Mods(object):
    """
    主代码类模块
    """
    def __init__(self):
        self.scan_mod_path = "mods/"
        self.scan_mods()

    def scan_mods(self):
        for mod_name in os.listdir(self.scan_mod_path):
            if os.path.isfile("mods/"+mod_name):
                print(mod_name)
                Mods.load_scan_mod(mod_name)

        print(buttons)

    @staticmethod
    def load_scan_mod(mod_name):
        path = 'mods/temp/{}'.format(list(os.path.splitext(mod_name))[0])
        sys.path.append(path)

        with zipfile.ZipFile('mods/'+mod_name, 'r') as zip_ref:
            zip_ref.extractall(path)
        with open(path+"/"+"setup-temp", "r") as f:
            _text = f.read()

        print(_text)
        main = __import__(_text)

        mod_button_name = main.__body_button_name__
        buttons[mod_button_name] = main.click_button
        mods_name_list.append(mod_button_name)

        del sys.path[sys.path.index(path)]
        print("导入{}，button name：{}".format(mod_name, mod_button_name))


def init() -> None:
    """
    :return: None
    初始化程序
    """
    shutil.rmtree("mods/temp", ignore_errors=True)
    for dir in ["logs", "mods/temp"]:
        os.makedirs(dir, exist_ok=True)
    Mods()


def main() -> None:
    """
    :return: None
    主程序入口
    """
    path = os.path.abspath('ui/main.html')
    api = Api()
    webview.create_window("window", path, js_api=api)
    webview.start(debug=False)


def on_exit() -> None:
    """
    :return: None
    当程序退出时清理缓存文件
    """
    shutil.rmtree("mods/temp", ignore_errors=True)

if __name__ == '__main__':
    init()
    main()
