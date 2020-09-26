# -*- coding:utf8 -*-
import sys
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QHeaderView, QItemDelegate, QApplication
# 用来装行表头所有复选框, 删除表格数据注意要清空此项
all_header_checkbox = []
header_field = ["", '管号', '结果', 'FAM', "VIC", "ROX", "HEX", "CY5", "kit_sql_id"]




class WidgetClicked(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):

        self.clicked.emit()

class CheckBoxHeader(QHeaderView):

    # 自定义 复选框全选信号
    select_all_clicked = QtCore.pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 55
    _y_offset = 20
    _width = 500
    _height = 500

    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None, ttable=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False
        self.ttable = ttable

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2.)

        if logicalIndex == 0:
            option = QtWidgets.QStyleOptionButton()
            option.rect = QtCore.QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QtWidgets.QStyle.State_Enabled | QtWidgets.QStyle.State_Active
            if self.isOn:
                option.state |= QtWidgets.QStyle.State_On
            else:
                option.state |= QtWidgets.QStyle.State_Off
            self.style().drawControl(QtWidgets.QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
                if self.isOn:
                    self.isOn = False
                else:
                    self.isOn = True
                    # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.isOn)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)

    # 自定义信号 select_all_clicked 的槽方法
    def change_state(self, isOn):
        # 如果行表头复选框为勾选状态
        if isOn:
            # 将所有的复选框都设为勾选状态
            for i in all_header_checkbox:
                i.setCheckState(QtCore.Qt.Checked)

            for i in range(self.ttable.tableWidget.rowCount()):

                self.ttable.set_row_edit(i)

        else:
            for i in all_header_checkbox:
                i.setCheckState(QtCore.Qt.Unchecked)
            for i in range(self.ttable.tableWidget.rowCount()):

                self.ttable.set_row_no_edit(i)


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):

        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class Table(object):
    item_old_data = {}
    item_new_data = {}
    not_value_items = []
    # 改动单元格颜色会引发itemChange事件，在保存时需要使用此变量隔离
    event_flag = True

    def initUI(self, parent):
        self.parent = parent
        self.grid = QtWidgets.QGridLayout(parent)
        self.tableWidget = QtWidgets.QTableWidget(parent)
        self.tableWidget.setStyleSheet("""
    
                                            QTableWidget{
                                              background-color:#EFEFEF;    
                                              /*相邻行颜色交替*/  
                                              alternate-background-color: #E6E6E6;
                                              border-top:none;    
                                              border-left:none;    
                                              border-right:none;    
                                              border-bottom:3px solid #B5B5B6;   
    
                                              /*selection-background-color:#44c767; */
                                          }
    
                                           QTableWidget::item QLineEdit{
                                               background-color:#EFEFEF;
                                           }
                                          /*表头*/  
                                           QHeaderView::section{
                                               background:#EFEFEF;
                                               alternate-background-color: #E6E6E6;
                                               color:#000000;
                                               border-bottom:5px solid #DCDDDD;  
                                               border-top:none;
                                               border-left:1px solid #DCDDDD;
                                               border-right:none;
    
                                           }
                                            /*表头选中*/  
                                           QHeaderView::section:checked{ background-color:#D3D3D4}
                                           """)
        """
                                            /*
                                           border-left:none;防止中间表头的border重叠 
                                           QHeaderView::section:first 
                                           {
                                               border-left:1px solid #DCDDDD;
                                           }
                                           */ 
                                           /*QTableView::item:!alternate:!selected{  
                                               background-color: #000000;    /*交替行的另一颜色*/  
                                           }*/ 
        """
        self.tableWidget.setObjectName("tableWidget")

        # 设置列数
        self.tableWidget.setColumnCount(len(header_field))

        self.tableWidget.setRowCount(0)

        # 设置表头内容
        self.header = CheckBoxHeader(ttable=self)  # 实例化自定义表头
        self.tableWidget.setHorizontalHeader(self.header)  # 设置表头
        self.tableWidget.setHorizontalHeaderLabels(header_field)  # 设置列表头字段
        self.header.select_all_clicked.connect(self.header.change_state)

        # 隐藏kit_sql_id 这一列(必须设置表头后才可隐藏)
        self.tableWidget.setColumnHidden(len(header_field) - 1, True)


        # 列宽自动分配
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 调整第一列宽度
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        # 设置列宽
        # self.tableWidget.horizontalHeader().setMinimumWidth(600)
        # 行高自动分配
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置纵向表头隐藏
        self.tableWidget.verticalHeader().setVisible(False)
        # 设置纵向表头宽度
        # self.tableWidget.verticalHeader().setFixedWidth(20)
        # 设置横向表头高度
        self.tableWidget.horizontalHeader().setFixedHeight(40)

        # # 设置表头不可点击
        # self.tableWidget.horizontalHeader().setSectionsClickable(False)
        # # 设置行高使用固定值
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # 设置行颜色交替，需要先在qss中设置alternate-background-color  QTableView::item:!alternate:!selected
        self.tableWidget.setAlternatingRowColors(True)
        # 设置网格虚线
        self.tableWidget.setGridStyle(QtCore.Qt.DashLine)
        # self.tableWidget.setShowGrid(False)

        # 禁止整个表编辑
        # self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 禁止第2列不可编辑
        # self.tableWidget.setItemDelegateForColumn(1, EmptyDelegate(self.tableWidget))
        # 设置表头不可点击
        self.tableWidget.horizontalHeader().setSectionsClickable(False)

        # 禁止多选
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.tableWidget.itemChanged.connect(self.item_new_info)
        self.tableWidget.itemDoubleClicked.connect(self.item_old_info)

        self.f1 = QtWidgets.QFrame(parent)
        self.grid.addWidget(self.tableWidget)
        self.grid.addWidget(self.f1)


    def item_new_info(self, item):
        # print(item.text())
        try:
            row = item.row()
            column = item.column()
            if (column + 1) != self.tableWidget.columnCount()  and self.event_flag:
                self.item_new_data[(row, column)] = item.text()
                if self.item_new_data.get((row, column)) and self.item_old_data.get((row, column)) and self.item_new_data.get((row, column)) == self.item_old_data.get((row, column)):
                    if (row + 1) % 2 == 0:
                        item.setBackground(QtGui.QColor('#E6E6E6'))
                    else:
                        item.setBackground(QtGui.QColor('#EFEFEF'))
                else:
                    if (row, column) not in self.not_value_items:
                        item.setBackground(QtGui.QColor('#ffff00'))
                    else:
                        item.setBackground(QtGui.QColor('#808080'))

        except Exception as e:
            traceback.print_exc()
            raise e

    def item_old_info(self, item):
        try:
            row = item.row()
            column = item.column()
            if (row, column) not in self.item_old_data.keys():
                self.item_old_data[(row, column)] = item.text()
        except Exception as e:
            traceback.print_exc()
            raise e

    def init_cls_paras(self):
        self.item_old_data = {}
        self.item_new_data = {}
        self.not_value_items = []
        global all_header_checkbox
        all_header_checkbox = []

    def modify(self, line):
        # print(self.tableWidget.currentRow())
        # print(self.tableWidget.currentItem())
        button = QtWidgets.QMessageBox.question(self.parent,"保存试剂盒类型","是否确认保存试剂盒类型？",
                                      QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel,QtWidgets.QMessageBox.Ok)

    def set_row_no_edit(self, row):
        for i in range(1, self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, i)

            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            else:
                self.tableWidget.cellWidget(row, i).setEnabled(False)
    def set_row_edit(self, row):
        for i in range(1, self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, i)
            if (row, i) not in self.not_value_items:
                if item:
                    item.setFlags(QtCore.Qt.ItemFlag(63))
                else:
                    self.tableWidget.cellWidget(row, i).setEnabled(True)

    def set_check(self, ch):
        global all_header_checkbox
        try:
            row = all_header_checkbox.index(ch)
            if ch.isChecked():
                ch.setChecked(False)
                self.set_row_no_edit(row)
            else:
                self.set_row_edit(row)
                ch.setChecked(True)
        except:
            traceback.print_exc()

    def set_check1(self, ch):
        global all_header_checkbox
        try:
            row = all_header_checkbox.index(ch)
            if ch.isChecked():
                print(ch.isChecked())
                self.set_row_edit(row)
            else:
                print(ch.isChecked())
                self.set_row_no_edit(row)
        except:
            traceback.print_exc()

    def create_row(self, row_index, *args):
        global all_header_checkbox
        wid = WidgetClicked()
        hbox = QtWidgets.QHBoxLayout(wid)
        hbox.setAlignment(QtCore.Qt.AlignCenter)
        check_box = QtWidgets.QCheckBox()
        hbox.addWidget(check_box)
        wid.clicked.connect(lambda: self.set_check(check_box))
        check_box.clicked.connect(lambda:self.set_check1(check_box))
        self.tableWidget.setCellWidget(row_index, 0, wid)
        all_header_checkbox.append(check_box)

        for i in range(1, len(args)+1):
            if args[i-1] == "#":
                pop_num = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(row_index, i, pop_num)
                self.not_value_items.append((row_index, i))
            else:
                pop_num = QtWidgets.QTableWidgetItem(args[i - 1])
                self.item_old_data[(row_index, i)] = args[i - 1]
                self.tableWidget.setItem(row_index, i, pop_num)

            self.tableWidget.item(row_index, i).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.item(row_index, i).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)



        # 设置某一列不可编辑
        # self.tableWidget.setItemDelegateForColumn(0,EmptyDelegate(self.tableWidget))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QtWidgets.QWidget()
    main_window.resize(QtCore.QSize(800, 600))
    win = Table()
    win.initUI(main_window)

    row_len = win.tableWidget.rowCount() + 1
    # 行数加一
    win.tableWidget.setRowCount(row_len)
    row_index = row_len - 1
    win.create_row(row_index, "A", "阴性", "40", "#", "38", "36", "39", "1")


    row_len = win.tableWidget.rowCount() + 1
    # 行数加一
    win.tableWidget.setRowCount(row_len)
    row_index = row_len - 1
    win.create_row(row_index, "B", "阴性", "40", "40", "38", "36", "44", "2")

    # 删除内容， 不会删除行数
    # win.tableWidget.clearContents()
    # 删除内容及行
    # win.tableWidget.removeRow(0)
    # win.tableWidget.removeRow(0)
    #
    # all_header_checkbox = []
    # header_field = ["", '管号', '结果', 'FAM', "VIC", "ROX", "HEX", "CY5", "kit_sql_id"]
    # item_old_data = {}
    # item_new_data = {}
    # not_value_items = []
    #
    # row_len = win.tableWidget.rowCount() + 1
    # # 行数加一
    # win.tableWidget.setRowCount(row_len)
    # row_index = row_len - 1
    # win.create_row(row_index, "A", "阴性", "40", "#", "38", "36", "39", "1")



    print(win.tableWidget.rowCount())
    win.tableWidget.setMaximumHeight(413)


    main_window.show()
    sys.exit(app.exec_())


