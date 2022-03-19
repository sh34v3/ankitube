#install ffmpeg if necessary
import os
import subprocess
import sys


try: #see if static-ffmpeg is installed
    os.system("static_ffmpeg -version")
    os.system("static_ffprobe -version")
except: # if not, call pip and install static-ffmpeg
    subprocess.call([sys.executable, "-m", "pip", "install", "static-ffmpeg"])
    os.system("static_ffmpeg -version")
    os.system("static_ffprobe -version")

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from aqt import gui_hooks

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

