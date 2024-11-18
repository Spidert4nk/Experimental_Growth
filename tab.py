from tabnanny import check
from PyQt5 import QtWidgets
from master_cell import Master_cell
from scroll_area import Scroll_area
import random
import sys


class Tab(QtWidgets.QWidget):
    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window
        self.grouped_cells = []
        self.seed = random.randrange(sys.maxsize)
        random.seed(self.seed)
        self.existing_randoms = {}
        self.randoms_cells = {}
        self.init_ui()

    def init_ui(self):
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.setContentsMargins(10, 10, 10, 5)

        self.master_cell = Master_cell(self, self.main_window)

        self.scroll_area = Scroll_area(self.main_window)

        vertical_layout.addWidget(self.master_cell)
        vertical_layout.addWidget(self.scroll_area)

        self.setLayout(vertical_layout)

    def add_to_grouped(self, cell):
        self.grouped_cells.append(cell)
        self.update_all_times(cell)

    def remove_from_grouped(self, cell):
        self.grouped_cells.remove(cell)
        self.update_all_times(cell)

    def update_all_times(self, cell):
        if len(self.grouped_cells) > 0 and cell in self.grouped_cells:
            time = cell.value_dict["Time :"]
            for cell in self.grouped_cells:
                cell.value_dict["Time :"] = time
                cell.update_all_display_value()
                cell.update_result()
            return
        else:
            cell.update_result()
            return

    def is_in_randoms(self, state: bool, cell: str, range: list[int]):
        if range[0] > range[1]:
            range[0] = range[1]
        query_string = f"{range[0]}-{range[1]}"
        return_value = None
        if state:
            self.randoms_cells[cell] = query_string
            return_value = self.check_randoms(*range)
        else:
            if cell in self.randoms_cells:
                del self.randoms_cells[cell]

        possibilities = list(self.existing_randoms.keys())

        for possible_range in possibilities:
            if possible_range not in self.randoms_cells.values():
                del self.existing_randoms[possible_range]

        return return_value

    def check_randoms(self, mins: int, maxs: int):
        mins = mins
        maxs = maxs

        query_string = f"{mins}-{maxs}"
        if query_string in self.existing_randoms:
            rand = self.existing_randoms[query_string]
            return rand
        else:
            rand = random.randint(mins, maxs)
            self.existing_randoms[query_string] = rand
            return rand

class Tab_Bar(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setUpdatesEnabled(True)
        self.setTabsClosable(True)

        self.make_bar()

        self.tabCloseRequested.connect(self.close_tab)

    def make_bar(self):
        self.insertTab(0, Tab(self.parent()), "Tab_1")
        tb = QtWidgets.QToolButton()
        tb.setText(" + ")
        tb.clicked.connect(self.add_tab)
        self.addTab(QtWidgets.QWidget(), "")
        self.setTabEnabled(1, False)
        self.tabBar().setTabButton(1, QtWidgets.QTabBar.ButtonPosition.RightSide, tb)

        close_button = QtWidgets.QTabBar.ButtonPosition.RightSide
        # This line hide the close button of the first tab, using "hide()" will keep the tab size as
        # if the button was still there
        self.tabBar().tabButton(0, close_button).hide()

    def add_tab(self):
        index = self.count()-1
        self.insertTab(index, Tab(self.parent()), f"Tab_{index+1}")
        self.setCurrentIndex(index)

    def close_tab(self, index):
        self.setCurrentIndex(index-1)
        self.removeTab(index)
