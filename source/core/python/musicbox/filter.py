# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config, plugins

if config.pyside_version == 2:
    from PySide2.QtCore import QObject, Qt, Signal, Slot
    from PySide2.QtWidgets import QAction, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import QObject, Qt, Signal, Slot
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QVBoxLayout, QWidget


class FilterSelectionWidget(QWidget):

    selected = Signal(str, object)
    
    def __init__(self, parent, input):
        super().__init__(parent)
        self.input = input


class FilterAction(QAction):
    
    selection_widget_created = Signal(FilterSelectionWidget)
    output_ready = Signal(object)

    def __init__(self, parent, *, input=None, input_producer=None, filter=None):
        super().__init__("Filter", parent)
        self.triggered.connect(self.run)
        self.input = input
        self.input_producer = input_producer
        self.filter = filter

    @Slot()
    def run(self):
        def _run_selected_filter(filter, input):
            filter_widget = plugins.load_plugin('filter_widget', filter)(input)
            self.filter_widget_created.emit(filter_widget)
            filter_widget.output_ready.connect(self.output_ready)

        input = self.input or self.input_producer()
        if self.filter is None:
            selection_widget = FilterSelectionWidget(input=input)
            self.selection_widget_created.emit(selection_widget)
            selection_widget.selected.connect(_run_selected_filter)
        else:
            _run_selected_filter(self.filter, input)


class FilterWidget(QWidget):

    execute_clicked = Signal()
    output_ready = Signal(object)

    def __init__(self, parent, input):
        super().__init__(parent)
        self.input = input
