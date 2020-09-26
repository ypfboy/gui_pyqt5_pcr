#coding=utf8
import os
import sys


# 所有外部模块在此导入，才可以冻结路径成功(在此导入是为了pyinstall可以将需要的模块收集完全)
# FW_PCR项目中不能使用pcr作为作为导入根路径， 否则pyinstaller会将所有模块全部打包， 冻结路径会失败，
# 项目中仍然使用FW_PCR作为， 然后在此处将所有第三方模块依次导入即可。
import matplotlib
import sqlite3
import xlsxwriter
import xmltodict

class SourceImporter:
    """导入器定义"""
    def __init__(self, dir):
        self.module_names = {"FW_PCR"}
        for name in os.listdir(dir):
            self.module_names.add(name)

    def find_spec(self, fullname, path, target=None):
        if fullname.split(".")[0] in self.module_names:
            li = [i for i in sys.meta_path if i.__class__.__name__ == "type"]
            return li[2].find_spec(fullname, path, target)
        else:
            return None

if getattr(sys, "frozen", False):
    source_dir= os.path.join(sys._MEIPASS, 'source/FW_PCR')
    sys.path.insert(0, source_dir)
    sys.meta_path.insert(0, SourceImporter(source_dir))
    from FW_PCR.fw_pcr import start

else:
    try:
        from FW_PCR.fw_pcr import start
    except ImportError:
        thisDir = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], "FW_PCR")
        sys.path.insert(0, thisDir)
        try:
             from fw_pcr import start
        except ImportError:
            raise ImportError('can not import FW_PCR')

def main():
    start.pcr_start()

if __name__ == '__main__':
    main()