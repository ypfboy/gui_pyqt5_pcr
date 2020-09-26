from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

#方法1
class mylineedit(QLineEdit):
    clicked=pyqtSignal()    #定义clicked信号
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button()==Qt.LeftButton:
            self.clicked.emit()     #发送clicked信号

class Wind(QDialog):
    clicked=pyqtSignal()
    def __init__(self):
        super().__init__()
        self.lnd=mylineedit()
        self.edit=QLineEdit()
        self.edit.installEventFilter(self)   #方法2(1)

        vb=QVBoxLayout()
        vb.addWidget(self.lnd)
        vb.addWidget(self.edit)
        self.setLayout(vb)

        self.lnd.clicked.connect(self.showData)
        self.clicked.connect(self.showData)     #该clicked信号是W1的信号而非edit的信号，但可以实现焦点落到edit时触发信号

    def showData(self):
        print('sssss')


# 方法2(2)
"""
def eventFilter(self, widget, event):
    if widget == self.edit:
        if event.type() == QEvent.FocusOut:
            pass
        elif event.type() == QEvent.FocusIn:
            self.clicked.emit()     #当焦点再次落到edit输入框时，发送clicked信号出去
        else:
            pass
    return False

def showData(self):
    print('ok')

"""
if __name__=="__main__":
    app=QApplication(sys.argv)
    w=Wind()
    w.show()
    sys.exit(app.exec_())

