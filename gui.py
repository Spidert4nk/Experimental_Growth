from PyQt5 import QtWidgets, QtCore

from decimal import Decimal
import pathlib

import input_output
from accuracy import more_accurate_results
from tab import Tab_Bar

from theme import theme
theme = theme()


def get_working_slash() -> str:
    """Decide which slash ('/', '\') is the prefered one the OS.

    Returns:
        str: The working slash
    """
    # NOTE : There's builtin library that help us get wich specific OS is running.
    # However, since I only need to make a choice between Windows or Unix, this is easier.
    path = pathlib.Path(__file__).parent.resolve()
    try:
        back_count = len(path.split("\\"))
    except:
        back_count = 0
    try:
        forward_count = len(path.split("/"))
    except:
        forward_count = 0

    # There's more back slash then forward slash, we're probably on Windows.
    if back_count > forward_count:
        return "\\"
    # We're on Unix
    return "/"


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """Init the UI of the obect.
        """
        self.setStyleSheet(theme.background)
        self.setWindowTitle("Exponential Growth Calculation Tool")
        self.setMinimumSize(QtCore.QSize(1200, 400))
        self.central_widget = Tab_Bar(self)
        self.setCentralWidget(self.central_widget)
        self.setObjectName("MainWindow")

        self.show()

    def calc_results(
        self,
        master_time: int,
        master_start_value: Decimal,
        master_growth_value: Decimal,
        master_add_value: Decimal,
        time: int,
        start_value: Decimal,
        growth_value: Decimal,
        add_value: Decimal,
        use_master_time: bool,
        group_cell: bool,
        value_by_times: bool,
    ) -> str:
        """Calculate the result base on the given values. Use more_accurate_results() as backend.

        Args:
            master_time (int): An int representing the value of the 'time' in the Master_cell.
            master_start_value (Decimal): A Decimal Object representing the value of the 'starting value' in the Master_cell.
            master_growth_value (Decimal): A Decimal Object representing the value of the 'growth rate' in the Master_cell.
            master_add_value (Decimal): A Decimal Object representing the value of the 'added value' in the Master_cell.
            time (Decimal): An int representing the value of the 'time' in the Child_cell.
            start_value (Decimal): A Decimal Object representing the value of the 'starting value' in the Child_cell.
            growth_value (Decimal): A Decimal Object representing the value of the 'growth rate' in the Child_cell.
            add_value (Decimal): A Decimal Object representing the value of the 'added value' in the Child_cell.
            value_by_times (Bool): Added after the fact. Multiplies the 'added value' by the amount of Times in Child_cell.

        Returns:
            str: A formated string of the result.
        """

        display = "Lacking information : "
        if master_start_value is None and start_value is None:
            display += "starting value ; "
        if master_growth_value is None and growth_value is None:
            display += "growth rate "
        if display[len(display) - 2: len(display)] == "; ":
            display = display[:-2]

        # Basicly if there's no lacking info.
        if display == "Lacking information : ":
            values = {
                "master_start_value": master_start_value,
                "master_growth_value": master_growth_value,
                "master_add_value": master_add_value,
                "start_value": start_value,
                "growth_value": growth_value,
                "add_value": add_value,
            }
            # We make sure to put all the unknow values (value = None) to 0 because we can't make math with "None" values.
            for key, value in values.items():
                if value is None:
                    values[key] = 0

            result = more_accurate_results(
                master_time,
                values["master_start_value"],
                values["master_growth_value"],
                values["master_add_value"],
                time,
                values["start_value"],
                values["growth_value"],
                values["add_value"],
                use_master_time,
                group_cell,
                value_by_times,
            )

            return result
        else:
            return display

    def get_last_path(self):
        try:
            slash = get_working_slash
            with open(f".{slash}last_path.txt", "r") as file:
                p = file.readlines()

            saving = p[1].replace("\n", "")
            printing = p[3].replace("\n", "")

            slash = get_working_slash()
            saving = slash.join(saving.split(slash)[0:-1])
            printing = slash.join(printing.split(slash)[0:-1])

        except:
            saving = ""
            printing = ""
        return saving, printing

    def save_last_path(self, new_saving: str = None, new_printing: str = None):
        saving, printing = self.get_last_path()

        if new_saving is None:
            new_saving = saving
        if new_printing is None:
            new_printing = printing

        text = f"Last saving path\n{new_saving}\nLast printing path\n{new_printing}\n"

        slash = get_working_slash()
        with open(f".{slash}last_path.txt", "w") as file:
            file.write(text)

    def save_in_file(self, tab):
        """Save the current cells info in a text file.
        """

        saving, _ = self.get_last_path()

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exponential Growth", saving, "Text(*.txt)"
        )
        # No path is given so we can't save a file anywhere
        if file_path == "":
            return
        # If we overwrite a previous text file, only get is name and not is extension
        file_path = file_path.split(".txt")[0]

        self.save_last_path(new_saving=file_path)

        current_children_count = tab.scroll_area.content_holder_layout.count() - 1
        all_children = [
            tab.scroll_area.content_holder_layout.itemAt(index).widget()
            for index in range(current_children_count)
        ]

        with open(f"{file_path}.txt", "w") as saving_file:
            saving_file.write(input_output.format_all(
                tab.master_cell, all_children, tab.seed, tab.existing_randoms, tab.randoms_cells))

    def load_from_file(self, tab):
        """Load the cells from a text file.
        """
        saving, _ = self.get_last_path()

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Exponential Growth", saving, "Texte(*.txt)"
        )
        # No path is given so we can't open a file
        if file_path == "":
            return

        with open(file_path, "r") as loading_file:
            list_of_lines = loading_file.readlines()

        seed, randoms, master, children_list = input_output.decode_all(
            list_of_lines)

        tab.seed = seed
        tab.existing_random = randoms

        tab.master_cell.value_dict = master
        tab.master_cell.update_all_display_value()
        tab.scroll_area.remove_all_children()
        for child_info in children_list:
            tab.scroll_area.add_child()
            index = tab.scroll_area.content_holder_layout.count() - 2
            new_child = tab.scroll_area.content_holder_layout.itemAt(
                index).widget()
            new_child.name = child_info[0]
            new_child.notes = child_info[1]
            new_child.value_dict = child_info[2]
            new_child.master_current_value = child_info[3]
            new_child.decimal_shown = child_info[4]
            new_child.random = child_info[5]
            new_child.use_master_time = child_info[6]
            new_child.group_times = child_info[7]
            new_child.update_all_display_value()
            new_child.update_result()

    def print_in_file(self, tab):
        _, printing = self.get_last_path()

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exponential Growth", printing, "Texte(*.txt)"
        )
        # No path is given so we can't save a file anywhere
        if file_path == "":
            return
        # If we overwrite a previous text file, only get is name and not is extension
        file_path = file_path.split(".txt")[0]

        self.save_last_path(new_printing=file_path)

        current_children_count = tab.scroll_area.content_holder_layout.count() - 1
        all_children = [
            tab.scroll_area.content_holder_layout.itemAt(index).widget()
            for index in range(current_children_count)
        ]

        text = ""
        for child in all_children:
            name = child.name_input.text()
            result = child.result_duo.input_elem.toPlainText()
            text += f"{name} = {result}\n"

        with open(f"{file_path}.txt", "w") as printing_file:
            printing_file.write(text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
