# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, Signal, Slot
else:
    from PySide6.QtCore import QObject, Signal, Slot


class Messenger(QObject):

    user_info = Signal(str)
    user_warning = Signal(str)
    user_alert = Signal(str)
    internal_info = Signal(str)
    internal_warning = Signal(str)
    internal_alert = Signal(str)

    @Slot(str)
    def inform_user(self, message):
        self.user_info.emit(message)

    @Slot(str)
    def inform_internal(self, message):
        self.internal_info.emit(message)

    @Slot(str)
    def inform(self, message):
        self.inform_user(message)
        self.inform_internal(message)

    @Slot(str)
    def warn_user(self, message):
        self.user_warning.emit(message)

    @Slot(str)
    def warn_internal(self, message):
        self.internal_warning.emit(message)

    @Slot(str)
    def warn(self, message):
        self.warn_user(message)
        self.warn_internal(message)

    @Slot(str)
    def alert_user(self, message):
        self.user_alert.emit(message)

    @Slot(str)
    def alert_internal(self, message):
        self.internal_alert.emit(message)

    @Slot(str)
    def alert(self, message):
        self.alert_user(message)
        self.alert_internal(message)
