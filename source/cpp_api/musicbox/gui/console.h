// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#ifndef MBOX_QT_CONSOLE_H
#define MBOX_QT_CONSOLE_H

#include "../external/pyncpp.h"

#include <QWidget>

#include "../export.h"

namespace mbox
{

MBOX_EXPORT Object newQtConsole(QWidget* parent = nullptr);

}

#endif // MBOX_QT_CONSOLE_H
