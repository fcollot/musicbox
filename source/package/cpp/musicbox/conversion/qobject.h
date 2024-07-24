// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#ifndef MBOX_QT_QOBJECT_H
#define MBOX_QT_QOBJECT_H

#include "../external/pyncpp.h"

#include <type_traits>

#include <QObject>

#include "../export.h"

MBOX_EXPORT bool pyncppToPython(const QObject* object, PyObject** output);
MBOX_EXPORT bool pyncppToCPP(PyObject* nativeObject, QObject** output);

template <class TYPE, typename = std::enable_if_t<std::is_base_of_v<QObject, TYPE> > >
MBOX_EXPORT bool pyncppToCPP(PyObject* nativeObject, TYPE** output)
{
    return pyncppToCPP(nativeObject, (QObject**)(output));
}

#endif // MBOX_QT_QOBJECT_H
