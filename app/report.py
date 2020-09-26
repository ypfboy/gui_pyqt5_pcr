#!python

import os
import sys
import time
import traceback

from app import jiexi_eds
from app import output_excel

'''
1、新冠
(1)达安
阴性：FAM 和 VIC 通道无扩增曲线或 Ct 值＞40，且 CY5 通道有扩增曲线
阳性：FAM 和 VIC 通道 Ct 值≤40，且有明显的扩增曲线
异常：在 FAM 或 VIC 单一通道 Ct 值≤40，另一通道无扩增曲线
7.1 如果检测样品在 FAM 和 VIC 通道无扩增曲线或 Ct 值＞40，且 CY5 通道有扩增曲线，可判样品未检测到 2019 新型冠状病毒
(2019-nCoV)RNA； 
7.2 如果检测样品在 FAM 和 VIC 通道 Ct 值≤40，且有明显的扩增曲线，可判样品为 2019 新型冠状病毒(2019-nCoV)阳性； 
7.3 如果检测样品仅在 FAM 或 VIC 单一通道 Ct 值≤40，另一通道无扩增曲线，结果需复检，复检结果一致可判样品为 2019 新型冠
状病毒(2019-nCoV)阳性；复检均为阴性可判断为未检测到 2019 新型冠状病毒(2019-nCoV)RNA 
(2)硕世
阳性：FAM或VIC的ct<=37
阴性：FAM和VIC的ct>40,CY5<=37
异常：FAM或VIC的ct>37且ct<=40，
(3)伯杰
阳性：FAM和VIC/HEX的ct<=38
阴性：FAM和VIC/HEX的ct>38，rox<=37
异常：其它
(4)卓诚惠
阳性：任意两个通道CT<=38，不管CY5
阴性：任意两个通道CT>=40，CY5《=38
异常：其它
'''

def novel_Coronavirus_Report_shuoshi(data):
	array = []
	for a in data:
		dist = {}
		if(a["data"] == {}): continue
		else: pass
		well = a["well"]
		fam_ct = float(a["data"]["FAM"]["ct"])
		vic_ct = float(a["data"]["VIC"]["ct"])
		cy5_ct = float(a["data"]["CY5"]["ct"])
		fam_rn = a["data"]["FAM"]["rn"]
		vic_rn = a["data"]["VIC"]["rn"]
		cy5_rn = a["data"]["CY5"]["rn"]

		if(fam_ct <= 37 or vic_ct <= 37):
			state = "阳性"
		elif(fam_ct >40 and vic_ct > 40 and cy5_ct <= 37):
			state = "阴性"
		else:
			state = "异常"
		msg = ""
		if(state == "异常"):
			msg = "FAM:"+str(fam_ct)+";VIC:"+str(vic_ct)+";ROX:"+str(rox_ct)
		else: msg = ""
		dist["well"] = well
		dist["msg"] = msg
		dist["result"] = state
		dist["data"] = [
			{
				"name": "FAM",
				"rn": fam_rn
			},
			{
				"name": "VIC",
				"rn": vic_rn
			},
			{
				"name": "CY5",
				"rn": cy5_rn
			}
		]
		array.append(dist)
	return(array)

def novel_Coronavirus_Report_DaAn(data):
	array = []
	for a in data:
		dist = {}
		if(a["data"] == {}): continue
		else: pass
		well = a["well"]
		fam_ct = float(a["data"]["FAM"]["ct"])
		vic_ct = float(a["data"]["VIC"]["ct"])
		cy5_ct = float(a["data"]["CY5"]["ct"])
		fam_rn = a["data"]["FAM"]["rn"]
		vic_rn = a["data"]["VIC"]["rn"]
		cy5_rn = a["data"]["CY5"]["rn"]

		if(fam_ct <= 40 and vic_ct <= 40):
			state = "阳性"
		elif(fam_ct >40 and vic_ct > 40 and cy5_ct <= 40):
			state = "阴性"
		else:
			state = "异常"
		msg = ""
		if(state == "异常"):
			msg = "FAM:"+str(fam_ct)+";VIC:"+str(vic_ct)+";ROX:"+str(rox_ct)
		else: msg = ""
		dist["well"] = well
		dist["msg"] = msg
		dist["result"] = state
		dist["data"] = [
			{
				"name": "FAM",
				"rn": fam_rn
			},
			{
				"name": "VIC",
				"rn": vic_rn
			},
			{
				"name": "CY5",
				"rn": cy5_rn
			}
		]
		array.append(dist)
	return(array)

def novel_Coronavirus_Report_BoJie(data):
	array = []
	for a in data:
		dist = {}
		if(a["data"] == {}): continue
		else: pass
		well = a["well"]
		fam_ct = float(a["data"]["FAM"]["ct"])
		
		rox_ct = float(a["data"]["ROX"]["ct"])
		fam_rn = a["data"]["FAM"]["rn"]
		
		rox_rn = a["data"]["ROX"]["rn"]
		
		if("VIC" in a["data"]):
			vic_ct = float(a["data"]["VIC"]["ct"])
			vic_rn = a["data"]["VIC"]["rn"]
		elif("HEX" in a["data"]):
			vic_ct = float(a["data"]["HEX"]["ct"])
			vic_rn = a["data"]["HEX"]["rn"]
		else: continue

		if(fam_ct <= 38 and vic_ct <= 38 and rox_ct <= 38):
			state = "阳性"
		elif(fam_ct >38 and vic_ct > 38 and rox_ct <= 38):
			state = "阴性"
		else:
			state = "异常"
		msg = ""
		if(state == "异常"):
			msg = "FAM:"+str(fam_ct)+";VIC:"+str(vic_ct)+";ROX:"+str(rox_ct)
		else: msg = ""
		dist["well"] = well
		dist["msg"] = msg
		dist["result"] = state
		dist["data"] = [
			{
				"name": "FAM",
				"rn": fam_rn
			},
			{
				"name": "VIC",
				"rn": vic_rn
			},
			{
				"name": "ROX",
				"rn": rox_rn
			}
		]
		array.append(dist)
	return(array)
			
def panduan_empty_well(array):
	wells = []
	rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
	cols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
	for a in array:
		well = a["well"]
		wells.append(well)
	for row in rows:
		for col in cols:
			dist = {}
			if(row+col not in wells):
				dist = {
					"well": row+col,
					"result": "无数据",
					"msg": "",
					"data": []
				}
				array.append(dist)
			else: continue
	return(array)

'''
data = [
{
    "pipe": a[1],
    "result": a[2],
    "FAM": a[3],
    "VIC": a[4],
    "ROX": a[5],
    "HEX": a[6],
    "CY5": a[7],
},
]
'''

def main(edsFile, model, kit, inputDist):
	dist = {}
	Bin = sys.path[0]
	data = jiexi_eds.main(edsFile)
	if(data == []):
		print("没提取到数据！")
	else: pass
	if not os.path.exists(Bin+"/xlsx/"):
		os.makedirs(Bin+"/xlsx/")
	else: pass
	try:
		array = []
		outPutFile = (Bin+"/xlsx/"+os.path.basename(edsFile).replace(".eds", "")+"_"+str(time.time()).replace(".", "")+".xlsx").replace("\\", "/")
		if(kit == "新冠_硕世"):
			array = novel_Coronavirus_Report_shuoshi(data)
		elif(kit == "新冠_达安"):
			array = novel_Coronavirus_Report_DaAn(data)
		elif(kit == "新冠_伯杰"):
			array = novel_Coronavirus_Report_BoJie(data)
		elif (kit == "新冠_伯杰"):
			array = novel_Coronavirus_Report_BoJie(data)
		else: 
			dist = {
				"success": False,
				"msg": "试剂盒类型错误",
				"data": []
			}
			return(dist)
		array = panduan_empty_well(array)
		output_excel.main(array, outPutFile)
		dist = {
			"success": True,
			"msg": "",
			"data": array
		}
	except Exception as e:
		dist = {
			"success": False,
			"msg": str(e),
			"data": []
		}
	return(dist, outPutFile)

if __name__ == '__main__':
	# main(sys.argv[1], "aaa", "新冠_伯杰", 3)
	print(main(r"C:\Users\61980\Desktop\FW_PCR\app\input\ZHUOCHENG-20200706-3(177-264).eds", "aaa", "新冠_伯杰", 3))