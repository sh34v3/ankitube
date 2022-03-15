import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        dir_path = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(dir_path, "ankitube.ui")
        uic.loadUi(ui_path, self)

        img_path = os.path.join(dir_path, 'sandstone.jpg')
        self.imLabel = self.findChild(QLabel, "label")
        self.pixmap = QPixmap(img_path)
        self.imLabel.setPixmap(self.pixmap)

        self.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())