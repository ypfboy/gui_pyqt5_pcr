# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Figure_Canvas(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
    instance = None

    # def __new__(cls, *args, **kwargs):
    #     if cls.instance:
    #        return cls.instance
    #     cls.instance = super(Figure_Canvas, cls).__new__(cls)
    #     return cls.instance

    def __init__(self, parent=None, width=4, height=3, dpi=100):
        # 如果负号显示不正常，设置此项
        matplotlib.rcParams['axes.unicode_minus'] = False
        # 设置　图像大小，　必须要在　获取画布　之前设置
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，或是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, self.fig) # 初始化父类
        self.setParent(parent)

        # 获取画布
        self.axes = plt.subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法

        # 设置画布
        self.set_axes()


    def set_axes(self):
        # 刻度显示位置
        self.axes.yaxis.set_ticks_position("left")
        self.axes.xaxis.set_ticks_position("bottom")
        # # 设置原点为（0， 0） (修改为只设置y轴不设置x轴)
        self.axes.spines['left'].set_position(("data", 0))
        # self.axes.spines["bottom"].set_position(("data", 0))
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

    def set_xticks(self, li_len=50, interval=2, rotation=0, color=""):

        # x、y轴刻度
        my_x_ticks = np.arange(0, li_len, interval)
        self.axes.set_xticks(my_x_ticks)
        kwargs = {}
        if color:
            kwargs["color"] = color
        if rotation:
            kwargs["rotation"] = rotation
        if kwargs:
            labels = self.axes.set_xticklabels(my_x_ticks, **kwargs)

            # for l in labels:
            #     l.update(kwargs)

    def draw_pic(self):
        pass

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












