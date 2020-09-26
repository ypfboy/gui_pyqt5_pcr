import numpy as np
import sys
import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QTimer
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class App(QWidget):
    def __init__(self, parent=None):
        # 父类初始化方法
        super(App, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('动态演示')
        self.setWindowIcon(QIcon('电力图标.jpg'))
        self.setWindowIcon(QIcon('2345_image_file_copy_1.jpg'))
        self.setFixedSize(1200, 700)
        self.setMinimumSize(1200, 700)
        self.setMaximumSize(1200, 700)
        # 几个QWidgets

        self.startBtn1 = QPushButton('开始1')
        self.startBtn2 = QPushButton('开始2')
        self.endBtn = QPushButton('结束')
        self.clearBtn = QPushButton('清除')
        self.startBtn1.clicked.connect(self.startTimer)
        self.startBtn2.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
        self.clearBtn.clicked.connect(self.clear_axes)
        # 时间模块
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        # 图像模块
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        # 垂直布局

        layout = QVBoxLayout()
        layout.addWidget(self.startBtn1)
        layout.addWidget(self.startBtn2)
        layout.addWidget(self.endBtn)
        layout.addWidget(self.clearBtn)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        #
        # self.ax = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.ax = plt.subplot(1, 1, 1)
        # 数组初始化

        self.init_data()

    def init_data(self):
        self.x = []
        self.index = 0  # 列表索引
        a1 = "-2761.28	-380.3101	744.9255	479.52045	786.4591	1237.476	1025.6022	117.36899	802.9483	429.69952	-295.84616	160.79567	-736.5781	-671.28	-267.2632	-469.4339	-414.10455	104.88101	268.72595	970.08655	3609.4626	8884.698	19172.918	38912.668	75271.17	130198.45	194587.67	255300.55	302161.56	337904.84	366042.3	389242.16	409106.75	427707.66	442510.38	454943.22	467397.38	476516.9	486813.94	493995.22	501359.62	510118.1	516560.12	523697.53	530468.8"
        a2 = "-6973.3677	-3470.593	-1596.975	-1277.8881	-482.23868	-935.74554	-588.3149	354.86572	-755.8911	-356.55426	78.37637	425.932	453.6439	32.94952	-144.5261	-131.50172	623.02264	-97.3592	-289.80356	-193.15419	-105.97356	-236.48042	-205.36229	-151.9629	169.46771	-765.5704	-1126.3273	-943.3341	-359.341	-1154.3479	-274.636	-626.73663	-674.1497	-910.43787	-2111.101	-2213.9517	-1742.8647	-1529.1841	-2666.9097	-3045.2603	-3673.1108	-3131.274	-3283.2185	-3152.9128	-4065.3572"
        a3 = "-10201.684	-6005.123	-3363.1868	-869.4382	-1299.2521	-518.6284	-1427.5673	-132.38118	287.67993	110.05357	421.1147	-91.38667	-395.57556	-894.7644	436.7342	740.98285	-441.20605	-585.3324	-251.08379	795.16486	-747.71155	895.2871	-493.7143	-909.02814	639.47046	1132.7191	1190.0303	1198.9038	1918.09	1670.9011	1803.7748	1931.8983	2105.3345	2483.458	1952.2068	1971.3303	1820.954	1765.3276	3256.3262	1794.4498	1718.386	1667.4471	2386.2583	2890.6318	2488.068"
        self.b1 = [float(i) for i in a1.split("\t")]
        self.b2 = [float(i) for i in a2.split("\t")]
        self.b3 = [float(i) for i in a3.split("\t")]
        self.selected = True

    def showTime(self):
        try:
            shuju = self.li[self.index]  # 返回一个[0,1)之间的浮点型随机数*10
            self.x.append(shuju)  # 数组更新
            # self.ax.clear()
            self.ax.plot(self.x)
            self.canvas.draw()
            self.index += 1
            if self.index +1 > len(self.li):
                self.endTimer()
        except Exception as e:
            print(e)
        print(1111111111111)

    # 启动函数
    def startTimer(self):
        # 设置计时间隔并启动

        if self.selected:
            self.li = self.b2
            self.selected = False
        else:
            self.li = self.b3
            self.selected = True

        self.timer.start(1)  # 每隔一秒执行一次绘图函数 showTime
        # self.startBtn1.setEnabled(False)  # 开始按钮变为禁用
        # self.endBtn.setEnabled(True)  # 结束按钮变为可用

    def endTimer(self):
        self.timer.stop()  # 计时停止
        # self.startBtn1.setEnabled(True)  # 开始按钮变为可用
        # self.endBtn.setEnabled(False)  # 结束按钮变为可用
        self.x = []  # 清空数组
        self.index = 0 # 索引归零

    def clear_axes(self):
        self.timer.stop()
        self.ax.cla()
        self.canvas.draw()

# 运行程序
if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    app.exec()


