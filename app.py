import sys
import random
import pywanda
import os
import wandalib
import sys

from dotenv import load_dotenv
import os

# Cargar variables desde el archivo WANDA_MODEL.env
load_dotenv("WANDA_MODEL.env")

wanda_bin = os.getenv("WANDA_BIN")
wanda_file = os.getenv("WANDA_FILE")

print(f"Wanda Bin Path: {wanda_bin}")
print(f"Wanda File Path: {wanda_file}")


cwd = r'C:\Users\juan.guerrero\Downloads\wanda\SIO'
wanda_bin = r'C:\Program Files (x86)\Deltares\Wanda 4.7\Bin\\'
wanda_file = os.path.join(cwd, "SIO_Basemodel.wdi")
wanda_model = pywanda.WandaModel(wanda_file, wanda_bin)

from random import choice

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QHBoxLayout,
    QGroupBox,
    QScrollArea,
    QWidget,
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont


TRANSIENT_OPTIONS = [
    "Valve Closing",
    "Pump Trip",]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wanda Scenarios Manager")
        self.setGeometry(100, 100, 800, 600)  # Set the window size
        self.setMinimumSize(QSize(800, 600))  # Set a minimum size
        
        self.wanda_bin = wanda_bin
        self.wanda_file = wanda_file
        
        self.wanda_model = None
        self.components = None
        
        self.cases = {}
        # Main layout
        main_layout = QVBoxLayout()
        
        # Current sections
        # Data section
        main_layout.addWidget(self.create_data_section())
        # Widgets section
        main_layout.addWidget(self.create_widgets_section())

        # Section for dynamically adding labels and comboboxes
        main_layout.addWidget(self.create_dynamic_widgets_section())
        
        # Buttons section
        main_layout.addWidget(self.create_buttons_section())
        
        # Configurar el widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def index_changed(self, index):  # index is an int starting from 0
        print(index)

    def text_changed(self, text):  # text is a str
        print(text)

    def create_data_section(self):
        data_layout = QVBoxLayout()
        data_layout.setSpacing(5)
        
        labels = [
        (f"Wanda Bin Path: {self.wanda_bin}", 10),
        # (f"Wanda File Path: {self.wanda_file}", None),
        # ("Wanda Model: ModelName", None),
        ]

        for text, font_size in labels:
            label = QLabel(text)
            if font_size:
                label.setFont(QFont("Roboto", font_size))
            label.setWordWrap(True)
            data_layout.addWidget(label)


        data_group = QGroupBox("Model Information")
        data_group.setLayout(data_layout)
        return data_group
    
    def create_widgets_section(self):
        """Crea la sección de widgets estáticos."""
        widgets_layout = QVBoxLayout()
        file_path_label = QLabel("No file selected")
        file_path_label.setWordWrap(True)
        widgets_layout.addWidget(file_path_label)
        self.file_path_label = file_path_label  # Store the label reference for later use
        
        # Button to open the file dialog
        file_button = QPushButton("Select File")
        file_button.clicked.connect(self.open_file_dialog)
        widgets_layout.addWidget(file_button)

        widgets_group = QGroupBox("Widgets")
        widgets_group.setLayout(widgets_layout)
        return widgets_group
    
    def create_dynamic_widgets_section(self):
        """Crea la sección de widgets dinámicos con scroll."""
        self.dynamic_layout = QVBoxLayout()
        self.dynamic_layout.setSpacing(5)

        dynamic_widget = QWidget()
        dynamic_widget.setLayout(self.dynamic_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(dynamic_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(200)

        dynamic_group = QGroupBox("Transient Scenarios")
        dynamic_group_layout = QVBoxLayout()
        dynamic_group_layout.addWidget(scroll_area)
        dynamic_group.setLayout(dynamic_group_layout)
        return dynamic_group

    def create_buttons_section(self):
        """Crea los botones para agregar widgets dinámicos."""

        # add_label_button = QPushButton("Add Label")
        # add_label_button.clicked.connect(self.open_file_dialog)
        # buttons_layout.addWidget(add_label_button)
        
        # Botón para agregar escenarios
        self.add_scenario_trip_button = QPushButton("Add Trip Scenario")
        self.add_scenario_trip_button.setEnabled(False)  # Initially disabled
        self.add_scenario_trip_button.clicked.connect(self.add_scenario)
        
        self.add_scenario_closure_button = QPushButton("Add Closure Scenario")
        self.add_scenario_closure_button.setEnabled(False)  # Initially disabled
        self.add_scenario_closure_button.clicked.connect(self.add_scenario)
        
        
        
        self.scenario_layout = QHBoxLayout()
        self.scenario_layout.addWidget(self.add_scenario_trip_button)
        self.scenario_layout.addWidget(self.add_scenario_closure_button)
        self.scenario_layout.addStretch()  # Add stretchable space to the right
        

        buttons_widget = QWidget()
        buttons_widget.setLayout(self.scenario_layout)
        return buttons_widget
    
    def open_file_dialog(self):
        # Open a file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "All Files (*.*);;Text Files (*.txt)")
        if file_path:
            self.file_path_label.setText(file_path)  # Display the selected file path
            self.wanda_file = file_path  # Update the wanda_file with the selected file path
            self.wanda_model = pywanda.WandaModel(self.wanda_file, self.wanda_bin)
            self.add_scenario_button.setEnabled(True)  # Enable the button after loading the model
            self.components = self.get_current_components()
            
    def add_label(self):
        new_label = QLabel("New Label")
        self.dynamic_layout.addWidget(new_label)

        
    def add_scenario(self):
        # Obtener el número dinámico basado en la cantidad de elementos ya creados
        scenario_number = self.dynamic_layout.count() + 1

        # Crear un QLabel con el texto "Scenario X"
        scenario_label = QLabel(f"Scenario {scenario_number}")

        # Crear un QComboBox con las opciones
        scenario_combobox = QComboBox()
        scenario_combobox.addItems(TRANSIENT_OPTIONS)
                
        # Crear combobox para cada tipo de componente
        type = scenario_combobox.currentText()
        if type == "Valve Closing":
            componentType = "VALVE"
        elif type == "Pump Trip":
            componentType = "PUMP"
        components = self.get_components_from_type(self.components, componentType)
        component_combobox = QComboBox()
        print(components)
        component_combobox.addItems(["Hola"])
        

        # Crear un layout horizontal para colocar el label y el combobox en la misma línea
        scenario_layout = QHBoxLayout()
        scenario_layout.addWidget(scenario_label)
        scenario_layout.addWidget(scenario_combobox)
        scenario_layout.addWidget(component_combobox)

        # Crear un contenedor para el layout horizontal
        scenario_widget = QWidget()
        scenario_widget.setLayout(scenario_layout)

        # Agregar el contenedor al layout dinámico
        self.dynamic_layout.addWidget(scenario_widget)
        
    def get_current_components(self):
        current_components = self.wanda_model.get_all_components_str()
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
    
    def get_components_from_type(self, all_components, type):
        print(type)
        print(all_components)
        # return all_components[type]


app = QApplication([])
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
