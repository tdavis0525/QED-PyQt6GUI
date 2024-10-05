# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, QWidget,
                             QVBoxLayout, QFormLayout, QLabel, QLineEdit, QSpinBox,
                             QDoubleSpinBox, QComboBox, QPushButton, QTextEdit, QFileDialog, QDialog, QVBoxLayout)
from PyQt6.QtCore import Qt
from configuration import Configuration
import json
from visualization import visualize_data

class VisualizationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualization")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add file selection dropdown
        self.file_combobox = QComboBox(self)
        layout.addWidget(self.file_combobox)

        # Add visualize button
        visualize_button = QPushButton("Visualize", self)
        visualize_button.clicked.connect(self.visualize)
        layout.addWidget(visualize_button)

        self.visualization_widget = QWidget(self)  # Widget to display visualization
        layout.addWidget(self.visualization_widget)
        self.thumbnail = None

    def populate_files(self, filenames):
        self.file_combobox.clear()
        self.file_combobox.addItems(filenames)

    def visualize(self):
        selected_file = self.file_combobox.currentText()
        if selected_file:
            self.thumbnail = visualize_data(selected_file)  # Visualize and get the thumbnail

class SimulationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Molecular Simulation Control")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Menu Bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)
        view_menu = QMenu("View", self)
        menu_bar.addMenu(view_menu)


        # Menu Actions
        save_action = QAction("Save Configuration", self)
        save_action.triggered.connect(self.save_config)
        file_menu.addAction(save_action)

        load_action = QAction("Load Configuration", self)
        load_action.triggered.connect(self.load_config)
        file_menu.addAction(load_action)

        visualize_action = QAction("Visualize Data", self)
        visualize_action.triggered.connect(self.show_visualization_dialog)
        view_menu.addAction(visualize_action)

        # Configuration Form
        config_form = QFormLayout()
        main_layout.addLayout(config_form)

        # MongoDB Configuration
        self.mongodb_uri_field = QLineEdit()
        self.database_name_field = QLineEdit()
        self.collection_name_field = QLineEdit()
        config_form.addRow(QLabel("MongoDB URI:"), self.mongodb_uri_field)
        config_form.addRow(QLabel("Database Name:"), self.database_name_field)
        config_form.addRow(QLabel("Collection Name:"), self.collection_name_field)

        # Simulation Parameters
        self.num_steps_field = QSpinBox()
        self.dt_field = QDoubleSpinBox()
        config_form.addRow(QLabel("Number of Steps:"), self.num_steps_field)
        config_form.addRow(QLabel("Time Step (dt):"), self.dt_field)

        # Molecule Configuration (using predefined molecules)
        self.molecule_config_editor = QTextEdit()
        config_form.addRow(QLabel("Molecule Configuration (JSON):"), self.molecule_config_editor)


        # Start/Stop Buttons
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        start_button = QPushButton("Start Simulation")
        button_layout.addWidget(start_button)
        stop_button = QPushButton("Stop Simulation")
        button_layout.addWidget(stop_button)

        # Connect buttons (example)
        # ... (Connect start_button and stop_button to your simulation logic)

        self.visualization_dialog = None


    def save_config(self):
        config = self.create_config_object()
        config_data = config.to_dict()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "config.json", "JSON Files (*.json)")
        if filename:
            with open(filename, "w") as f:
                json.dump(config_data, f, indent=4)

    def load_config(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Configuration", "", "JSON Files (*.json)")
        if filename:
            try:
                with open(filename, 'r') as f:
                    config_dict = json.load(f)
                    config = Configuration()
                    config.from_dict(config_dict)
                    # Update GUI elements using the loaded config data
                    # ...
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                dialog = QMaterialDialog(self)
                dialog.setWindowTitle("Error")
                dialog.setLabelText(f"Error loading configuration: {e}")
                dialog.addButton("OK")
                dialog.exec()

    def create_config_object(self):
        # Get values from the GUI widgets and create a Configuration object. Update as needed.
        mongodb_uri = self.mongodb_uri_field.text()
        database_name = self.database_name_field.text()
        collection_name = self.collection_name_field.text()
        num_steps = self.num_steps_field.value()
        dt = self.dt_field.value()
        try:
            molecules = json.loads(self.molecule_config_editor.toPlainText())
        except json.JSONDecodeError:
            dialog = QMaterialDialog(self)
            dialog.setWindowTitle("Error")
            dialog.setLabelText("Invalid molecule configuration JSON.")
            dialog.addButton("OK")
            dialog.exec()
            return None
        return Configuration(mongodb_uri, database_name, collection_name, num_steps, dt, molecules)

    def show_visualization_dialog(self):
        if self.visualization_dialog is None:
            self.visualization_dialog = VisualizationDialog(self)
            filenames = ["simulation_data.json"]
            self.visualization_dialog.populate_files(filenames)
        self.visualization_dialog.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimulationGUI()
    window.show()
    sys.exit(app.exec())