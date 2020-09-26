# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from fw_pcr.main import MyMainWindow


def load_data(sp):
    for i in range(1, 11):              #模拟主程序加载过程
        time.sleep(0.3)                   # 加载数据
        sp.showMessage("加载... {0}%".format(i * 10), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
        QtWidgets.qApp.processEvents()  # 允许主进程处理事件

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap(r"C:\Users\61980\Desktop\FW_PCR\resources\imgs\20_bg-02.png"))
    # splash.resize(QtCore.QSize(800, 600))
    splash.setGeometry(QtCore.QRect(400, 300, 800, 600))
    splash.showMessage("加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()                           # 显示启动界面
    load_data(splash)
    QtWidgets.qApp.processEvents()          # 处理主进程事件
                  # 加载数据

    my_window = MyMainWindow()
    my_window.show()
    splash.finish(my_window)                   # 隐藏启动界面
    sys.exit(app.exec_())