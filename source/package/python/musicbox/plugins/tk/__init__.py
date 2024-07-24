# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import tkinter as tk
from musicbox import plugins


class Gui():

    def __init__(self):
        self._init_enums()
        self.Action = Action
        self.Application = Application
        self.DockWidget = DockWidget
        self.Label = Label
        self.LineEdit = LineEdit
        self.MainWindow = MainWindow
        self.ScrollArea = ScrollArea
        self.Signal = Signal
        self.Slot = Slot
        self.VBoxLayout = VBoxLayout
        self.Widget = Widget

    def _init_enums(self):
        self._add_enum('AlignBottom')
        self._add_enum('LeftDockWidgetArea')
        self._add_enum('PlainText')

    def _add_enum(self, name):
        setattr(self, name, name)

    def app(self):
        return Application.instance

    def run(self):
        self.app().native.mainloop()


class Signal():

    def __init__(self, *arg_types):
        self.arg_types = arg_types
        self._connections = []

    def clone(self):
        return Signal(self.arg_types)

    def connect(self, reciever):
        self._connections.append(reciever)

    def emit(*args):
        for connection in self._connections:
            connection(*args)


def Slot(*args):
    def decorator(function):
        return function
    return decorator


class TkObject():

    def __init__(self):
        self.native = None
        self.delayed_calls = []
        for key, value in vars(self.__class__).items():
            if isinstance(value, Signal):
                setattr(self, key, value.clone())
        self.set_unused(
            'setAlignment',
            'setEnabled',
            'setFocusProxy',
            'setSpacing',
            'setWordWrap',
        )

    def create(self, *args, **kwargs):
        print(f'creating {self.native_class}: {args} {kwargs}')
        self.native = self.native_class(*args, **kwargs)
        for call in self.delayed_calls:
            function, args, kwargs = call
            getattr(self.native, function)(*args, **kwargs)

    def native_call(self, function, *args, **kwargs):
        if self.native is not None:
            getattr(self.native, function)(*args, **kwargs)
        else:
            self.delayed_calls.append((function, args, kwargs))

    def set_unused(self, *functions):
        for function in functions:
            setattr(self, function, self.unused_function)

    def unused_function(self, *args, **kwargs):
        pass


class Widget(TkObject):

    native_class = tk.Frame

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    def create(self, parent):
        super().create(parent, *self.args, **self.kwargs)

    def setLayout(self, layout):
        self._layout = layout

    def layout(self):
        return self._layout

    def showMaximized(self):
        self.native_call('state', 'zoomed')

    def setWindowTitle(self, title):
        self.native_call('title', title)

    def resize(self, width, height):
        self.native_call('geometry', f'{width}x{height}')

    def setEnabled(self, enabled):
        if enabled:
            self.native_call('state', 'enable')
        else:
            self.native_call('state', 'disable')


class Application(TkObject):

    instance = None

    def __init__(self, argv=None):
        super().__init__()
        self.native = tk.Tk()
        self.__class__.instance = self

    def setApplicationName(self, name):
        self.native_call('title', name)


class Layout(TkObject):

    def __init__(self):
        super().__init__()
        self.frame = tk.Frame()


class VBoxLayout(Layout):

    def addWidget(self, widget):
        widget.create(self.frame)
        widget.native.pack(side=tk.TOP)


class Action(TkObject):

    triggered = Signal()

    def __init__(self, name, parent=None):
        super().__init__()
        self.name = name


class Label(Widget):

    native_class = tk.Label

    def __init__(self, text=None):
        super().__init__(text=text)
        self.set_unused(
            'setTextFormat',
        )


class DockWidget(Widget):

    native_class = tk.Frame

    def __init__(self, title):
        super().__init__()
        self.title = title


class LineEdit(Widget):

    native_class = tk.Entry
    returnPressed = Signal()

    def __init__(self):
        super().__init__()


class ScrollArea(Widget):

    native_class = tk.Canvas

    def __init__(self):
        super().__init__()
        self.set_unused(
            'setWidgetResizable',
        )
        self.hscroll_bar = ScrollBar()
        self.vscroll_bar = ScrollBar()

    def create(self, parent):
        self.hscroll_bar.create(parent)
        self.vscroll_bar.create(parent)
        self.kwargs |= {
            'xscrollcommand': self.hscroll_bar.native,
            'yscrollcommand': self.vscroll_bar.native,
        }
        super().create(parent)
        self.widget.create(self.native)

    def setWidget(self, widget):
        self.widget = widget

    def horizontalScrollBar(self):
        return self.hscroll_bar

    def verticalScrollBar(self):
        return self.vscroll_bar


class ScrollBar(TkObject):

    native_class = tk.Scrollbar
    rangeChanged = Signal()

    def __init__(self):
        super().__init__()
        self.set_unused(
            'setValue',
        )


class Menu(TkObject):

    def __init__(self):
        super().__init__()
        self.native = None

    def create(self, parent):
        self.native = tk.Menu(parent)

    def addMenu(self, name):
        menu = Menu()
        menu.create(self.native)
        self.native_call('add_cascade', label=name, menu=menu)
        return menu

    def addAction(self, action):
        self.native_call('add_command', label=action.name, command=action.triggered.emit)


class MainWindow(Widget):

    def __init__(self):
        super().__init__()
        self.native = Application.instance.native
        self.frame = tk.Frame(self.native)
        self.central_area = tk.Frame(self.frame)
        self.dock_areas = {
            'LeftDockWidgetArea': tk.Frame(self.frame)
        }

    def menuBar(self):
        menu_bar = Menu()
        menu_bar.create(self.native)
        return menu_bar

    def setCentralWidget(self, widget):
        self.central_widget = widget
        widget.create(self.central_area)
        
    def addDockWidget(self, dock_area, widget):
        widget.create(self.dock_areas[dock_area])
