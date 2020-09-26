# -*- coding:utf8 -*-

import sys,time

from PyQt5 import QtWidgets, QtCore
from fw_pcr.main import MyMainWindow
from views.uiStartFace import Ui_StartFace



class StartFace(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StartFace, self).__init__(parent)
        # 禁用关闭按钮
        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        # 只显示关闭
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 隐藏整个头部
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.add = Ui_StartFace()
        # qr = self.frameGeometry()
        # qt = QtWidgets.QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(qt)
        self.add.setupUi(self)

        self.sty_str = "border-image: url(:/newPrefix/imgs/18_gene1.png);"
        self.sty_str2 = "border-image: url(:/newPrefix/imgs/19_gene2.png);"


    def load_start_face(self):
        for i in range(5):
            time.sleep(0.25)
            eval("self.add." + "show_%s"%i + ".setStyleSheet(self.sty_str)")
            time.sleep(0.25)
            # 界面刷新
            QtWidgets.QApplication.processEvents()

    def finsh(self, main_window):
        self.load_start_face()
        self.close()
        main_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    start_face = StartFace()
    start_face.show()
    app.processEvents()
    window = MyMainWindow()
    start_face.finsh(window)
    sys.exit(app.exec_())
