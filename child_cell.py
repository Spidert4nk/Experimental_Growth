from PyQt5 import QtWidgets, QtCore, QtGui
import small_objects

from theme import theme
theme = theme()


class Child_cell(QtWidgets.QLabel):
    """An object representing a 'child' cell with his appearance and logic.

    Args:
        scroll_area (Scroll_area): A Scroll_area object.
        main_object (QMainWindow): A QMainWindow object. Use to acces method of the main window.
    """

    def __init__(self, tab, main_object, number):
        super().__init__()
        self.main_object = main_object
        self.tab = tab
        self.master_current_value = self.tab.master_cell.value_dict
        self.value_dict = {
            "Time :": 0,
            "Starting Value :": None,
            "Growth Rate (%) :": None,
            "Add Value :": 0,
            "Random range :": [0, 0]
        }
        self.name = ""
        self.notes = ""
        self.decimal_shown = False
        self.random = False
        self.group_times = False
        self.use_master_time = False
        self.value_by_times = False

        self.setObjectName(f"Child_{number}")
        self.initUI()

    def initUI(self) -> None:
        """Init the Ui of the object.
        """
        self.setFixedHeight(120)
        self.setStyleSheet(theme.cell)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(5, 5, 5, 5)

        name_bundle = QtWidgets.QWidget()
        name_bundle_lay = QtWidgets.QHBoxLayout()
        name_label = QtWidgets.QLabel("Name")
        name_label.setStyleSheet(theme.text)
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setStyleSheet(theme.input_field)
        self.name_input.textChanged.connect(self.save_name)
        name_bundle_lay.addWidget(name_label)
        name_bundle_lay.addWidget(self.name_input)
        name_bundle.setLayout(name_bundle_lay)

        note_holder = QtWidgets.QWidget()
        note_hodler_lay = QtWidgets.QGridLayout()
        self.note_input = QtWidgets.QTextEdit()
        self.note_input.setFixedHeight(50)
        self.note_input.setPlaceholderText("Notes")
        self.note_input.setStyleSheet(theme.input_field)
        self.note_input.textChanged.connect(
            lambda: self.limite_notes_length(500))
        note_hodler_lay.addWidget(self.note_input)
        note_holder.setLayout(note_hodler_lay)
        note_holder.setFixedWidth(250)
        name_bundle.setFixedWidth(250)

        input_info = list(self.value_dict.items())
        # Here we take all the info in the value_dict, this output tuples => (key, value)
        # we then unpack the tuple and pass them as arguments using the "*tuple"

        self.start_duo = small_objects.Simple_Duo(self, *input_info[1])
        self.growth_duo = small_objects.Simple_Duo(self, *input_info[2])

        self.time_duo = small_objects.Spin_Duo(self, *input_info[0])
        self.time_checkbox = small_objects.My_CheckBox("Use Master Time")
        self.time_checkbox.toggled.connect(self.handle_checkbox)
        self.time_checkbox.setObjectName("use_master")

        # New code, and all valbytimes and value_by_times inclusions:
        self.valbytimes_checkbox = small_objects.My_CheckBox("Value by times")
        self.valbytimes_checkbox.toggled.connect(self.handle_checkbox)
        self.valbytimes_checkbox.setObjectName("valbytimes")

        self.random_checkbox = small_objects.My_CheckBox("Use Random Added")
        self.random_checkbox.toggled.connect(self.handle_checkbox)
        self.random_checkbox.setObjectName("random")

        self.add_duo = small_objects.Simple_Duo(self, *input_info[3])
        self.add_checkbox = small_objects.My_CheckBox("Group Times")
        self.add_checkbox.toggled.connect(self.handle_checkbox)
        self.add_checkbox.setObjectName("group")

        duplicate_button = small_objects.Dup_Button()
        duplicate_button.clicked.connect(
            lambda: self.tab.scroll_area.duplicate_child(self)
        )
        button_bundle = QtWidgets.QWidget()
        bundle_lay = QtWidgets.QHBoxLayout()
        up_one_button = small_objects.Generic_Small_Button("▲")
        up_one_button.setStyleSheet(theme.text)
        up_one_button.clicked.connect(
            lambda: self.tab.scroll_area.move_child("Up", self))

        down_one_button = small_objects.Generic_Small_Button("▼")
        down_one_button.setStyleSheet(theme.text)
        down_one_button.clicked.connect(
            lambda: self.tab.scroll_area.move_child("Down", self)
        )
        bundle_lay.addWidget(up_one_button)
        bundle_lay.addWidget(down_one_button)
        button_bundle.setLayout(bundle_lay)

        drop_down_duo = QtWidgets.QWidget()
        self.drop_down_duo_layout = QtWidgets.QHBoxLayout()
        drop_down_label = QtWidgets.QLabel("Move to :")
        self.drop_down = small_objects.My_DropDown(self, self.main_object)
        self.drop_down_duo_layout.addWidget(drop_down_label)
        self.drop_down_duo_layout.addWidget(self.drop_down)
        drop_down_duo.setLayout(self.drop_down_duo_layout)

        close_button = small_objects.Delete_Button()
        close_button.clicked.connect(
            lambda: self.tab.scroll_area.remove_specific_children([self])
        )
        self.result_duo = small_objects.Result_Duo(self, "Result :")

        self.decimal_checkbox = small_objects.My_CheckBox("See decimal")
        self.decimal_checkbox.toggled.connect(self.handle_checkbox)
        self.decimal_checkbox.setObjectName("see_decimal")

        checkbox_bundle = QtWidgets.QWidget()
        checkbox_bundle_layout = QtWidgets.QVBoxLayout()
        checkbox_bundle_layout.addWidget(self.valbytimes_checkbox)
        checkbox_bundle_layout.addWidget(self.random_checkbox)
        checkbox_bundle_layout.addWidget(self.add_checkbox)
        checkbox_bundle_layout.addWidget(self.time_checkbox)
        checkbox_bundle.setLayout(checkbox_bundle_layout)

        self.grid_layout.addWidget(name_bundle, 0, 0, 1, 2)
        self.grid_layout.addWidget(note_holder, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.time_duo, 0, 2, 1, 2)

        self.grid_layout.addWidget(self.start_duo, 1, 2, 1, 2)

        self.grid_layout.addWidget(self.growth_duo, 1, 4, 1, 2)

        self.grid_layout.addWidget(self.add_duo, 0, 4, 1, 2)
        self.grid_layout.addWidget(checkbox_bundle, 0, 6, 2, 2)

        self.grid_layout.addWidget(self.result_duo, 0, 8, 2, 6)
        self.grid_layout.addWidget(self.decimal_checkbox, 0, 12, 1, 1)
        self.grid_layout.addWidget(drop_down_duo, 0, 14, 1, 1)
        self.grid_layout.addWidget(button_bundle, 1, 14, 1, 1)
        self.grid_layout.addWidget(close_button, 0, 15, 1, 1)
        self.grid_layout.addWidget(duplicate_button, 1, 15, 1, 1)

        self.setLayout(self.grid_layout)

    def save_name(self):
        """Save the name from the name_input into a class variable.
        """
        self.name = self.name_input.text()

    def handle_checkbox(self):
        sender = self.sender()
        state = sender.isChecked()
        name = sender.objectName()
        # This replace a triple if statement, it's cleaner ;)
        match name:
            case "see_decimal":
                self.decimal_shown = state
            case "random": #passes state:true to tab.is_in_randoms
                self.random = state
                self.handle_random_display()
                added = self.tab.is_in_randoms(self.random, self.objectName(), self.value_dict["Random range :"])
                if added is not None:
                    self.value_dict["Add Value :"] = added #THIS is the line I need to work nicely with value_by_times
            case "use_master":
                self.use_master_time = state
            case "group":
                self.group_times = state
                if state:
                    self.tab.add_to_grouped(self)
                else:
                    self.tab.remove_from_grouped(self)
            case "valbytimes":
                self.value_by_times = state

        self.update_result()

    def check_times(self):
        self.tab.update_all_times(self)

    def update_result(self):
        """Update the result based on the value from the master_cell and it's own values.
        """
        keys = list(self.value_dict.keys())
        master_value_dict = self.master_current_value
        master_time = master_value_dict[keys[0]]
        master_start_value = master_value_dict[keys[1]]
        master_growth_value = master_value_dict[keys[2]]
        master_add_value = master_value_dict[keys[3]]
        time = self.value_dict[keys[0]]
        start_value = self.value_dict[keys[1]]
        growth_value = self.value_dict[keys[2]]
        add_value = self.value_dict[keys[3]]
        result = self.main_object.calc_results(
            master_time,
            master_start_value,
            master_growth_value,
            master_add_value,
            time,
            start_value,
            growth_value,
            add_value,
            self.use_master_time,
            self.group_times,
            self.value_by_times
        )
        if not self.decimal_shown:
            if "." in result:
                integer, decimal = result.split(".")
                if len(decimal) >= 3:
                    decimal = decimal[0:3]
                result = f"{integer}.{decimal}"
        self.result_duo.input_elem.setText(result)

    def limite_notes_length(self, max):
        """Limit the length of the notes.

        Args:
            max ([type]): The maximum note length.
        """
        current_text = self.note_input.toPlainText()
        current_text_length = len("".join(current_text.split("\n")))
        if current_text_length > max:
            self.note_input.textCursor().deletePreviousChar()
        self.notes = self.note_input.toPlainText()

    def reset_drop_down(self):
        """Reset the dropdown to it's default value.
        """
        drop_down = small_objects.My_DropDown(self, self.main_object)
        self.drop_down_duo_layout.removeWidget(self.drop_down)
        self.drop_down = drop_down
        self.drop_down_duo_layout.addWidget(self.drop_down)

    def update_all_display_value(self):
        """Update all the displays.
        """
        keys = list(self.value_dict.keys())
        self.name_input.setText(self.name)
        self.note_input.setText(self.notes)
        self.decimal_checkbox.setChecked(self.decimal_shown)
        self.valbytimes_checkbox.setChecked(self.value_by_times)
        self.random_checkbox.setChecked(self.random)
        self.handle_random_display()
        self.time_checkbox.setChecked(self.use_master_time)
        self.add_checkbox.setChecked(self.group_times)
        self.time_duo.update_display_value(str(int(self.value_dict[keys[0]])))
        self.start_duo.update_display_value(
            str(self.value_dict[keys[1]]))
        self.growth_duo.update_display_value(
            str(self.value_dict[keys[2]]))
        if self.value_dict[keys[3]] > 0:
            self.add_duo.update_display_value(str(self.value_dict[keys[3]]))

    def handle_random_display(self):
        #self.add_duo.setParent(None)
        self.add_duo.setParent(self)
        input_info = list(self.value_dict.items())
        if self.random:
            self.add_duo = small_objects.Random_Duo(self, *input_info[4])
            ranges = self.value_dict["Random range :"].copy()
            self.add_duo.input_max.setText(
                str(ranges[1]))
            self.add_duo.input_min.setText(
                str(ranges[0]))

        else:
            self.add_duo = small_objects.Simple_Duo(self, *input_info[3])
        self.grid_layout.addWidget(self.add_duo, 0, 4, 1, 2) 
