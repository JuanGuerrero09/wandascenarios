import sys
import random
import pywanda
import os
import wandalib
import sys


cwd =  r'C:\Users\juan.guerrero\Downloads\wanda\SIO'
wanda_bin = r'C:\Program Files (x86)\Deltares\Wanda 4.7\Bin\\'
wanda_file = os.path.join(cwd, "SIO_Basemodel.wdi")
wanda_model = pywanda.WandaModel(wanda_file, wanda_bin)

from random import choice

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt, QSize


window_titles = [
    "My App",
    "My App",
    "Still My App",
    "Still My App",
    "What on earth",
    "What on earth",
    "This is surprising",
    "This is surprising",
    "Something went wrong",
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wanda Scenarios Manager")
        self.setGeometry(100, 100, 800, 600)  # Set the window size
        self.setMinimumSize(QSize(800, 600))  # Set a minimum size

        self.n_times_clicked = 0

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.windowTitleChanged.connect(self.the_window_title_changed)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Clicked.")
        new_window_title = choice(window_titles)
        print("Setting title:  %s" % new_window_title)
        self.setWindowTitle(new_window_title)

    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == "Something went wrong":
            self.button.setDisabled(True)



app = QApplication([])
# app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()






all_components = wanda_model.get_all_components_str()

def get_current_components():
    current_components = wanda_model.get_all_components_str()
    components = {}
    for component in current_components:
        component_splited = component.split(" ", 1)
        type_ = component_splited[0]  # Avoid using 'type' as it's a built-in function
        name = component_splited[1]

        # Initialize the list if the key does not exist
        if type_ not in components:
            components[type_] = []

        components[type_].append(name)
    return components

def get_components_from_type(all_components, type):
    return all_components[type]


def show_components(filter, all_components):
    list = get_components_from_type(all_components, filter)
    str = ""
    for component in list[filter]:
        str += filter + " " + component + "\n"
    return str

