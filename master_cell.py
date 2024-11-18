from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton

import small_objects
from theme import theme

theme = theme()


class Master_cell(QLabel):
    """An object representing the 'master' cell with his appearance and logic.

    Args:
        main_object (QMainWindow): A QMainWindow object. Use to acces method of the main window.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.setObjectName("MASTER CELL")
        self.main_window = main_window
        self.value_dict = {
            "Time :": 0,
            "Starting Value :": None,
            "Growth Rate (%) :": None,
            "Add Value :": 0,
        }

        self.initUI()

    def initUI(self) -> None:
        """Init the UI of the object.
        """
        self.setMinimumWidth(800)
        self.setFixedHeight(120)
        self.setStyleSheet(theme.cell)

        font = QFont("Arial", 15)

        grid_layout = QGridLayout()

        print_button = QPushButton("Print")
        print_button.setMaximumSize(QSize(100, 40))
        print_button.clicked.connect(
            lambda: self.main_window.print_in_file(self.parent()))

        title = QLabel("Master Values")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(font)
        title.setStyleSheet(theme.title)

        input_info = list(self.value_dict.items())
        # Here we take all the info in the value_dict, this output tuples => (key, value)
        # we then unpack the tuple and pass them as arguments using the "*tuple"
        self.time_duo = small_objects.Spin_Duo(self, *input_info[0])
        self.start_duo = small_objects.Simple_Duo(self, *input_info[1])
        self.growth_duo = small_objects.Simple_Duo(self, *input_info[2])
        self.add_duo = small_objects.Simple_Duo(self, *input_info[3])

        save_button = QPushButton("Save")
        save_button.setMaximumSize(QSize(100, 40))
        save_button.setStyleSheet(theme.save_button)
        save_button.clicked.connect(
            lambda: self.main_window.save_in_file(self.parent()))

        load_button = QPushButton("Load")
        load_button.setMaximumSize(QSize(100, 40))
        load_button.setStyleSheet(theme.load_button)
        load_button.clicked.connect(
            lambda: self.main_window.load_from_file(self.parent()))

        grid_layout.addWidget(print_button, 0, 0, 2, 1)
        grid_layout.addWidget(title, 0, 1, 1, 4)
        grid_layout.addWidget(self.time_duo, 3, 1, 2, 1)
        grid_layout.addWidget(self.start_duo, 3, 2, 2, 1)
        grid_layout.addWidget(self.growth_duo, 3, 3, 2, 1)
        grid_layout.addWidget(self.add_duo, 3, 4, 2, 1)
        grid_layout.addWidget(save_button, 0, 5, 2, 1)
        grid_layout.addWidget(load_button, 3, 5, 2, 1)

        self.setLayout(grid_layout)

    def update_all_children(self):
        """Update all the "master_current_value" class variable of all the children to the current values of the 'Master_cell'.
        """
        children_holder = self.parent().scroll_area.content_holder_layout
        # We don't want the "add cell" button
        current_children_count = children_holder.count() - 1
        children = [
            children_holder.itemAt(index).widget()
            for index in range(current_children_count)
        ]
        for child in children:
            child.master_current_value = self.value_dict
            child.update_result()

    def update_all_display_value(self):
        """Update all the displays.
        """
        keys = list(self.value_dict.keys())
        self.time_duo.update_display_value(str(self.value_dict[keys[0]]))
        self.start_duo.update_display_value(
            str(self.value_dict[keys[1]]))
        self.growth_duo.update_display_value(
            str(self.value_dict[keys[2]]))
        self.add_duo.update_display_value(str(self.value_dict[keys[3]]))
