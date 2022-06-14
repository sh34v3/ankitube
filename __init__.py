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

from aqt.utils import *
# import all of the Qt GUI library
from aqt.qt import *
from aqt import gui_hooks

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def AddAnkiTubeButton() -> None:
    """
    Adds a button to the add card dialogue that opens AnkiTube

    Callback function for add_cards_did_init hook
    """
    at_button = aqt.qt.QPushButton()
    at_button.show()


gui_hooks.add_cards_did_init.append(testFuncton)



# Hook( #hook for the editor having initialized all but its buttons
# name="editor_did_init_left_buttons",
# args=["buttons: list[str]", "editor: aqt.editor.Editor"],
# ),

# Hook( #hook for the editor having initialized its buttons
#         name="editor_did_init_buttons",
#         args=["buttons: list[str]", "editor: aqt.editor.Editor"],
#     ),

# Hook( #hook for the add cards dialogue initializing
#     name="add_cards_did_init",
#     args=["addcards: aqt.addcards.AddCards"],
# ),