import sys

from PyQt5 import QtWidgets
from fw_pcr.main import MyMainWindow
from views.startFace import StartFace


def pcr_start():

    app = QtWidgets.QApplication(sys.argv)
    start_face = StartFace()
    start_face.show()
    app.processEvents()
    window = MyMainWindow()
    start_face.finsh(window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    pcr_start()
