import sys
import os
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        dir_path = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(dir_path, "ankitube.ui")
        uic.loadUi(ui_path, self)

        self.file = self.findChild(QMenu, "menu_file")
        self.help = self.file.addAction("Help")
        self.file.triggered[QAction].connect(self.showDialog())

        self.exec()

    def showDialog(self, q):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Ankitube is designed to allow download of YouTube video clips easily for \
                        educational purposes. Simply copy the URL into the text box, enter the \
                        clip start and end times. FFMpeg is a required dependency to allow .mp4 to \
                        .webm conversion to ensure anki video player compatability.\n \n")
        msgBox.setWindowTitle("Help")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = msgBox.exec()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())