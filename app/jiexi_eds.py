#!python

import re
import os
import sys
import json
import shutil
import zipfile
import xmltodict
from pathlib import Path

def unzip_file(edsFile, base_path):
	'''
	@name: 解压eds文件
	@test: 
	@msg: 
	@param {eds文件，home路径} 
	@return: analysis_result.txt，路径地址
	'''
	
	directory = Path(base_path+"/tmp")
	unzipMe = zipfile.ZipFile(edsFile) 
	unzipMe.extractall(directory)
	unzipMe.close()
	analysisResulsFile = directory / "apldbio/sds/analysis_result.txt"
	xmlFile = directory / "apldbio/sds/plate_setup.xml"
	xmlWorkSheet = directory / "xl/worksheets/sheet1.xml"
	if os.path.exists(analysisResulsFile):
		return (analysisResulsFile, xmlFile, xmlWorkSheet)
	else: return

def jiexi_eds_results(analysisResulsFile):
	dist_data = {}
	cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
	with open(analysisResulsFile, "r") as f:
		lines = f.readlines()
		start_num = 0
		well_num = ""
		target = ""
		for line in lines:
			line = line.strip("\n")
			line = line.strip("\r")
			array = line.split("\t")
			if(array[0] == "Well"):
				start_num = 1
				continue
			elif(start_num == 1): pass
			else: continue
			if(start_num == 1):
				if(re.match("^\d+\t.*", line)):
					well_num = array[0]
					target = array[2]
				elif(re.match("^Delta Rn values\t(.*)", line)):
					a = re.match("^Delta Rn values\t(.*)", line)
					DRns = a.group(1).split("\t")
					well = cols[int(int(well_num)/12)]+str((int(well_num))%12+1)
					if(well not in dist_data):
						dist_data[well] = {target: DRns}
					else:
						dist_data[well][target] = DRns
			else: continue
	return(dist_data)

def jiexi_eds_xml_worksheet(xmlWorkSheet):
	distXml = {}
	f = open(xmlWorkSheet, "r", encoding = "utf-8")
	xml_data = f.read()
	f.close()
	dist_xml = xmltodict.parse(xml_data)
	dist_json = json.loads(json.dumps(dist_xml))
	for rowData in dist_json["worksheet"]["sheetData"]["row"]:
		well_num = 0
		if("is" in rowData["c"][0]):
			well_num = rowData["c"][0]["is"]["t"]
		elif("v" in rowData["c"][0]):
			well_num = rowData["c"][0]["v"]
		else: continue
		target_name = ""
		if("is" in rowData["c"][2]):
			target_name = rowData["c"][2]["is"]["t"]
		elif("v" in rowData["c"][2]):
			target_name = rowData["c"][2]["v"]
		else: continue
		reporter = ""
		if("is" in rowData["c"][4]):
			reporter = rowData["c"][4]["is"]["t"]
		elif("v" in rowData["c"][4]):
			reporter = rowData["c"][4]["v"]
		else: continue
		ct = 0
		if("is" in rowData["c"][6]):
			ct = rowData["c"][6]["is"]["t"]
		elif("v" in rowData["c"][6]):
			ct = rowData["c"][6]["v"]
		else: continue
		cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
		if(well_num == "Well"): continue
		else: pass
		well = cols[int((int(well_num)-1)/12)]+str((int(well_num)-1)%12+1)
		if(well not in distXml):
			distXml[well] = {target_name: [reporter, ct]}
		else:
			distXml[well][target_name] = [reporter, ct]
	return(distXml)
		
def return_data(distData, distXml):
	data = []
	for well in distData:
		dist = {
			"well": well
		}
		for target in distData[well]:
			dist1 = {}
			reporter = distXml[well][target][0]
			ct = distXml[well][target][1]
			dist1["ct"] = str(ct)
			dist1["rn"] = distData[well][target]
			if("data" not in dist):
				dist["data"] = {
					reporter: dist1
				}
			else:
				dist["data"][reporter] = dist1
		data.append(dist)
	return(data)

def remove_dir(base_path):
	shutil.rmtree("./tmp")

def main(edsFile):
	dist = {}
	base_path = sys.path[0]
	# try:
	analysisResulsFile, xmlDataFile, xmlWorkSheet = unzip_file(edsFile, "./")
	distData = jiexi_eds_results(analysisResulsFile)
	distXml = jiexi_eds_xml_worksheet(xmlWorkSheet)
	data = return_data(distData, distXml)
	remove_dir(base_path)
	dist["success"] = True
	return(data)

if __name__ == "__main__":
	dist = main()

















