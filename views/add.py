# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QInputDialog

from PyQt5 import QtCore, QtGui, QtWidgets
from views.uiAdd import Ui_Form

# class Ui_Form(object):
#     def setupUi(self, Form):
#         Form.setObjectName("Form")
#         Form.setEnabled(True)
#         Form.resize(446, 170)
#         Form.setMinimumSize(QtCore.QSize(446, 170))
#         Form.setMaximumSize(QtCore.QSize(446, 170))
#         Form.setStyleSheet("background-color: rgb(220, 245, 255);")
#         self.gridLayout = QtWidgets.QGridLayout(Form)
#         self.gridLayout.setContentsMargins(0, 0, 0, 0)
#         self.gridLayout.setSpacing(0)
#         self.gridLayout.setObjectName("gridLayout")
#         self.frame = QtWidgets.QFrame(Form)
#         self.frame.setMaximumSize(QtCore.QSize(424, 100))
#         self.frame.setStyleSheet("")
#         self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame.setObjectName("frame")
#         self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
#         self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
#         self.gridLayout_2.setSpacing(0)
#         self.gridLayout_2.setObjectName("gridLayout_2")
#         self.lineEdit_4 = QtWidgets.QLineEdit(self.frame)
#         self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
#         self.lineEdit_4.setObjectName("lineEdit_4")
#         self.gridLayout_2.addWidget(self.lineEdit_4, 1, 1, 1, 1)
#         self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
#         self.lineEdit_3.setStyleSheet("")
#         self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
#         self.lineEdit_3.setObjectName("lineEdit_3")
#         self.gridLayout_2.addWidget(self.lineEdit_3, 0, 1, 1, 1)
#         self.lineEdit = QtWidgets.QLineEdit(self.frame)
#         self.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
#         self.lineEdit.setStyleSheet("border:none;")
#         self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
#         self.lineEdit.setObjectName("lineEdit")
#         self.gridLayout_2.addWidget(self.lineEdit, 0, 0, 1, 1)
#         self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
#         self.lineEdit_2.setFocusPolicy(QtCore.Qt.NoFocus)
#         self.lineEdit_2.setStyleSheet("border:none;")
#         self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
#         self.lineEdit_2.setObjectName("lineEdit_2")
#         self.gridLayout_2.addWidget(self.lineEdit_2, 1, 0, 1, 1)
#         self.gridLayout_2.setColumnStretch(0, 1)
#         self.gridLayout_2.setColumnStretch(1, 3)
#         self.gridLayout_2.setRowStretch(0, 1)
#         self.gridLayout_2.setRowStretch(1, 3)
#         self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
#         self.frame_2 = QtWidgets.QFrame(Form)
#         self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_2.setObjectName("frame_2")
#         self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         self.pushButton = QtWidgets.QPushButton(self.frame_2)
#         self.pushButton.setMinimumSize(QtCore.QSize(70, 0))
#         self.pushButton.setMaximumSize(QtCore.QSize(70, 16777215))
#         self.pushButton.setStyleSheet("")
#         self.pushButton.setObjectName("pushButton")
#         self.horizontalLayout.addWidget(self.pushButton)
#         self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
#         self.pushButton_2.setMinimumSize(QtCore.QSize(70, 0))
#         self.pushButton_2.setMaximumSize(QtCore.QSize(70, 16777215))
#         self.pushButton_2.setStyleSheet("")
#         self.pushButton_2.setObjectName("pushButton_2")
#         self.horizontalLayout.addWidget(self.pushButton_2)
#         self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
#
#         self.retranslateUi(Form)
#         QtCore.QMetaObject.connectSlotsByName(Form)
#
#     def retranslateUi(self, Form):
#         _translate = QtCore.QCoreApplication.translate
#         Form.setWindowTitle(_translate("Form", "新增"))
#         self.lineEdit.setText(_translate("Form", "机器编号"))
#         self.lineEdit_2.setText(_translate("Form", "机器类型"))
#         self.pushButton.setText(_translate("Form", "确定"))
#         self.pushButton_2.setText(_translate("Form", "取消"))

class MyMainForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        # 禁用关闭按钮
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        # 只显示关闭
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 隐藏整个头部
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.add = Ui_Form()
        self.add.setupUi(self)
        self.add.pushButton.clicked.connect(self.sour_add)
        self.add.pushButton_2.clicked.connect(self.cancel)
        self.add.comboBox.addItem("7500-1")
        self.add.comboBox.addItem("7500-2")
        self.add.comboBox_2.addItem("7500")
        self.add.comboBox_2.addItem("7500")


    def sour_add(self):
        self.add_li = [self.add.comboBox.currentText(), self.add.comboBox_2.currentText()]
        # print(self.add_li)
        self.close()

    def cancel(self):
        self.add_li = []
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()

    """
    aa = QtWidgets.QDialog()
    myWin = Ui_Form()
    myWin.setupUi(aa)
    aa.show()
    """
    sys.exit(app.exec_())