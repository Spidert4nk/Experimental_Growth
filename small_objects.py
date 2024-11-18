from PyQt5 import QtWidgets, QtCore, QtGui
from theme import theme
theme = theme()


class Duo(QtWidgets.QWidget):
    def __init__(self, parent, title, place_holder):
        super().__init__()
        self.title = title
        self.value = None
        if place_holder is None:
            place_holder = ""
        self.place_holder = str(place_holder)
        self.parent = parent

        self.setParent(parent)
        self.setObjectName(title)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                           QtWidgets.QSizePolicy.Policy.Preferred)

    def update_parent_value(self):
        object_name = self.objectName()
        title = self.title
        if object_name != "Result :":
            if self.objectName() == "Random_Duo":
                mins = self.input_min.text()
                if mins == "":
                    mins = 0
                maxs = self.input_max.text()
                if maxs == "":
                    maxs = mins
                value = [int(mins), int(maxs)]
                title = "Random range :"
            elif self.objectName() == "Spin_Duo":
                value = self.input_elem.input_elem.text()
            else:
                value = self.input_elem.text()

            if value == "":
                self.parent.value_dict[title] = None
            elif type(value) == type([]):
                self.parent.value_dict[title] = value
            else:
                self.parent.value_dict[title] = float(value)

        if "Child" in self.parent.objectName():
            if isinstance(self, Spin_Duo):
                self.parent.check_times()
            elif isinstance(self, Random_Duo):
                state = self.parent.random
                cell = self.parent.objectName()
                range = self.parent.value_dict["Random range :"]
                self.parent.tab.is_in_randoms(state, cell, range)
            else:
                self.parent.update_result()
        else:
            self.parent.update_all_children()

    def update_display_value(self, value: str):
        if self.objectName() == "Spin_Duo":
            display = self.input_elem.input_elem
        elif self.objectName() == "Random_Duo":
            return
            # display = self.input_min
        else:
            display = self.input_elem

        display.setText(value)

class Random_Duo(Duo):
    def __init__(self, parent, title, range):
        super().__init__(parent, title, "")
        self.setObjectName("Random_Duo")
        self.init_ui(range)

    def init_ui(self, range) -> None:
        self.setMinimumWidth(150)
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        input_title = QtWidgets.QLabel(self.title)
        input_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        input_title.setStyleSheet(theme.text)

        input_holder = QtWidgets.QWidget()
        input_holder_layout = QtWidgets.QHBoxLayout()
        input_holder_layout.setContentsMargins(0, 0, 0, 0)

        self.input_min = My_Line_Edit(self)
        self.input_max = My_Line_Edit(self)

        input_holder_layout.addWidget(self.input_min)
        input_holder_layout.addWidget(self.input_max)
        input_holder.setLayout(input_holder_layout)

        vertical_layout.addWidget(input_title)
        vertical_layout.addWidget(input_holder)

        self.setLayout(vertical_layout)


class Simple_Duo(Duo):
    def __init__(self, parent, title, place_holder):
        super().__init__(parent, title, place_holder)
        self.init_ui()
        self.setObjectName("Simple_Duo")

    def init_ui(self) -> None:
        self.setMinimumWidth(150)
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        input_title = QtWidgets.QLabel(self.title)
        input_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        input_title.setStyleSheet(theme.text)

        self.input_elem = My_Line_Edit(self)
        self.input_elem.setPlaceholderText(self.place_holder)

        vertical_layout.addWidget(input_title)
        vertical_layout.addWidget(self.input_elem)

        self.setLayout(vertical_layout)


class Spin_Duo(Duo):
    def __init__(self, parent, title, place_holder):
        super().__init__(parent, title, place_holder)
        self.init_ui()
        self.setObjectName("Spin_Duo")

    def init_ui(self) -> None:
        self.setMinimumWidth(150)
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        input_title = QtWidgets.QLabel(self.title)
        input_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        input_title.setStyleSheet(theme.text)
        self.input_elem = Spin_box()
        self.input_elem.input_elem.textChanged.connect(
            self.update_parent_value)
        self.input_elem.setStyleSheet(theme.input_field)

        vertical_layout.addWidget(input_title)
        vertical_layout.addWidget(self.input_elem)

        self.setLayout(vertical_layout)


class Result_Duo(Duo):
    def __init__(self, parent, title):
        super().__init__(parent, title, "")
        self.init_ui()

    def init_ui(self) -> None:
        lay = QtWidgets.QVBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignBaseline)

        input_title = QtWidgets.QLabel(self.title)
        input_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        input_title.setStyleSheet(theme.text)
        input_title.setFixedSize(40, 20)
        self.input_elem = QtWidgets.QTextEdit()
        self.input_elem.setReadOnly(True)
        self.input_elem.setFixedHeight(60)
        self.input_elem.setStyleSheet(theme.input_field)

        lay.addWidget(input_title)
        lay.addWidget(self.input_elem)

        self.setLayout(lay)


class My_Line_Edit(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
        self.textChanged.connect(self.custom_input_flag)

    def init_ui(self) -> None:
        self.setFixedHeight(25)
        self.setStyleSheet(theme.input_field)

    def custom_input_flag(self):
        def set_new_text(text):
            self.setText(text)
            self.setCursorPosition(len(text))

        accepted = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

        current_text = self.text()
        if len(current_text) >= 1:
            last_char = current_text[len(current_text) - 1]
            previous_text = current_text[0:-1]
            if (
                (len(current_text) == 1 and last_char == ".")
                or last_char not in accepted
                or (last_char == "." and "." in previous_text)
            ):
                return set_new_text(previous_text)

            elif "." in current_text:
                integer, decimal = current_text.split(".")
                if len(decimal) > 3:
                    decimal = decimal[0:3]
                    new_text = f"{integer}.{decimal}"
                    set_new_text(new_text)
        return self.parent.update_parent_value()


class Spin_box(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.minus_button = QtWidgets.QPushButton("<")
        self.minus_button.setFixedSize(QtCore.QSize(25, 25))
        self.minus_button.setStyleSheet(theme.cell)
        self.minus_button.clicked.connect(self.remove_1)

        self.input_elem = QtWidgets.QLineEdit()
        self.input_elem.setFixedHeight(25)
        self.input_elem.setValidator(QtGui.QIntValidator())
        self.input_elem.setText("0")
        self.input_elem.textChanged.connect(self.check_for_negative)

        plus_button = QtWidgets.QPushButton(">")
        plus_button.setFixedSize(QtCore.QSize(25, 25))
        plus_button.setStyleSheet(theme.cell)
        plus_button.clicked.connect(self.add_1)

        horizontal_layout.addWidget(self.minus_button)
        horizontal_layout.addWidget(self.input_elem)
        horizontal_layout.addWidget(plus_button)

        self.setLayout(horizontal_layout)

    def add_1(self):
        value = int(float(self.input_elem.text()))
        value += 1
        self.input_elem.setText(str(value))
        self.check_for_disable()

    def remove_1(self):
        value = int(float(self.input_elem.text()))
        value -= 1
        self.input_elem.setText(str(value))
        self.check_for_disable()

    def check_for_negative(self):
        if self.input_elem.text() == "" or int(float(self.input_elem.text())) < 0:
            self.input_elem.setText("0")
            self.check_for_disable()

    def check_for_disable(self):
        if int(self.input_elem.text()) == 0:
            self.minus_button.setDisabled(True)
        else:
            self.minus_button.setDisabled(False)


class My_DropDown(QtWidgets.QComboBox):
    def __init__(self, parent, main_object) -> None:
        super().__init__()
        self.parent = parent
        self.main_object = main_object
        self.setCurrentText("")
        self.addItems(["🡻", "🡹", "↑3", "↓3", "↑5", "↓5"])
        self.activated[str].connect(self.triggered)
        self.setFixedWidth(24)

    def triggered(self, text):
        self.parent.scroll_area.move_child(text, self.parent)


class My_CheckBox(QtWidgets.QCheckBox):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("Arial", 10))
        self.setStyleSheet(
            "QCheckBox::indicator{width:20px;height:20px;}")


class Generic_Small_Button(QtWidgets.QPushButton):
    def __init__(self, text):
        super().__init__(text=text)
        self.setFont(QtGui.QFont('Arial', 12))
        self.setFixedSize(QtCore.QSize(28, 28))


class Delete_Button(Generic_Small_Button):
    """Inherite the "Generic_Small_Button" and apply a custom text.
    """

    def __init__(self):
        super().__init__("🗑")


class Dup_Button(Generic_Small_Button):
    def __init__(self):
        super().__init__("⿻") #📋
