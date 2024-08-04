import webview
import os
import sys
import zipfile
import shutil


mods_name_list = list()
buttons = dict()


class Api(object):

    def return_mod_name(self):
        return mods_name_list

    def click_button(self, button_name):
        buttons[button_name]()


class Mods(object):
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

        main = __import__("main")

        mod_button_name = main.__body_button_name__
        buttons[mod_button_name] = main.click_button
        mods_name_list.append(mod_button_name)

        print(sys.path)
        del sys.path[sys.path.index(path)]
        print("导入{}，button name：{}".format(mod_name, mod_button_name))
        print(sys.path)


def main():
    path = 'ui/main.html'
    api = Api()

    webview.create_window("window", path, js_api=api)

    webview.start(debug=False)


def init():
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    if not os.path.isdir("mods"):
        os.mkdir("mods")

    if os.path.isdir("mods/temp"):
        shutil.rmtree("mods/temp")
        os.mkdir("mods/temp")

    else:
        os.mkdir("mods/temp")

    Mods()


if __name__ == '__main__':
    init()
    main()
