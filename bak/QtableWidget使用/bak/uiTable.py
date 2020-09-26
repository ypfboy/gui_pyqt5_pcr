import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QHeaderView, QItemDelegate, QApplication


class ReLineEdit(QtWidgets.QLineEdit):

    def leaveEvent(self, event):
        self.setStyleSheet("border:none")
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet("color:#0055ff;border:none")

    def mouseMoveEvent(self, mouse_event):
        '''
        重写鼠标的左键右键选中
        :param mouse_event:
        :return:
        '''
        if mouse_event.buttons == QtCore.Qt.LeftButton or mouse_event.buttons() == QtCore.Qt.RightButton:
            return


    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        return None

    def keyPressEvent(self, key_event):
        '''
        重写键盘的全选，复制粘贴
        :param key_event:
        :return:
        '''
        if key_event == QtGui.QKeySequence.SelectAll:  # 禁止全选
            return
        if key_event == QtGui.QKeySequence.Paste:  # 禁止粘贴
            return
        if key_event == QtGui.QKeySequence.Copy:  # 禁止复制
            return

class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):

        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class Table(object):

    def initUI(self, parent):
        self.grid = QtWidgets.QGridLayout(parent)
        self.tableWidget = QtWidgets.QTableWidget(parent)
        self.tableWidget.setStyleSheet("QTableWidget {\n"
                                       "    background-color:white;    \n"
                                       "    border:1px solid #E0DDDC;   \n"
                                       "}\n"
                                       "QHeaderView::section {\n"
                                       "    background-color:white;    \n"
                                       "    border:1px solid #E0DDDC;  \n"
                                       "    height:20px;               \n"
                                       "}\n"
                                       "QTableView{\n"
                                       "    color: rgb(0, 0, 0);\n"
                                       "    border: 1px solid #E0DDDC;        \n"
                                       "}\n"
                                       "\n"
                                       "")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        # 列宽自动分配
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 行高自动分配
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置纵向表头隐藏
        self.tableWidget.verticalHeader().setVisible(False)
        # 设置纵向表头宽度
        # self.tableWidget.verticalHeader().setFixedWidth(20)
        # 　设置横向表头高度
        self.tableWidget.horizontalHeader().setFixedHeight(40)
        # 设置表头内容
        list = ['机器编号', '机器类型', '操作']
        self.tableWidget.setHorizontalHeaderLabels(list)
        # 设置表头不可点击
        self.tableWidget.horizontalHeader().setSectionsClickable(False)
        # 设置行高使用固定值
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.grid.addWidget(self.tableWidget)


    def create_row(self):
        newItem = QtWidgets.QTableWidgetItem("7500-1")
        self.tableWidget.setItem(0, 0, newItem)

        comBox = QtWidgets.QComboBox()  # 新建一个下拉组件
        comBox.addItem("7500")
        comBox.addItem("7600")
        # comBox.currentIndexChanged.connect(self.comboxSelect)
        self.tableWidget.setCellWidget(0, 1, comBox)

        self.frame1 = QtWidgets.QWidget()
        # self.frame1.setMaximumWidth(80)
        self.hboxlayout = QtWidgets.QHBoxLayout(self.frame1)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(0)

        line = ReLineEdit("修改")  #
        line.setStyleSheet("border:none;")
        line.setAlignment(QtCore.Qt.AlignRight)
        line.setMinimumHeight(40)
        line.setFocusPolicy(QtCore.Qt.NoFocus)

        line1 = QtWidgets.QLineEdit("/")
        line1.setStyleSheet("border:none;")
        line1.setMaximumWidth(10)
        line1.setAlignment(QtCore.Qt.AlignCenter)
        line1.setMinimumHeight(40)
        line1.setFocusPolicy(QtCore.Qt.NoFocus)

        line2 = ReLineEdit("删除")
        line2.setStyleSheet("border:none;")
        line2.setMinimumHeight(40)
        # 设置不可编辑
        line2.setFocusPolicy(QtCore.Qt.NoFocus)

        # searchBtn.setStyleSheet("QPushButton{margin:3px};")
        self.hboxlayout.addWidget(line)
        self.hboxlayout.addWidget(line1)
        self.hboxlayout.addWidget(line2)
        # searchBtn.clicked.connect(self.butClick)
        self.tableWidget.setCellWidget(0, 2, self.frame1)  #
        # 设置某一列不可编辑
        # self.tableWidget.setItemDelegateForColumn(0,EmptyDelegate(self.tableWidget)) # 设置第二列不可编辑

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QtWidgets.QWidget()
    win = Table()
    win.initUI(main_window)
    main_window.show()
    sys.exit(app.exec_())

