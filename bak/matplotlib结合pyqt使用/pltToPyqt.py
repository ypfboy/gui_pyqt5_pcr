# -*- coding: utf-8 -*-
import random
import traceback

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets, QtCore


class Figure_Canvas(FigureCanvas):  # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键

    def __init__(self, parent=None, width=4, height=3, dpi=100):
        # 如果负号显示不正常，设置此项
        matplotlib.rcParams['axes.unicode_minus'] = False
        # 解决中文乱码
        plt.rcParams['font.sans-serif'] = ['SimHei']

        # 设置　图像大小，　必须要在　获取画布　之前设置
        self.fig = plt.figure(figsize=(width, height),
                              dpi=dpi)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，或是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, self.fig)  # 初始化父类
        self.setParent(parent)

        # 获取画布
        self.axes = plt.subplot(1, 1, 1)  # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法

        # 设置画布
        self.set_axes()

    def set_axes(self):
        # 刻度显示位置
        self.axes.yaxis.set_ticks_position("left")
        self.axes.xaxis.set_ticks_position("bottom")
        # 设置原点为（0， 0）
        self.axes.spines['left'].set_position(("data", 0))
        self.axes.spines["bottom"].set_position(("data", 0))
        # 去掉x、y轴对面的封闭线
        self.axes.spines["right"].set_color('none')
        self.axes.spines['top'].set_color('none')
        # 设置坐标轴样式为虚线
        self.axes.spines["left"].set_linestyle("--")
        self.axes.spines["left"].set_alpha(0.5)
        self.axes.spines["left"].set_color("#808080")
        # 网格设置， 设置为虚线, 设置网格线颜色
        self.axes.grid(True, linestyle="--", alpha=0.5, c="#808080")

        # 设置 主刻度线 长度为0， 也就是不显示
        self.axes.tick_params(which='major', direction='in', length=0)
        # x、y轴范围
        # plt.ylim((-100000, 1100000))

    def set_xticks(self, axes, li_len=50, interval=2, rotation=0, color=""):
        # x、y轴刻度
        my_x_ticks = np.arange(0, li_len, interval)
        axes.set_xticks(my_x_ticks)
        kwargs = {}
        if color:
            kwargs["color"] = color
        if rotation:
            kwargs["rotation"] = rotation
        if kwargs:
            labels = axes.set_xticklabels(my_x_ticks, **kwargs)

            # for l in labels:
            #     l.update(kwargs)



    def test(self):
        a = "-2761.28	-380.3101	744.9255	479.52045	786.4591	1237.476	1025.6022	117.36899	802.9483	429.69952	-295.84616	160.79567	-736.5781	-671.28	-267.2632	-469.4339	-414.10455	104.88101	268.72595	970.08655	3609.4626	8884.698	19172.918	38912.668	75271.17	130198.45	194587.67	255300.55	302161.56	337904.84	366042.3	389242.16	409106.75	427707.66	442510.38	454943.22	467397.38	476516.9	486813.94	493995.22	501359.62	510118.1	516560.12	523697.53	530468.8"
        a1 = "-6973.3677	-3470.593	-1596.975	-1277.8881	-482.23868	-935.74554	-588.3149	354.86572	-755.8911	-356.55426	78.37637	425.932	453.6439	32.94952	-144.5261	-131.50172	623.02264	-97.3592	-289.80356	-193.15419	-105.97356	-236.48042	-205.36229	-151.9629	169.46771	-765.5704	-1126.3273	-943.3341	-359.341	-1154.3479	-274.636	-626.73663	-674.1497	-910.43787	-2111.101	-2213.9517	-1742.8647	-1529.1841	-2666.9097	-3045.2603	-3673.1108	-3131.274	-3283.2185	-3152.9128	-4065.3572"
        a2 = "-10201.684	-6005.123	-3363.1868	-869.4382	-1299.2521	-518.6284	-1427.5673	-132.38118	287.67993	110.05357	421.1147	-91.38667	-395.57556	-894.7644	436.7342	740.98285	-441.20605	-585.3324	-251.08379	795.16486	-747.71155	895.2871	-493.7143	-909.02814	639.47046	1132.7191	1190.0303	1198.9038	1918.09	1670.9011	1803.7748	1931.8983	2105.3345	2483.458	1952.2068	1971.3303	1820.954	1765.3276	3256.3262	1794.4498	1718.386	1667.4471	2386.2583	2890.6318	2488.068"
        b = [float(i) for i in a.split("\t")]
        b1 = [float(i) for i in a1.split("\t")]
        b2 = [float(i) for i in a2.split("\t")]
        # b = [15, -4, -100, 100]
        print(b)

        self.axes.plot(list(range(len(b))), b, color="#8fefd6")
        self.axes.plot(list(range(len(b1))), b1, color="#f9938f")
        self.axes.plot(list(range(len(b2))), b2, color="#d4dde1")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_10 = QtWidgets.QFrame(self.centralwidget)
        self.frame_10.setGeometry(QtCore.QRect(69, 50, 581, 441))
        self.frame_10.setMinimumSize(QtCore.QSize(581, 441))
        self.frame_10.setStyleSheet("")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.draw_fun()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def draw_fun(self):
        # ===通过graphicview来显示图形
        """
        self.horizontalLayout_1110 = QtWidgets.QGridLayout(self.frame_10)
        self.graphicview = QtWidgets.QGraphicsView(self.frame_10)  # 第一步，创建一个QGraphicsView
        # 去除边框
        self.graphicview.setStyleSheet("border:none;")
        # 去除滑动条
        self.graphicview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicview.setObjectName("graphicview")

        self.dr = Figure_Canvas()
        # 实例化一个FigureCanvas
        # self.dr.test()  # 画图
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(self.dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicview.setScene(graphicscene)  # 第五步，把QGraphicsScene放入QGraphicsView
        self.graphicview.show()  # 最后，调用show方法呈现图形！Voila!!
        # self.graphicview.setFixedSize(500, 500)
        self.but = QtWidgets.QPushButton(self.frame_10)

        self.horizontalLayout_1110.addWidget(self.graphicview)
        self.horizontalLayout_1110.addWidget(self.but)
        """

        # 方法2
        self.horizontalLayout_1110 = QtWidgets.QGridLayout(self.frame_10)
        # 实例化一个FigureCanvas
        self.dr = Figure_Canvas(width=4, height=4, dpi=100, parent=self.frame_10)
        # self.dr.set_xticks(rotation=90)
        # self.dr.test()  # 画图
        self.but = QtWidgets.QPushButton(self.frame_10)
        self.but.setText("画线")
        self.but1 = QtWidgets.QPushButton(self.frame_10)
        self.but1.setText("选择一条线")
        self.horizontalLayout_1110.addWidget(self.dr)
        self.horizontalLayout_1110.addWidget(self.but)
        self.horizontalLayout_1110.addWidget(self.but1)


class ReMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.num = random.randint(1, 100)
        self.x1 = np.random.randint(3000, size=self.num)
        # self.y = np.cos(self.x)
        self.y1 = np.random.randint(3000, size=self.num)
        self.x1.sort()
        self.y1.sort()
        self.line1 = self.dr.axes.plot(self.x1, self.y1, color="#8fefd6")[0]

        self.x2 = np.random.randint(3000, size=self.num)
        # self.y = np.cos(self.x)
        self.y2 = np.random.randint(3000, size=self.num)
        self.x2.sort()
        self.y2.sort()
        self.line2 = self.dr.axes.plot(self.x2, self.y2, color="#8fefd6")[0]

        print(self.line1)
        print(self.line2)
        self.count = 0
        # self.but.clicked.connect(self.plot_update_line)
        # self.but.clicked.connect(self.plot_update_axes)
        # self.but.clicked.connect(self.plot_dynamic_line)
        self.but.clicked.connect(self.start_time)
        self.but1.clicked.connect(self.select_line)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.init_data()

    def init_data(self):
        self.y1 = []
        self.y2 = []
        self.y3 = []
        self.index1 = 0  # 列表索引
        self.index2 = 0  # 列表索引
        self.index3 = 0  # 列表索引
        a1 = "-2761.28	-380.3101	744.9255	479.52045	786.4591	1237.476	1025.6022	117.36899	802.9483	429.69952	-295.84616	160.79567	-736.5781	-671.28	-267.2632	-469.4339	-414.10455	104.88101	268.72595	970.08655	3609.4626	8884.698	19172.918	38912.668	75271.17	130198.45	194587.67	255300.55	302161.56	337904.84	366042.3	389242.16	409106.75	427707.66	442510.38	454943.22	467397.38	476516.9	486813.94	493995.22	501359.62	510118.1	516560.12	523697.53	530468.8"
        a2 = "-6973.3677	-3470.593	-1596.975	-1277.8881	-482.23868	-935.74554	-588.3149	354.86572	-755.8911	-356.55426	78.37637	425.932	453.6439	32.94952	-144.5261	-131.50172	623.02264	-97.3592	-289.80356	-193.15419	-105.97356	-236.48042	-205.36229	-151.9629	169.46771	-765.5704	-1126.3273	-943.3341	-359.341	-1154.3479	-274.636	-626.73663	-674.1497	-910.43787	-2111.101	-2213.9517	-1742.8647	-1529.1841	-2666.9097	-3045.2603	-3673.1108	-3131.274	-3283.2185	-3152.9128	-4065.3572"
        a3 = "-10201.684	-6005.123	-3363.1868	-869.4382	-1299.2521	-518.6284	-1427.5673	-132.38118	287.67993	110.05357	421.1147	-91.38667	-395.57556	-894.7644	436.7342	740.98285	-441.20605	-585.3324	-251.08379	795.16486	-747.71155	895.2871	-493.7143	-909.02814	639.47046	1132.7191	1190.0303	1198.9038	1918.09	1670.9011	1803.7748	1931.8983	2105.3345	2483.458	1952.2068	1971.3303	1820.954	1765.3276	3256.3262	1794.4498	1718.386	1667.4471	2386.2583	2890.6318	2488.068"
        self.li1 = [float(i) for i in a1.split("\t")]
        self.li2 = [float(i) for i in a2.split("\t")]
        self.li3 = [float(i) for i in a3.split("\t")]
        self.selected1 = True
        self.selected2 = False
        self.selected3 = True

    def show_time(self):
        try:
            if self.index1 < len(self.li1):
                d1 = self.li1[self.index1]
                self.y1.append(d1)
                self.index1 += 1
            if self.index2 < len(self.li2):
                d2 = self.li2[self.index2]
                self.y2.append(d2)
                self.index2 += 1

            if self.index3 < len(self.li3):
                d3 = self.li3[self.index3]
                self.y3.append(d3)
                self.index3 += 1

            self.dr.axes.clear()
            flag= 0
            flag1 = []
            if self.selected1:
                flag1.append((self.index1,len(self.li1)))
                self.dr.axes.plot(list(range(len(self.y1))), self.y1)
            if self.selected2:
                flag1.append((self.index2, len(self.li2)))
                self.dr.axes.plot(list(range(len(self.y2))), self.y2)
            if self.selected3:
                flag1.append((self.index3, len(self.li3)))
                self.dr.axes.plot(list(range(len(self.y3))), self.y3)
            self.dr.set_axes()
            self.dr.fig.canvas.draw()
            for k, v in flag1:
                if k >= v:
                    flag += 1
            if flag == self.select_count:
                self.end_time()
            print(11)
        except:
            traceback.print_exc()

    def end_time(self):
        self.timer.stop()
        self.init_data()
        self.selected1 = False
        self.selected2 = False
        self.selected3 = True


    def start_time(self):
        print(self.timer)
        self.dr.axes.cla()
        self.dr.fig.canvas.draw()
        self.select_count = len([i for i in [self.selected1, self.selected2, self.selected3] if i])
        self.timer.start(1)  # 每隔一毫秒执行一次绘图函数 showTime

    def select_line(self):
        self.end_time()
        self.start_time()



    def plot_update_line(self):
        """动态更新同一条曲线的内容"""
        self.count += 1
        if self.count < 10:
            try:
                # p = random.randint(1, 1000)
                # num = random.randint(1, 100)
                updated_y = np.random.randint(1000, size=self.num)
                updated_y.sort()
                self.line1.set_xdata(self.x2)
                self.line1.set_ydata(updated_y)
                # 更新图像
                self.dr.fig.canvas.draw()
                print(id(self.dr.fig))
                # self.dr.fig.canvas.flush_events()
            except Exception as e:
                print(e)
        else:
            """
            移除某一条曲线
            """
            try:
                self.dr.axes.lines.remove(self.dr.axes.lines[0])
                self.dr.fig.canvas.draw()
            except Exception as e:
                print(e)

    def plot_update_axes(self):
        """
            plt.ion()：打开交互模式
            plt.ioff()：关闭交互模式
            plt.clf()：清除当前的Figure对象(figure是初始化的画布对象)
            plt.cla()：清除当前的`Axes对象`（Axes对象保存了画布及画布的一些设置，plt.cla()清空画布设置，及画布所画图像）
            plt.pause()：暂停功能
        """
        try:
            self.dr.axes.cla()
            rotation = random.randint(1, 90)
            num_x = random.randint(50, 900)
            # FIXME x,y必须长度相同
            # num_y = random.randint(50, 900)
            self.x3 = np.random.randint(3000, size=num_x)
            # self.y = np.cos(self.x)
            # self.y3 = np.random.randint(3000, size=num_x)
            self.x3.sort()
            # self.y3.sort()
            self.line2 = self.dr.axes.plot(list(range(len(self.x3))), self.x3, color="#8fefd6")[0]
            # self.dr.set_xticks(rotation=rotation, li_len=len(self.x3), interval=1000)
            self.dr.set_axes()
            print(id(self.dr.axes))
            # 更新图像
            self.dr.fig.canvas.draw()
        except Exception as e:
            print(e)

    def plot_dynamic_line(self):
        a = "-2761.28	-380.3101	744.9255	479.52045	786.4591	1237.476	1025.6022	117.36899	802.9483	429.69952	-295.84616	160.79567	-736.5781	-671.28	-267.2632	-469.4339	-414.10455	104.88101	268.72595	970.08655	3609.4626	8884.698	19172.918	38912.668	75271.17	130198.45	194587.67	255300.55	302161.56	337904.84	366042.3	389242.16	409106.75	427707.66	442510.38	454943.22	467397.38	476516.9	486813.94	493995.22	501359.62	510118.1	516560.12	523697.53	530468.8"
        a1 = "-6973.3677	-3470.593	-1596.975	-1277.8881	-482.23868	-935.74554	-588.3149	354.86572	-755.8911	-356.55426	78.37637	425.932	453.6439	32.94952	-144.5261	-131.50172	623.02264	-97.3592	-289.80356	-193.15419	-105.97356	-236.48042	-205.36229	-151.9629	169.46771	-765.5704	-1126.3273	-943.3341	-359.341	-1154.3479	-274.636	-626.73663	-674.1497	-910.43787	-2111.101	-2213.9517	-1742.8647	-1529.1841	-2666.9097	-3045.2603	-3673.1108	-3131.274	-3283.2185	-3152.9128	-4065.3572"
        a2 = "-10201.684	-6005.123	-3363.1868	-869.4382	-1299.2521	-518.6284	-1427.5673	-132.38118	287.67993	110.05357	421.1147	-91.38667	-395.57556	-894.7644	436.7342	740.98285	-441.20605	-585.3324	-251.08379	795.16486	-747.71155	895.2871	-493.7143	-909.02814	639.47046	1132.7191	1190.0303	1198.9038	1918.09	1670.9011	1803.7748	1931.8983	2105.3345	2483.458	1952.2068	1971.3303	1820.954	1765.3276	3256.3262	1794.4498	1718.386	1667.4471	2386.2583	2890.6318	2488.068"
        b = [float(i) for i in a.split("\t")]
        b1 = [float(i) for i in a1.split("\t")]
        b2 = [float(i) for i in a2.split("\t")]
        b1.extend(b2)
        b1.extend(b)
        x = []
        y = []
        for n in range(len(b1)):
            x.append(n)
            y.append(b1[n])
            self.dr.axes.cla()
            self.dr.axes.plot(x, y, color='black', linewidth=0.2)
            # line2,=plt.plot(tm[m],resp[m],marker='o',color='red',markersize=0.2)
            self.dr.fig.canvas.draw()
            # plt.pause(0.00001)
            # ax.lines.remove(line2)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    main_window = ReMainWindow()
    main_window.show()
    sys.exit(app.exec_())
