# -*- coding:utf8 -*-

import os
import random
import shutil
import sys

import traceback
from resources import my_imgs_rc
from PyQt5 import QtCore, QtGui, QtWidgets
from config import constants
from utils.connectSolite import ConnectSqlite
from views import add
from views.pcr import Ui_MainWindow
from utils.pltToPyqt import Figure_Canvas
from app import report
from views import uiTable
from views import uiTableKit


class ReMainWindow(QtWidgets.QMainWindow):
    start_size = 1024 * 768
    flag = False

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        width = self.geometry().size().width()
        height = self.geometry().size().height()
        size = width * height // self.start_size * 15

        # print(size)
        if size >= 22:
            size = 22
        if size < 15:
            size = 15
        if width > 1500:
            self.flag = True
        else:
            self.flag = False
        self.setStyleSheet("font: %spx '微软雅黑';" % size)


class MyMainWindow(Ui_MainWindow, ReMainWindow):
    set_select_selected = "pushButton_parse"
    set_settings_selected = "pushButton_settings_1"

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        try:
            self.setupUi(self)
            self.init_pic()

            self.pushButton_parse.clicked.connect(lambda: self.set_select(self.pushButton_parse.objectName()))
            self.pushButton_history.clicked.connect(lambda: self.set_select(self.pushButton_history.objectName()))
            self.pushButton_upload_many.clicked.connect(
                lambda: self.set_select(self.pushButton_upload_many.objectName()))
            self.pushButton_settings.clicked.connect(lambda: self.set_select(self.pushButton_settings.objectName()))
            self.pushButton_support.clicked.connect(lambda: self.set_select(self.pushButton_support.objectName()))

            self.pushButton_settings_1.clicked.connect(
                lambda: self.set_settings(self.pushButton_settings_1.objectName()))
            self.pushButton_settings_2.clicked.connect(
                lambda: self.set_settings(self.pushButton_settings_2.objectName()))

            # 下机数据
            self.pushButton_input.clicked.connect(self.pushButton_input_clicked)
            # 样本信息
            self.pushButton_example_info.clicked.connect(self.example_info)
            # 生成报告
            self.pushButton_generate_word.clicked.connect(self.generate_word)
            # 上传报告
            self.pushButton_upload_word.clicked.connect(self.upload_word)


            # 　按钮事件
            self.buttons_event()
            # 界面切换
            self.set_select(self.set_select_selected)
            self.set_settings(self.set_settings_selected)
            # 画线
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.show_time)
            self.init_data()
            # 复选框
            self.checkBox_flag = 0
            self.set_checkbox()

            # settings
            self.table_machine_num = uiTable.Table()
            self.table_machine_num.initUI(self.frame_machine_num)
            self.table_kit_type = uiTableKit.Table()
            self.table_kit_type.initUI(self.frame_kit_type)

            #　用于隔离下拉框与恢复默认功能
            self.switch_set_flag = True

            # machine 、kit
            self.conn_obj = ConnectSqlite()
            self.init_machine()
            self.init_comboBox_machine_type_num()
            self.init_kit_type()

            # kit下拉框切换
            self.comboBox_kit_type.currentIndexChanged.connect(self.switch_kit_type)

            # machine删除
            self.pushButton_machine_del.clicked.connect(self.machine_del)
            # machine增加
            self.pushButton_machine_add.clicked.connect(self.machine_add)
            # machine保存修改
            self.pushButton_machine_save.clicked.connect(self.machine_save)
            # kit保存修改
            self.pushButton_kit_save.clicked.connect(self.kit_save)
            # kit恢复默认
            self.pushButton_kit_default.clicked.connect(self.kit_default)

            # 报告存放位置
            self.generate_word_file = ""


        except:
            traceback.print_exc()

    def init_machine(self):
        ret = self.conn_obj.select("select * from machines")
        # ret1 = self.conn_obj.select("select distinct machine_type from machines")
        # machine_type = [i[0] for i in ret1]

        self.machine_type_num = []
        for i in range(len(ret)):
            row_len = i + 1
            # 行数加一
            self.table_machine_num.tableWidget.setRowCount(row_len)
            # 写入数据
            ty = ret[i][1]
            self.machine_type_num.append(ty)
            self.table_machine_num.create_row(ty, ret[i][2].strip().split(","), str(ret[i][0]), i)

        self.table_machine_num.item_old_data = self.table_machine_num.item_new_data
        self.table_machine_num.item_new_data = {}

    def init_comboBox_machine_type_num(self):
        for i in self.machine_type_num:
            self.comboBox_machine_type_num.addItem(i)

    def kit_default(self):
        self.pushButton_kit_default.setStyleSheet("border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")
        ret = QtWidgets.QMessageBox.question(self, "提示", "确认保存修改",
                                             QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                             QtWidgets.QMessageBox.Cancel)
        if ret == QtWidgets.QMessageBox.Cancel:
            self.pushButton_kit_default.setStyleSheet(
                "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
            return
        try:

            # 清空表格
            for i in range(self.table_kit_type.tableWidget.rowCount()):
                self.table_kit_type.tableWidget.removeRow(0)

            # 下拉框切换时不做操作
            self.switch_set_flag = False

            # 当前参数设置界面kit下拉框的值
            now_kit_type_val = self.comboBox_kit_type.currentText()

            # 类变量初始化
            self.table_kit_type.init_cls_paras()

            # comboBox内容清空
            # self.kit_types = []
            # self.comboBox_kit_type.clear()
            # self.comboBox_kits_type.clear()

            # 删除kits表， 复制kits_def为kits表
            self.conn_obj.creat_kits_from_kits_def(now_kit_type_val)
            self.init_kit_type()

            # 恢复下拉框
            self.switch_set_flag = True

        except:
            traceback.print_exc()
        self.pushButton_kit_default.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")

    def init_kit_type(self):

        ret = self.conn_obj.select("select distinct kit_type from kits")
        self.kit_types = [i[0] for i in ret]
        if self.switch_set_flag:
            [self.comboBox_kit_type.addItem(i) for i in self.kit_types]
            [self.comboBox_kits_type.addItem(i) for i in self.kit_types]

        ret1 = self.conn_obj.select(
            "select * from kits where kit_type='%s'" % self.comboBox_kit_type.currentText())

        ret1 = [(*i[1:8], str(i[0])) for i in ret1]
        for i in range(len(ret1)):
            row_len = i + 1
            # 行数加一
            self.table_kit_type.tableWidget.setRowCount(row_len)
            # 写入数据
            self.table_kit_type.create_row(i, *ret1[i])

        self.table_kit_type.item_old_data = self.table_kit_type.item_new_data
        self.table_kit_type.item_new_data = {}

    def switch_kit_type(self):
        if self.switch_set_flag:
            # 清空表格
            for i in range(self.table_kit_type.tableWidget.rowCount()):
                self.table_kit_type.tableWidget.removeRow(0)
            # self.table_kit_type.tableWidget.clearContents()

            ret1 = self.conn_obj.select(
                "select * from kits where kit_type='%s'" % self.comboBox_kit_type.currentText())

            self.table_kit_type.init_cls_paras()

            ret1 = [(*i[1:8], str(i[0])) for i in ret1]
            for i in range(len(ret1)):
                row_len = i + 1
                # 行数加一
                self.table_kit_type.tableWidget.setRowCount(row_len)
                # 写入数据
                self.table_kit_type.create_row(i, *ret1[i])

            self.table_kit_type.item_old_data = self.table_kit_type.item_new_data
            self.table_kit_type.item_new_data = {}
            for i in self.table_kit_type.item_old_data.keys():
                if (i[0] + 1) % 2 == 0:
                    self.table_kit_type.tableWidget.item(*i).setBackground(QtGui.QColor('#E6E6E6'))
                else:
                    self.table_kit_type.tableWidget.item(*i).setBackground(QtGui.QColor('#EFEFEF'))

    def init_pic(self):

        self.horizontalLayout_1110 = QtWidgets.QGridLayout(self.frame_pic)
        self.dr = Figure_Canvas(width=4, height=3, dpi=100, parent=self.frame_pic)
        self.horizontalLayout_1110.addWidget(self.dr)
        # print(self.horizontalLayout_1110.count())

    def machine_del(self):
        self.pushButton_machine_del.setStyleSheet(
            "border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")

        if any([i.isChecked() for i in uiTable.all_header_checkbox]):
            ret = QtWidgets.QMessageBox.question(self,"提示","确认删除选中的机器编号？",QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel,QtWidgets.QMessageBox.Cancel)

            if ret == QtWidgets.QMessageBox.Ok:
                try:
                    del_rows_index = [i for i in range(len(uiTable.all_header_checkbox)) if uiTable.all_header_checkbox[i].isChecked()]
                    del_rows_index.sort(reverse=True)
                    last_column_index = self.table_machine_num.tableWidget.columnCount() -1
                    del_rows_sql_ids = [int(self.table_machine_num.tableWidget.item(i, last_column_index).text()) for i in del_rows_index]



                    if len(del_rows_sql_ids) == 1:
                        self.conn_obj.update("delete from machines where id = %s" % str(del_rows_sql_ids[0]))
                    else:
                        self.conn_obj.update("delete from machines where id in %s"  % str(tuple(del_rows_sql_ids)))

                    # 清空tableWidget显示内容， 不清除表头设置
                    # self.table_machine_num.tableWidget.clear()
                    for _ in range(self.table_machine_num.tableWidget.rowCount()):
                        self.table_machine_num.tableWidget.removeRow(0)
                    # 清空Table类变量
                    self.table_machine_num.init_cls_paras()
                    # 清空分析界面机器类型下拉框内容
                    self.machine_type_num = []
                    self.comboBox_machine_type_num.clear()
                    # 重新加载tableWidget显示内容
                    self.init_machine()
                    # 重新加载分析界面机器类型下拉框内容
                    self.init_comboBox_machine_type_num()

                except:
                    traceback.print_exc()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "请勾选要删除的机器编号")

        self.pushButton_machine_del.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")

    def machine_add(self):
        self.pushButton_machine_add.setStyleSheet(
            "border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")
        myWin = add.MyMainForm()
        myWin.exec_()
        add_li = myWin.add_li
        # add_li[1] = add_li[1].strip().split(",")

        if add_li:
            self.conn_obj.update("insert into machines values(null, '%s', '%s')" % (add_li[0], add_li[1]))
            sql_id = self.conn_obj.select("select max(id) from machines")[0][0]

            row_len = self.table_machine_num.tableWidget.rowCount() + 1
            self.table_machine_num.tableWidget.setRowCount(row_len)
            self.table_machine_num.create_row(add_li[0], add_li[1].strip().split(","), str(sql_id), row_len - 1)

            # 清空分析界面机器类型下拉框内容
            self.machine_type_num = []
            self.comboBox_machine_type_num.clear()
            # 重新加载分析界面机器类型下拉框内容
            ret = self.conn_obj.select("select * from machines")
            for i in range(len(ret)):
                ty = ret[i][1]
                self.machine_type_num.append(ty)
            self.init_comboBox_machine_type_num()

        self.pushButton_machine_add.setStyleSheet(
            "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")

    def machine_save(self):
        self.pushButton_machine_save.setStyleSheet(
            "border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")
        try:
            # print("ssss: %s" % str(self.table_machine_num.item_new_data))
            if not self.table_machine_num.item_new_data and not self.table_machine_num.combobox_new_data:
                QtWidgets.QMessageBox.warning(self, "提示", "           未做修改         ")
                self.pushButton_machine_save.setStyleSheet(
                    "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
                return
            update_items = {}
            for k, v in self.table_machine_num.item_new_data.items():
                if self.table_machine_num.item_old_data[k] == v:
                    continue
                update_items[k] = v
            update_combobox = {}
            for k, v in self.table_machine_num.combobox_new_data.items():
                if self.table_machine_num.combobox_old_data[k] == v:
                    continue
                update_combobox[k] = v
            if not update_combobox and not update_items:
                QtWidgets.QMessageBox.warning(self, "提示", "           未做修改         ")
                self.pushButton_machine_save.setStyleSheet(
                    "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
                return

            for k, v in update_items.items():
                if v == "":
                    QtWidgets.QMessageBox.warning(self, "提示", "           保存不能为空         ")
                    self.pushButton_machine_save.setStyleSheet(
                        "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
                    return

            # FIXME 可以在这里添加保存的数据限制

            ret = QtWidgets.QMessageBox.question(self, "提示", "确认保存修改",
                                                 QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                 QtWidgets.QMessageBox.Cancel)
            if ret == QtWidgets.QMessageBox.Cancel:
                self.pushButton_machine_save.setStyleSheet(
                    "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
                return

            update_data = {}
            for k, v in update_items.items():
                if isinstance(update_data.get(k[0]), dict):
                    update_data[k[0]][k[1]] = v
                else:
                    update_data[k[0]] = {}
                    update_data[k[0]][k[1]] = v
            for k, v in update_combobox.items():
                if isinstance(update_data.get(v[0]), dict):
                    update_data[v[0]][2] = v[2]
                else:
                    update_data[v[0]] = {}
                    update_data[v[0]][2] = v[2]

            machine_sql_id_index = self.table_machine_num.tableWidget.columnCount() - 1
            for k, v in update_data.items():
                row_sql_id = self.table_machine_num.tableWidget.item(k, machine_sql_id_index).text()
                old_sql_type_data = self.conn_obj.select("select machine_type from machines where id=%s" % row_sql_id)[0][0]
                new_sql = "update machines set "
                new_sql_1 = ""
                for k1, v1 in v.items():
                    if k1 == 1:
                        new_sql_1 += self.conn_obj.machine_fields[k1] + "='%s'," % v1
                    elif k1 == 2:
                        li = old_sql_type_data.split(",")
                        li.remove(v1)
                        li.insert(0, v1)
                        new_sql_1 += self.conn_obj.machine_fields[k1] + "='%s'," % ",".join(li)
                new_sql += new_sql_1.strip().strip(",")
                new_sql += " where id=%s" % row_sql_id
                print("machine_sql: %s" % new_sql)

                self.conn_obj.update(new_sql)


            self.table_machine_num.event_flag = False
            for k, v in self.table_machine_num.item_new_data.items():
                if (k[0] + 1) % 2 == 0:
                    self.table_machine_num.tableWidget.item(*k).setBackground(QtGui.QColor('#E6E6E6'))
                else:
                    self.table_machine_num.tableWidget.item(*k).setBackground(QtGui.QColor('#EFEFEF'))

                self.table_machine_num.item_old_data[k] = v

            for k, v in self.table_machine_num.combobox_new_data.items():
                if (v[0] + 1) % 2 == 0:
                    k.setStyleSheet("QComboBox {background-color:#E6E6E6;}")
                else:
                    k.setStyleSheet("QComboBox {background-color:#EFEFEF;}")

                self.table_machine_num.combobox_old_data[k] = v

            self.table_machine_num.combobox_new_data = {}
            self.table_machine_num.item_new_data = {}



            ret = self.conn_obj.select("select * from machines")
            self.machine_type_num = []
            for i in range(len(ret)):
                ty = ret[i][1]
                self.machine_type_num.append(ty)

            # 清空分析界面机器类型下拉框内容
            self.machine_type_num = []
            self.comboBox_machine_type_num.clear()
            # 重新加载分析界面机器类型下拉框内容
            ret = self.conn_obj.select("select * from machines")
            for i in range(len(ret)):
                ty = ret[i][1]
                self.machine_type_num.append(ty)
            self.init_comboBox_machine_type_num()


            self.table_machine_num.event_flag = True

        except:
            traceback.print_exc()
        self.pushButton_machine_save.setStyleSheet(
            "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")

    def kit_save(self):
        self.pushButton_kit_save.setStyleSheet(
            "border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")
        try:
            # print("ssss: %s" % str(self.table_kit_type.item_new_data))
            if not self.table_kit_type.item_new_data:
                QtWidgets.QMessageBox.warning(self, "提示", "           未做修改         ")
                self.pushButton_kit_save.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
                return
            update_items = {}
            for k, v in self.table_kit_type.item_new_data.items():
                if self.table_kit_type.item_old_data[k] == v:
                    continue
                update_items[k] = v

            if not update_items:
                QtWidgets.QMessageBox.warning(self, "提示", "           未做修改         ")
                self.pushButton_kit_save.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
                return

            for k, v in update_items.items():
                if v == "":
                    QtWidgets.QMessageBox.warning(self, "提示", "           保存不能为空         ")
                    self.pushButton_kit_save.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
                    return

            # FIXME 可以在这里添加保存的数据限制

            ret = QtWidgets.QMessageBox.question(self, "提示", "确认保存修改",
                                                 QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                 QtWidgets.QMessageBox.Cancel)
            if ret == QtWidgets.QMessageBox.Cancel:
                self.pushButton_kit_save.setStyleSheet(
                    "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
                return

            update_data = {}
            for k, v in update_items.items():
                if isinstance(update_data.get(k[0]), dict):
                    update_data[k[0]][k[1]] = v
                else:
                    update_data[k[0]] = {}
                    update_data[k[0]][k[1]] = v

            kit_sql_id_index = self.table_kit_type.tableWidget.columnCount() - 1
            for k, v in update_data.items():
                row_sql_id = self.table_kit_type.tableWidget.item(k, kit_sql_id_index).text()
                new_sql = "update kits set "
                new_sql_1 = ""
                for k1, v1 in v.items():
                    new_sql_1 += self.conn_obj.kit_fields[k1] + "='%s'," % v1
                new_sql += new_sql_1.strip().strip(",")
                new_sql += " where id=%s" % row_sql_id
                print("kit_sql: %s" % new_sql)
                self.conn_obj.update(new_sql)


            self.table_kit_type.event_flag = False
            for k, v in self.table_kit_type.item_new_data.items():
                if (k[0] + 1) % 2 == 0:
                    self.table_kit_type.tableWidget.item(*k).setBackground(QtGui.QColor('#E6E6E6'))
                else:
                    self.table_kit_type.tableWidget.item(*k).setBackground(QtGui.QColor('#EFEFEF'))

                self.table_kit_type.item_old_data[k] = v

            self.table_kit_type.item_new_data = {}
            self.table_kit_type.event_flag = True

        except:
            traceback.print_exc()
        self.pushButton_kit_save.setStyleSheet(
            "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")

    def set_settings(self, obj_name):

        if obj_name == "pushButton_settings_1":
            self.stackedWidget_settings.setCurrentIndex(0)
            self.pushButton_settings_1.setStyleSheet(
                'background-color: #4a637c;font: 75 11pt "微软雅黑";border-radius:10px;color:#ffffff;')
        else:
            self.pushButton_settings_1.setStyleSheet(
                'background-color: #ffffff;font: 75 11pt "微软雅黑";border-radius:10px;color:#000000;')

        if obj_name == "pushButton_settings_2":
            self.stackedWidget_settings.setCurrentIndex(1)
            self.pushButton_settings_2.setStyleSheet(
                'background-color: #4a637c;font: 75 11pt "微软雅黑";border-radius:10px;color:#ffffff;')
        else:
            self.pushButton_settings_2.setStyleSheet(
                'background-color: #ffffff;font: 75 11pt "微软雅黑";border-radius:10px;color:#000000;')

    def set_select(self, obj_name):

        if obj_name == "pushButton_parse":
            self.stackedWidget.setCurrentIndex(0)
            self.pushButton_parse.setStyleSheet(constants.pushButton_parse_style2)
        else:
            self.pushButton_parse.setStyleSheet(constants.pushButton_parse_style1)

        if obj_name == "pushButton_history":
            self.stackedWidget.setCurrentIndex(1)
            self.pushButton_history.setStyleSheet(constants.pushButton_history_style2)
        else:
            self.pushButton_history.setStyleSheet(constants.pushButton_history_style1)

        if obj_name == "pushButton_upload_many":
            self.stackedWidget.setCurrentIndex(2)
            self.pushButton_upload_many.setStyleSheet(constants.pushButton_upload_many_style2)
        else:
            self.pushButton_upload_many.setStyleSheet(constants.pushButton_upload_many_style1)

        if obj_name == "pushButton_settings":
            self.stackedWidget.setCurrentIndex(3)
            self.pushButton_settings.setStyleSheet(constants.pushButton_settings_style2)
        else:
            self.pushButton_settings.setStyleSheet(constants.pushButton_settings_style1)

        if obj_name == "pushButton_support":
            self.stackedWidget.setCurrentIndex(4)
            self.pushButton_support.setStyleSheet(constants.pushButton_support_style2)
        else:
            self.pushButton_support.setStyleSheet(constants.pushButton_support_style1)

    def pushButton_input_clicked(self):

        self.pushButton_input.setStyleSheet(
            "border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "下机数据", ".",
                                                          "eds files(*.eds);;All Files(*)")
        self.pushButton_input.setStyleSheet(
            "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
        # print(file_name)
        if not file_name[0]:
            return
        try:
            self.data_file_name.setText(os.path.split(file_name[0])[1])
            machine_type = self.comboBox_machine_type_num.currentText()
            kit_type = self.comboBox_kits_type.currentText()
            resp = report.main(file_name[0], machine_type, kit_type, 3)
            if resp[0]["success"]:
                self.generate_word_file = resp[1]

                self.dict_data = {}
                for i in resp[0]["data"]:
                    self.dict_data[i["well"]] = i
                for obj in self.collect_buttons_obj():
                    obj = eval(obj)
                    try:
                        obj_name = obj.objectName()
                        if obj_name in self.dict_data.keys():
                            if self.dict_data[obj_name]["result"].strip() == "阴性":
                                obj.setStyleSheet(constants.ret_set_color2)
                            elif self.dict_data[obj_name]["result"].strip() == "异常":
                                obj.setStyleSheet(constants.ret_set_color3)
                            elif self.dict_data[obj_name]["result"].strip() == "无数据":
                                obj.setStyleSheet(constants.ret_set_color4)
                            elif self.dict_data[obj_name]["result"].strip() == "阳性":
                                obj.setStyleSheet(constants.ret_set_color5)
                            elif self.dict_data[obj_name]["result"].strip() == "纯合":
                                obj.setStyleSheet(constants.ret_set_color6)
                            elif self.dict_data[obj_name]["result"].strip() == "杂合":
                                obj.setStyleSheet(constants.ret_set_color7)
                            elif self.dict_data[obj_name]["result"].strip() == "野生":
                                obj.setStyleSheet(constants.ret_set_color8)
                        else:
                            obj.setStyleSheet(constants.ret_set_color4)
                    except Exception as e:
                        obj.setStyleSheet(constants.ret_set_color3)
                        raise(e)
            else:
                QtWidgets.QMessageBox.warning(self, "提示", "           下机数据加载错误        ")
        except Exception as e:
            raise(e)

    def example_info(self):
        self.pushButton_example_info.setStyleSheet(
            "border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "样本信息", ".",
                                                          "All Files(*);;Txt files(*.txt)")
        self.pushButton_example_info.setStyleSheet(
            "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
        if not file_name[0]:

            return

        # FIXME 待开发

    def generate_word(self):

        self.pushButton_generate_word.setStyleSheet(
            "border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")

        if not self.generate_word_file:
            QtWidgets.QMessageBox.warning(self, "提示", "           需要先加载下机数据         ")
            self.pushButton_generate_word.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")
            return
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, "生成报告", ".", "xls files(*.xls);;xlsx files(*.xlsx);;All Files(*)")
        self.pushButton_generate_word.setStyleSheet("color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")

        if not file_name[0]:
            QtWidgets.QMessageBox.warning(self, "提示", "           未输入文件保存位置         ")
            return
        try:
            print(self.generate_word_file)
            with open(self.generate_word_file, 'rb') as fsrc:
                with open(file_name[0], 'wb') as fdst:
                    shutil.copyfileobj(fsrc, fdst)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "提示", "%s" % e)
            traceback.print_exc()

    def upload_word(self):
        self.pushButton_upload_word.setStyleSheet(
            "border-radius:10px;background-color: rgb(0, 85, 127);color: rgb(255, 255, 255);")

        QtWidgets.QMessageBox.information(self, "提示", "           开发中         ")
        self.pushButton_upload_word.setStyleSheet(
            "color: rgb(0, 0, 0);background-color: rgb(255, 255, 255);border-radius:10px;")

    def collect_buttons_obj(self):

        columns = range(1, 13)
        rows = list("ABCDEFGH")
        objs = [("self." + i + str(j)) for i in rows for j in columns]
        # print(objs)

        return objs

    def set_checkbox(self):
        self.checkBox_fam.stateChanged.connect(self.set_fam_checkebox)
        self.checkBox_fam.setChecked(True)
        self.checkBox_vic.stateChanged.connect(self.set_vic_checkebox)
        self.checkBox_vic.setChecked(True)
        self.checkBox_rox.stateChanged.connect(self.set_rox_checkbox)
        self.checkBox_rox.setChecked(True)

    def set_fam_checkebox(self):
        if self.checkBox_fam.isChecked():
            self.fam_selected = True
        else:
            self.fam_selected = False
        if self.checkBox_flag < 3:
            self.checkBox_flag += 1
        else:
            self.start_time()

    def set_vic_checkebox(self):
        if self.checkBox_vic.isChecked():
            self.vic_selected = True
        else:
            self.vic_selected = False
        if self.checkBox_flag < 3:
            self.checkBox_flag += 1
        else:
            self.start_time()

    def set_rox_checkbox(self):
        if self.checkBox_rox.isChecked():
            self.rox_selected = True
        else:
            self.rox_selected = False
        if self.checkBox_flag < 3:
            self.checkBox_flag += 1
        else:
            self.start_time()
        # print("self.checkBox_flag: %s" % self.checkBox_flag)

    def init_data(self):
        self.fam_temp = []
        self.vic_temp = []
        self.rox_temp = []
        self.fam_index = 0  # 列表索引
        self.vic_index = 0  # 列表索引
        self.rox_index = 0  # 列表索引

    def show_time(self):
        if getattr(self, "fam_li", False) and  getattr(self, "vic_li", False) and getattr(self, "rox_li", False):
            if self.fam_index < len(self.fam_li):
                d1 = self.fam_li[self.fam_index]
                self.fam_temp.append(d1)
                self.fam_index += 1
            if self.vic_index < len(self.vic_li):
                d2 = self.vic_li[self.vic_index]
                self.vic_temp.append(d2)
                self.vic_index += 1
            if self.rox_index < len(self.rox_li):
                d3 = self.rox_li[self.rox_index]
                self.rox_temp.append(d3)
                self.rox_index += 1

            # self.dr.axes.clear()
            flag = 0
            flag1 = []
            if self.fam_selected:
                flag1.append((self.fam_index, len(self.fam_li)))
                self.dr.axes.plot(list(range(len(self.fam_temp))), self.fam_temp, color="#8fefd6")
            if self.vic_selected:
                flag1.append((self.vic_index, len(self.vic_li)))
                self.dr.axes.plot(list(range(len(self.vic_temp))), self.vic_temp, color="#f9938f")
            if self.rox_selected:
                flag1.append((self.rox_index, len(self.rox_li)))
                self.dr.axes.plot(list(range(len(self.rox_temp))), self.rox_temp, color="#000000")

            # self.dr.set_axes()
            self.dr.axes.set_title(self.now_button_name)

            # 坐标轴刻度的倾斜放在作完图后在一次性调整
            # main_width = self.geometry().size().width()
            # #
            # if main_width < 1500:
            #     self.dr.set_xticks(rotation=90)
            # else:
            self.dr.set_xticks()

            self.dr.fig.canvas.draw()
            for k, v in flag1:
                if k >= v:
                    flag += 1
            if flag == self.select_count:
                self.end_time()

    def end_time(self):
        self.timer.stop()
        # 画完成图片后，最后调整下界面
        self.dr.set_axes()
        main_width = self.geometry().size().width()
        if main_width < 1500:
            self.dr.set_xticks(rotation=90)
        else:
            self.dr.set_xticks()
        self.dr.fig.canvas.draw()

        self.init_data()

    def start_time(self):
        self.dr.axes.cla()
        self.dr.fig.canvas.draw()
        # 一次性添加网格线
        self.dr.axes.grid(True, linestyle="--", alpha=0.5, c="#808080")
        self.init_data()
        self.select_count = len([i for i in [self.fam_selected, self.vic_selected, self.rox_selected] if i])
        self.timer.start(1)  # 每隔一毫秒执行一次绘图函数 showTime

    def draw_pic(self, button_obj_name):
        try:
            self.now_button_name = button_obj_name
            data = self.dict_data[button_obj_name]
            ret = {i["name"]: i["rn"] for i in data["data"]}
            self.fam_li = [float(i) for i in ret["FAM"]]
            self.vic_li = [float(i) for i in ret["VIC"]]
            self.rox_li = [float(i) for i in ret["ROX"]]

            # print("id: %s" % id(self.dr))
            self.start_time()
        except Exception as e:
            traceback.print_exc()

    def clear_layout_widgets(self, layout):
        if not layout.count():
            return
        for i in reversed(range(self.horizontalLayout_1110.count())):
            self.horizontalLayout_1110.itemAt(i).widget().setParent(None)

    def buttons_event(self):
        self.A1.clicked.connect(lambda: self.draw_pic(self.A1.objectName()))
        self.A2.clicked.connect(lambda: self.draw_pic(self.A2.objectName()))
        self.A3.clicked.connect(lambda: self.draw_pic(self.A3.objectName()))
        self.A4.clicked.connect(lambda: self.draw_pic(self.A4.objectName()))
        self.A5.clicked.connect(lambda: self.draw_pic(self.A5.objectName()))
        self.A6.clicked.connect(lambda: self.draw_pic(self.A6.objectName()))
        self.A7.clicked.connect(lambda: self.draw_pic(self.A7.objectName()))
        self.A8.clicked.connect(lambda: self.draw_pic(self.A8.objectName()))
        self.A9.clicked.connect(lambda: self.draw_pic(self.A9.objectName()))
        self.A10.clicked.connect(lambda: self.draw_pic(self.A10.objectName()))
        self.A11.clicked.connect(lambda: self.draw_pic(self.A11.objectName()))
        self.A12.clicked.connect(lambda: self.draw_pic(self.A12.objectName()))
        self.B1.clicked.connect(lambda: self.draw_pic(self.B1.objectName()))
        self.B2.clicked.connect(lambda: self.draw_pic(self.B2.objectName()))
        self.B3.clicked.connect(lambda: self.draw_pic(self.B3.objectName()))
        self.B4.clicked.connect(lambda: self.draw_pic(self.B4.objectName()))
        self.B5.clicked.connect(lambda: self.draw_pic(self.B5.objectName()))
        self.B6.clicked.connect(lambda: self.draw_pic(self.B6.objectName()))
        self.B7.clicked.connect(lambda: self.draw_pic(self.B7.objectName()))
        self.B8.clicked.connect(lambda: self.draw_pic(self.B8.objectName()))
        self.B9.clicked.connect(lambda: self.draw_pic(self.B9.objectName()))
        self.B10.clicked.connect(lambda: self.draw_pic(self.B10.objectName()))
        self.B11.clicked.connect(lambda: self.draw_pic(self.B11.objectName()))
        self.B12.clicked.connect(lambda: self.draw_pic(self.B12.objectName()))
        self.C1.clicked.connect(lambda: self.draw_pic(self.C1.objectName()))
        self.C2.clicked.connect(lambda: self.draw_pic(self.C2.objectName()))
        self.C3.clicked.connect(lambda: self.draw_pic(self.C3.objectName()))
        self.C4.clicked.connect(lambda: self.draw_pic(self.C4.objectName()))
        self.C5.clicked.connect(lambda: self.draw_pic(self.C5.objectName()))
        self.C6.clicked.connect(lambda: self.draw_pic(self.C6.objectName()))
        self.C7.clicked.connect(lambda: self.draw_pic(self.C7.objectName()))
        self.C8.clicked.connect(lambda: self.draw_pic(self.C8.objectName()))
        self.C9.clicked.connect(lambda: self.draw_pic(self.C9.objectName()))
        self.C10.clicked.connect(lambda: self.draw_pic(self.C10.objectName()))
        self.C11.clicked.connect(lambda: self.draw_pic(self.C11.objectName()))
        self.C12.clicked.connect(lambda: self.draw_pic(self.C12.objectName()))
        self.D1.clicked.connect(lambda: self.draw_pic(self.D1.objectName()))
        self.D2.clicked.connect(lambda: self.draw_pic(self.D2.objectName()))
        self.D3.clicked.connect(lambda: self.draw_pic(self.D3.objectName()))
        self.D4.clicked.connect(lambda: self.draw_pic(self.D4.objectName()))
        self.D5.clicked.connect(lambda: self.draw_pic(self.D5.objectName()))
        self.D6.clicked.connect(lambda: self.draw_pic(self.D6.objectName()))
        self.D7.clicked.connect(lambda: self.draw_pic(self.D7.objectName()))
        self.D8.clicked.connect(lambda: self.draw_pic(self.D8.objectName()))
        self.D9.clicked.connect(lambda: self.draw_pic(self.D9.objectName()))
        self.D10.clicked.connect(lambda: self.draw_pic(self.D10.objectName()))
        self.D11.clicked.connect(lambda: self.draw_pic(self.D11.objectName()))
        self.D12.clicked.connect(lambda: self.draw_pic(self.D12.objectName()))
        self.E1.clicked.connect(lambda: self.draw_pic(self.E1.objectName()))
        self.E2.clicked.connect(lambda: self.draw_pic(self.E2.objectName()))
        self.E3.clicked.connect(lambda: self.draw_pic(self.E3.objectName()))
        self.E4.clicked.connect(lambda: self.draw_pic(self.E4.objectName()))
        self.E5.clicked.connect(lambda: self.draw_pic(self.E5.objectName()))
        self.E6.clicked.connect(lambda: self.draw_pic(self.E6.objectName()))
        self.E7.clicked.connect(lambda: self.draw_pic(self.E7.objectName()))
        self.E8.clicked.connect(lambda: self.draw_pic(self.E8.objectName()))
        self.E9.clicked.connect(lambda: self.draw_pic(self.E9.objectName()))
        self.E10.clicked.connect(lambda: self.draw_pic(self.E10.objectName()))
        self.E11.clicked.connect(lambda: self.draw_pic(self.E11.objectName()))
        self.E12.clicked.connect(lambda: self.draw_pic(self.E12.objectName()))
        self.F1.clicked.connect(lambda: self.draw_pic(self.F1.objectName()))
        self.F2.clicked.connect(lambda: self.draw_pic(self.F2.objectName()))
        self.F3.clicked.connect(lambda: self.draw_pic(self.F3.objectName()))
        self.F4.clicked.connect(lambda: self.draw_pic(self.F4.objectName()))
        self.F5.clicked.connect(lambda: self.draw_pic(self.F5.objectName()))
        self.F6.clicked.connect(lambda: self.draw_pic(self.F6.objectName()))
        self.F7.clicked.connect(lambda: self.draw_pic(self.F7.objectName()))
        self.F8.clicked.connect(lambda: self.draw_pic(self.F8.objectName()))
        self.F9.clicked.connect(lambda: self.draw_pic(self.F9.objectName()))
        self.F10.clicked.connect(lambda: self.draw_pic(self.F10.objectName()))
        self.F11.clicked.connect(lambda: self.draw_pic(self.F11.objectName()))
        self.F12.clicked.connect(lambda: self.draw_pic(self.F12.objectName()))
        self.G1.clicked.connect(lambda: self.draw_pic(self.G1.objectName()))
        self.G2.clicked.connect(lambda: self.draw_pic(self.G2.objectName()))
        self.G3.clicked.connect(lambda: self.draw_pic(self.G3.objectName()))
        self.G4.clicked.connect(lambda: self.draw_pic(self.G4.objectName()))
        self.G5.clicked.connect(lambda: self.draw_pic(self.G5.objectName()))
        self.G6.clicked.connect(lambda: self.draw_pic(self.G6.objectName()))
        self.G7.clicked.connect(lambda: self.draw_pic(self.G7.objectName()))
        self.G8.clicked.connect(lambda: self.draw_pic(self.G8.objectName()))
        self.G9.clicked.connect(lambda: self.draw_pic(self.G9.objectName()))
        self.G10.clicked.connect(lambda: self.draw_pic(self.G10.objectName()))
        self.G11.clicked.connect(lambda: self.draw_pic(self.G11.objectName()))
        self.G12.clicked.connect(lambda: self.draw_pic(self.G12.objectName()))
        self.H1.clicked.connect(lambda: self.draw_pic(self.H1.objectName()))
        self.H2.clicked.connect(lambda: self.draw_pic(self.H2.objectName()))
        self.H3.clicked.connect(lambda: self.draw_pic(self.H3.objectName()))
        self.H4.clicked.connect(lambda: self.draw_pic(self.H4.objectName()))
        self.H5.clicked.connect(lambda: self.draw_pic(self.H5.objectName()))
        self.H6.clicked.connect(lambda: self.draw_pic(self.H6.objectName()))
        self.H7.clicked.connect(lambda: self.draw_pic(self.H7.objectName()))
        self.H8.clicked.connect(lambda: self.draw_pic(self.H8.objectName()))
        self.H9.clicked.connect(lambda: self.draw_pic(self.H9.objectName()))
        self.H10.clicked.connect(lambda: self.draw_pic(self.H10.objectName()))
        self.H11.clicked.connect(lambda: self.draw_pic(self.H11.objectName()))
        self.H12.clicked.connect(lambda: self.draw_pic(self.H12.objectName()))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
