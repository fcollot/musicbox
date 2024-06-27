// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include "qobject.h"

#include "../conversion.h"

bool pyncppToPython(const QObject* object, PyObject** output)
{
    bool success = true;

    try
    {
        QString className = object->metaObject()->className();
        mbox::Module pyncppQtModule = mbox::Module::import("musicbox.qt");
        mbox::Object pythonClass = pyncppQtModule.callMethod("get_class", qUtf8Printable(className));
        mbox::Object objectPointer = PyLong_FromVoidPtr(const_cast<QObject*>(object));
        mbox::Module shibokenModule = mbox::Module::import(MBOX_SHIBOKEN_PACKAGE);
        mbox::Object wrappedObject = shibokenModule.callMethod("wrapInstance", objectPointer, pythonClass);
        *output = wrappedObject.newReference();
    }
    catch (mbox::Exception& e)
    {
        mbox::raiseError(&e);
        success = false;
    }

    return success;
}

bool pyncppToCPP(PyObject* nativeObject, QObject** output)
{
    bool success = true;

    try
    {
        mbox::Module shibokenModule = mbox::Module::import(MBOX_SHIBOKEN_PACKAGE);
        mbox::Object objectPointer = shibokenModule.callMethod("getCppPointer", nativeObject)[0];
        *output = (QObject*)PyLong_AsVoidPtr(*objectPointer);
    }
    catch (mbox::Exception& e)
    {
        mbox::raiseError(&e);
        success = false;
    }

    return success;
}
