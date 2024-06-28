// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include "console.h"

#include "../conversion.h"

namespace mbox
{

Object newQtConsole(QWidget* parent)
{
    Object consoleClass = Module::import("mbox.qt.console").attribute("Console");
    Object console = consoleClass();
    console.callMethod("run");
    QWidget* consoleWidget = console.toCPP<QWidget*>();
    consoleWidget->setParent(parent);
    return console;
}

}
