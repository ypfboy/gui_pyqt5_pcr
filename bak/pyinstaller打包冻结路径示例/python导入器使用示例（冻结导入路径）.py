import os
import sys
"""
sys.meta_path使用示例
"""

class SourceImporter:
    # 导入器，
    def __init__(self, dir):
        self.module_names = {"FW_PCR",}
        for name in os.listdir(dir):
            self.module_names.add(name)

    def find_spec(self, fullname, path, target=None):
        print(fullname, path, target)
        if fullname.split(".")[0] in self.module_names:
            print("11111111111111111111  : " + fullname + "    " + str(path))
            return sys.meta_path[1].find_spec(fullname, path, target)
        else:
            return None


source_dir= os.path.join(r"C:\Users\61980\Desktop\aa\pcr", 'FW_PCR')
sys.path.insert(0, source_dir)
sys.meta_path.insert(0, SourceImporter(source_dir))
# Import
import FW_PCR