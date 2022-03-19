#        ___  __                    __                     __                 ___       __   ___ 
#  |\/| |__  /  ` |__|  /\  |\ | | /  `  /\  |        /\  |  \ \  /  /\  |\ |  |   /\  / _` |__  
#  |  | |___ \__, |  | /~~\ | \| | \__, /~~\ |___    /~~\ |__/  \/  /~~\ | \|  |  /~~\ \__> |___ 
                                                                                               
# contact: buginformation@protonmail.ch

#--NOTES--

# TODO
# Implement a QtThread class that will allow me to dynamically update the progress bar: https://www.youtube.com/watch?v=ivcxZSHL7jM&ab_channel=VFXPipeline
# Implement a way to determine progress of ffmpeg from stdout: https://www.youtube.com/watch?v=-z1pvtMOTmg&ab_channel=FlorianDahlitz
# ----if I can get stdout dynamically from ffmpeg, I simply need to take the time=00:00:xx field from its output
# ---- time in seconds/(clip_end - clip_start) will give completion percentage

# -*- coding: utf-8 -*-

# import random for unique filenames
from random import randint

# #import os library for making a directory
import os
# #import subprocess for callimg ffmpeg
import subprocess

# #import web scraping libraries
from pytube import YouTube

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets

#where to save media
SAVE_PATH = os.getcwd()+"/media/"
SCRIPT_DIR = os.getcwd()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 198)
        MainWindow.setMinimumSize(QtCore.QSize(700, 198))
        MainWindow.setMaximumSize(QtCore.QSize(700, 198))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.link_textbox = QtWidgets.QLineEdit(self.centralwidget)
        self.link_textbox.setGeometry(QtCore.QRect(90, 20, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.link_textbox.setFont(font)
        self.link_textbox.setObjectName("link_textbox")
        self.start_time = QtWidgets.QSpinBox(self.centralwidget)
        self.start_time.setGeometry(QtCore.QRect(220, 70, 43, 24))
        self.start_time.setMaximum(599)
        self.start_time.setObjectName("start_time")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(180, 70, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(280, 70, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.end_time = QtWidgets.QSpinBox(self.centralwidget)
        self.end_time.setGeometry(QtCore.QRect(310, 70, 43, 24))
        self.end_time.setMinimum(1)
        self.end_time.setMaximum(600)
        self.end_time.setProperty("value", 10)
        self.end_time.setObjectName("end_time")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(370, 70, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(460, 70, 16, 21))
        self.checkBox.setText("")
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.get_video_button = QtWidgets.QPushButton(self.centralwidget, clicked = lambda:self.getClip()) #clicked functionality needs to be added like this
        self.get_video_button.setGeometry(QtCore.QRect(530, 20, 151, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.get_video_button.setFont(font)
        self.get_video_button.setObjectName("get_video_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 71, 31))
        self.label.setObjectName("label")
        # self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        # self.progress_bar.setGeometry(QtCore.QRect(10, 110, 671, 31))
        # self.progress_bar.setProperty("value", 0)
        # self.progress_bar.setInvertedAppearance(False)
        # self.progress_bar.setObjectName("progress_bar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 20))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_help = QtWidgets.QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.menu_file.addAction(self.action_help)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.action_help.triggered.connect(lambda: self.showHelpDialog("Help")) 
        #^
        #have to use a lambda function if you want to pass a parameter within this framework
        #thank being said, I put a parameter in here for my own educational purposes, not because I needed to

        self.statusbar.showMessage("Ready...")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Clip times (in seconds):"))
        self.label_3.setText(_translate("MainWindow", "Start:"))
        self.label_4.setText(_translate("MainWindow", "End:"))
        self.label_5.setText(_translate("MainWindow", "Keep audio?"))
        self.get_video_button.setText(_translate("MainWindow", "Get Video"))
        self.label.setText(_translate("MainWindow", "Enter Link:"))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.action_help.setText(_translate("MainWindow", "Info"))

    def getClip(self):
        link: str = self.link_textbox.text()
        print(link)

        try:
            self.statusbar.showMessage("Getting YouTube Stream...")
            self.statusbar.repaint()
            yt = YouTube(link)
        except:
            self.statusbar.showMessage("!!!Connection Error: Double check link is valid...")
            self.statusbar.repaint()
            return
        # self.progress_bar.setValue(25)
        #get mp4 StreamQuery
        yt_streams = yt.streams.filter(file_extension='mp4')

        #get highest resolution Stream available in mp4files
        download_video = yt_streams.get_highest_resolution()

        self.statusbar.showMessage("Downloading video...")
        self.statusbar.repaint()
        # self.progress_bar.setValue(50)
        # downloading video
        download_video.download(output_path=SAVE_PATH)

        clip_start: int = int(self.start_time.text())
        clip_end: int = int(self.end_time.text())
        clip = self.clipencode(clip_start, clip_end, download_video.default_filename)

        # self.progress_bar.setValue(100)

        self.statusbar.showMessage("Done!")
        self.statusbar.repaint()

    #extract a clip from a video file by callimg ffmpeg
    def clipencode(self, start_time: int, end_time: int, infile_video: str):
        os.chdir(SAVE_PATH) # change working directory to media temp directory

        infile: str = str(infile_video)
        infile: str = str('\"'+infile+'\"')

        uniquename = ""
        for ch in infile_video:
            if len(uniquename) > 20:
                break
            elif randint(0, 1):
                uniquename = uniquename + chr(randint(65, 90))
            else:
                uniquename = uniquename + chr(randint(97, 122))

        uniquename = uniquename+".webm"

        print(uniquename)

        if self.checkBox.isChecked():
            self.statusbar.showMessage("Extracting clip....")
            self.statusbar.repaint()
            #subprocess.call(str('ffmpeg -i '+infile_video+' -c:v libvpx-vp9 -b:v 2M -pass 1 -an -f null /dev/null && \ '))
            subprocess.call([
                'ffmpeg',                   # call ffmpeg
                '-ss', str(start_time),          # our clip starts here
                '-i', infile_video,         # this is the video to be converted
                '-t', str(end_time - start_time), #how long our clip is
                '-threads', '4',            # use 4 threads for the video conversion
                '-c:v', 'libvpx-vp9',       # c[odec]:v[ideo] - we use libvpx cause we want webm
                '-c:a', 'libvorbis',        # c[odec]:a[udio] - this is the one everyone else was using
                '-b:v',  '400k',            # reccomended video bitrate
                '-b:a', '192k',             # reccomended audio bitrate
                '-deadline', 'good',    # setting for quality vs. speed (best, good, realtime (fastest)); boundry for quality vs. time set the following settings
                '-qmin', '0',               # quality minimum boundry. (lower means better)
                '-qmax', '50',              # quality maximum boundry (higher means worse)
                uniquename               # file to be written out
            ])
        else:
            self.statusbar.showMessage("Extracting clip with no audio....")
            self.statusbar.repaint()
             #subprocess.call(str('ffmpeg -i '+infile_video+' -c:v libvpx-vp9 -b:v 2M -pass 1 -an -f null /dev/null && \ '))
            subprocess.call([
                'ffmpeg',                   # call ffmpeg
                '-an',                      #remove all audio streams
                '-ss', str(start_time),          # our clip starts here
                '-i', infile_video,         # this is the video to be converted
                '-t', str(end_time - start_time), #how long our clip is
                '-threads', '4',            # use 4 threads for the video conversion
                '-c:v', 'libvpx-vp9',       # c[odec]:v[ideo] - we use libvpx cause we want webm
                '-b:v',  '400k',            # reccomended video bitrate
                '-deadline', 'good',    # setting for quality vs. speed (best, good, realtime (fastest)); boundry for quality vs. time set the following settings
                '-qmin', '0',               # quality minimum boundry. (lower means better)
                '-qmax', '50',              # quality maximum boundry (higher means worse)
                uniquename               # file to be written out
            ])

    def showHelpDialog(self, tl):
        icon = QtWidgets.QMessageBox.Information

        #this is the easiest way to do a multi line string with easily understood formatting
        text =("Ankitube is designed to allow download of YouTube video clips easily for educational purposes. \n \n"
        "Simply copy the URL into the text box, enter the clip start and end times. "
        "FFMpeg is a required dependency to allow .mp4 to .webm conversion "
        "to ensure anki video player compatability.")
        
        title = tl
        msgBox = QtWidgets.QMessageBox(icon, title, text)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Cancel)

        msgBox.exec()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
