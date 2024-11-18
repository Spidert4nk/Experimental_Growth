from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from child_cell import Child_cell

from theme import theme
theme = theme()


class Scroll_area(QScrollArea):
    """An object representing a 'scroll area' with his appearance and logic.

    Args:
        main_object (QMainWindow): A QMainWindow object. Use to acces method of the main window.
    """

    def __init__(self, main_object: QMainWindow):
        super().__init__()
        self.main_object = main_object
        self.init_ui()

    def init_ui(self) -> None:
        """Init the UI of the object.
        """
        self.setWidgetResizable(True)
        content_holder = QWidget()
        content_holder.setStyleSheet(theme.scroll_area)

        self.content_holder_layout = QVBoxLayout()
        self.content_holder_layout.setContentsMargins(30, 20, 20, 30)
        content_holder.setLayout(self.content_holder_layout)

        add_child_button = QPushButton("Add cell")
        add_child_button.clicked.connect(self.add_child)
        add_child_button.setFixedHeight(80)
        add_child_button.setStyleSheet(f"margin:20px;{theme.cell}")

        self.content_holder_layout.addWidget(add_child_button)

        self.setWidget(content_holder)

    def add_child(self) -> None:
        """Add a Child_cell object at the end of the scroll area.
        """
        current_children_count = self.content_holder_layout.count()
        next_child_index = current_children_count - 1
        cell = Child_cell(self.parent(), self.main_object,
                          current_children_count)
        self.content_holder_layout.insertWidget(next_child_index, cell)

        cell.update_result()

    def move_child(self, place: str, child: Child_cell):
        """Move the given 'child' to the given 'place'.

        Args:
            place ([type]): A string representing the place where the child should be put.
            child ([type]): A Child_cell object.
        """
        # We don't want the 'add cell' button
        current_children_count = self.content_holder_layout.count() - 1
        child_index = self.content_holder_layout.indexOf(child)
        possible_places = {
            "🡹": float("-inf"),
            "🡻": current_children_count,
            "Up": -1,
            "Down": 1,
            "↑3": -3,
            "↓3": 3,
            "↑5": -5,
            "↓5": 5,
        }
        next_index = possible_places[place]
        child_index += next_index
        if child_index >= current_children_count:
            child_index = current_children_count - 1
        elif child_index < 0:
            child_index = 0
        self.content_holder_layout.removeWidget(child)
        self.content_holder_layout.insertWidget(child_index, child)
        self.update()
        child.reset_drop_down()

    def duplicate_child(self, child: Child_cell):
        """Make a copy of the given 'child' and put it right under it in the scroll area.

        Args:
            child ([type]): A Child_cell object.
        """
        new_child = Child_cell(self.parent(), self.main_object, self.content_holder_layout.count())
        new_child.master_current_value = child.master_current_value.copy()
        new_child.value_dict = child.value_dict.copy()
        new_child.decimal_shown = child.decimal_shown
        new_child.use_master_time = child.use_master_time
        new_child.value_by_times = child.value_by_times
        new_child.group_times = child.group_times
        new_child.update_all_display_value()
        new_child.update_result()
        child_index = self.content_holder_layout.indexOf(child)
        self.content_holder_layout.insertWidget(child_index + 1, new_child)

    def remove_all_children(self):
        """Remove all the children from the scroll area.
        """
        current_children_count = self.content_holder_layout.count() - 1
        all_children = [
            self.content_holder_layout.itemAt(index).widget()
            for index in range(current_children_count)
        ]
        self.remove_specific_children(all_children)

    def remove_specific_children(self, children_list: list) -> None:
        for child in children_list:
            child.setParent(None)
        self.update()
