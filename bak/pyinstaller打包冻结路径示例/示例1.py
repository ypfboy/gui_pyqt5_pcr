import os
import sys
"""
sys.meta_path使用示例, 冻结路径使用的是这个类 <class '_frozen_importlib_external.PathFinder'>
"""
import os
import sys


class SourceImporter:

    def __init__(self, dir):
        self.module_names = {"pyzo"}
        for name in os.listdir(dir):
            self.module_names.add(name)

    def find_spec(self, fullname, path, target=None):
        # print(fullname)
        if fullname.split(".")[0] in self.module_names:
            # print("1111111111111111 : " + fullname)
            return sys.meta_path[-2].find_spec(fullname, path, target)
        else:
            return None


source_dir= os.path.join(r"C:\Users\61980\Desktop\aa\pcr", 'FW_PCR')
sys.path.insert(0, source_dir)
sys.meta_path.insert(0, SourceImporter(source_dir))
# Import
import FW_PCR
# FW_PCR.appss    ['C:\\Users\\61980\\Desktop\\aa\\pcr\\FW_PCR']
# for i in sys.meta_path:
#     print(i)
for i in sys.meta_path:
    print(i.__class__.__name__)
# print(dir(sys.meta_path[-2]))


""""
[<__main__.SourceImporter object at 0x000002A690F51948>,
 <class '_frozen_importlib.BuiltinImporter'>, 
 <class '_frozen_importlib.FrozenImporter'>, 
 <pyimod03_importers.FrozenImporter object at 0x000002A69053B088>, 
 <class '_frozen_importlib_external.PathFinder'>,
  <pkg_resources.extern.VendorImporter object at 0x000002A690DAE748>,
   <pkg_resources._vendor.six._SixMetaPathImporter object at 0x000002A690DE8D08>, 
   <six._SixMetaPathImporter object at 0x000002A69C490BC8>]
"""

"""
[<class '_frozen_importlib.BuiltinImporter'>, 
<class '_frozen_importlib.FrozenImporter'>,
 <class '_frozen_importlib_external.PathFinder'>]
"""