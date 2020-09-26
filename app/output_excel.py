#!python
import re
import xlsxwriter

def main(array, putFile):
	print(array)
	workbook = xlsxwriter.Workbook(putFile)
	worksheet1 = workbook.add_worksheet('result')
	dist = {}
	for dist_data in array:
		well = dist_data["well"]
		msg = dist_data["msg"]
		if(msg != ""):
			result = dist_data["result"]+"("+msg+")"
		else:
			result = dist_data["result"]
		a = re.match("([A-H])(\d+)", well)
		row = a.group(1)
		col = a.group(2)
		if(col not in dist):
			dist[col] = {
				row: result
			}
		else:
			dist[col][row] = result
	cols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"] 
	rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
	head = ["date", "lis_id", "Sampling_tube_id", "patient_id", "type", "Well", "Result"]
	for i in range(len(head)):
		worksheet1.write(0, i, head[i])
	row_num = 1
	for col in cols:
		for row in rows:
			line = []
			if(col in dist and row in dist[col]):
				line = [".", ".", ".", ".", "NovelCoronavirus", row+col, dist[col][row]]
			else:
				line = [".", ".", ".", ".", "NovelCoronavirus", row+col, "无数据"]
			for i in range(len(line)):
				worksheet1.write(row_num, i, line[i])
			row_num += 1
	workbook.close()