# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import enum


class Gui():

    def __init__(self):
        self._symbols = {}

        #        if config.pyside_version == 2:
        #            from PySide2 import QtCore, QtGui, QtWidgets
        #        else:
        from PySide6 import QtCore, QtGui, QtWidgets

        self._import_core_module(QtCore)
        self._import_gui_module(QtGui)
        self._import_widgets_module(QtWidgets)

    def _import_core_module(self, core):
        self._symbols['Object'] = core.QObject
        self._symbols['Event'] = core.QEvent
        self._symbols['Signal'] = core.Signal
        self._symbols['Slot'] = core.Slot
        self._symbols['Settings'] = core.QSettings
        self._import_enums(core.Qt)
        self._import_objects(core)

    def _import_gui_module(self, gui):
        self._import_objects(gui)
        self._symbols['Color'] = gui.QColor
        self._symbols['Pixmap'] = gui.QPixmap

    def _import_widgets_module(self, widgets):
        self._import_objects(widgets)
        self._symbols['SizePolicy'] = widgets.QSizePolicy

    def _import_enums(self, target):
        for name in dir(target): ## use vars
            thing = getattr(target, name)
            if isinstance(thing, enum.EnumMeta):
                for enum_member in thing:
                    self._symbols[enum_member.name] = enum_member

    def _import_objects(self, module):
        for name in dir(module):
            thing = getattr(module, name)
            if isinstance(thing, type) and issubclass(thing, self._symbols['Object']):
                self._symbols[name[1:]] = thing

    def symbols(self):
        return self._symbols

    def run(self):
        #        if config.pyside_version == 2:
        #            return self.app().exec_()
        #        else:
        return  self._symbols['Application'].instance().exec()
