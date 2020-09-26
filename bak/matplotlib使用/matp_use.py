import matplotlib
import matplotlib.pyplot as plt
import numpy as np
a = "-2761.28	-380.3101	744.9255	479.52045	786.4591	1237.476	1025.6022	117.36899	802.9483	429.69952	-295.84616	160.79567	-736.5781	-671.28	-267.2632	-469.4339	-414.10455	104.88101	268.72595	970.08655	3609.4626	8884.698	19172.918	38912.668	75271.17	130198.45	194587.67	255300.55	302161.56	337904.84	366042.3	389242.16	409106.75	427707.66	442510.38	454943.22	467397.38	476516.9	486813.94	493995.22	501359.62	510118.1	516560.12	523697.53	530468.8"
a1 = "-6973.3677	-3470.593	-1596.975	-1277.8881	-482.23868	-935.74554	-588.3149	354.86572	-755.8911	-356.55426	78.37637	425.932	453.6439	32.94952	-144.5261	-131.50172	623.02264	-97.3592	-289.80356	-193.15419	-105.97356	-236.48042	-205.36229	-151.9629	169.46771	-765.5704	-1126.3273	-943.3341	-359.341	-1154.3479	-274.636	-626.73663	-674.1497	-910.43787	-2111.101	-2213.9517	-1742.8647	-1529.1841	-2666.9097	-3045.2603	-3673.1108	-3131.274	-3283.2185	-3152.9128	-4065.3572"
a2 = "-10201.684	-6005.123	-3363.1868	-869.4382	-1299.2521	-518.6284	-1427.5673	-132.38118	287.67993	110.05357	421.1147	-91.38667	-395.57556	-894.7644	436.7342	740.98285	-441.20605	-585.3324	-251.08379	795.16486	-747.71155	895.2871	-493.7143	-909.02814	639.47046	1132.7191	1190.0303	1198.9038	1918.09	1670.9011	1803.7748	1931.8983	2105.3345	2483.458	1952.2068	1971.3303	1820.954	1765.3276	3256.3262	1794.4498	1718.386	1667.4471	2386.2583	2890.6318	2488.068"
b = [float(i) for i in a.split("\t")]
b1 = [float(i) for i in a1.split("\t")]
b2 = [float(i) for i in a2.split("\t")]
# b = [15, -4, -100, 100]
print(b)
# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus']=False
#　设置　图像大小，　必须要在　ax = plt.gca()　之前设置
plt.figure(figsize=(8, 5), dpi=100)

# 设置画布颜色
# plt.gcf().set_facecolor("#5f809b")

# 获得当前的Axes对象
ax = plt.gca()


# 刻度显示位置
ax.yaxis.set_ticks_position("left")
ax.xaxis.set_ticks_position("bottom")
# 设置原点为（0， 0）
ax.spines['left'].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
# 去掉x、y轴对面的封闭线
ax.spines["right"].set_color('none')
ax.spines['top'].set_color('none')
# 设置坐标轴样式为虚线
ax.spines["left"].set_linestyle("--")
ax.spines["left"].set_alpha(0.5)
ax.spines["left"].set_color("#d4dde1")

print(dir(ax.spines["left"]))
# 网格设置， 设置为虚线, 设置网格线颜色
ax.grid(True, linestyle="--", alpha=0.5, c="#d4dde1")

# x、y轴刻度
my_x_ticks = np.arange(0, 50, 2)
# my_y_ticks = np.arange(-2, 2, 0.3)
# 方法1
# plt.xticks(my_x_ticks)
# plt.yticks(my_y_ticks)
# 方法2
ax.set_xticks(my_x_ticks)
kwargs = {"color": "blue", "rotation": 90}
labels = ax.set_xticklabels(my_x_ticks, **kwargs)
# for l in labels:
#     l.update(kwargs)

# 设置 主刻度线 长度为0， 也就是不显示
ax.tick_params(which='major',direction='in', length=0)

# x、y轴范围
# plt.ylim((-100000, 1100000))


ax.plot(list(range(len(b))), b)
ax.plot(list(range(len(b1))), b1)
ax.plot(list(range(len(b2))), b2)
plt.show()

