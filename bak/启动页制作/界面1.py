# -*- coding:utf8 -*-

import sys,time

from PyQt5 import QtWidgets, QtGui
from fw_pcr.main import MyMainWindow


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__(QtGui.QPixmap(r"C:\Users\61980\Desktop\FW_PCR\resources\imgs\20_bg-02.png"))  #启动程序的图片

    #效果 fade =1 淡入   fade= 2  淡出，  t sleep 时间 毫秒
    def effect(self):
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() + 0.02     #设置淡入
            if newOpacity > 1:
                break

            self.setWindowOpacity(newOpacity)
            self.show()
            t -= 1
            time.sleep(0.04)

        time.sleep(1)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() - 0.02         #设置淡出
            if newOpacity < 0:
                break

            self.setWindowOpacity(newOpacity)
            t += 1
            time.sleep(0.04)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.effect()
    app.processEvents()   #＃设置启动画面不影响其他效果
    window = MyMainWindow()     #程序的主类
    window.show()
    splash.finish(window)      #启动画面完成启动
    sys.exit(app.exec_())
