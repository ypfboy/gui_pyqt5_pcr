import sys
from PyQt5.QtWidgets import *


# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import Qt, QDate, QTime, QDateTime, QTimer

class Widget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("层叠窗口部件演示")
        self.cbBox = QComboBox()
        self.cbBox.addItems(["页面1", "页面2"])
        self.textEdit = QTextEdit()
        # self.textEdit.setFixedHeight(200)
        self.textEdit.setText(" Input something here:")
        self.textEdit.selectAll()
        self.stackedWidget = QStackedWidget()

        self.stackedWidget.addWidget(self.create_widget1())
        self.stackedWidget.addWidget(self.textEdit)
        layout = QVBoxLayout()
        layout.addWidget(self.cbBox)
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)
        self.resize(250, 50)
        # 下拉框选择改变时 就改变 层叠窗口部件的当前页面
        self.cbBox.currentIndexChanged[int].connect(self.on_cbBox_currentIndexChanged)

        self.stackedWidget.currentChanged[int].connect(self.on_currentChanged)

    def create_widget1(self):
        # 创建自定义复合窗口部件

        widget = QWidget()  # step1
        gLayout = QGridLayout()

        label1 = QLabel("姓名:")
        lineEdit1 = QLineEdit()
        label1.setBuddy(lineEdit1)
        label2 = QLabel("性别:")
        buttonGroup = QButtonGroup()
        radioButton1 = QRadioButton("男")
        radioButton2 = QRadioButton("女")
        radioButton2.setChecked(True)
        # 同一button group 或同一 父窗体的 为一个分组，多选一
        buttonGroup.addButton(radioButton1)
        buttonGroup.addButton(radioButton2)
        gLayout.addWidget(label1, 0, 0)
        gLayout.addWidget(lineEdit1, 0, 1, 1, 2)
        gLayout.addWidget(label2, 1, 0)
        gLayout.addWidget(radioButton1, 1, 1)
        gLayout.addWidget(radioButton2, 1, 2)
        widget.setLayout(gLayout)  # step2
        return widget

    def on_cbBox_currentIndexChanged(self, index):
        '''下拉框选择改变时 就改变 层叠窗口部件的当前页面'''
        self.stackedWidget.setCurrentIndex(index)

    def on_currentChanged(self, index):
        print("current tab index:", index)
        print("current tab index:", self.stackedWidget.currentIndex())
        print("current tab widget:", self.stackedWidget.currentWidget())
        print("tab count", self.stackedWidget.count())
        # self.stackedWidget.setCurrentIndex(1)  #可通过代码设定当前tab
        # self.stackedWidget.setTabEnabled (self, int index, bool)  #disable Tab


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wg = Widget()
    wg.show()
    sys.exit(app.exec_())