// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include <musicbox.h>

#include <QApplication>
#include <QDebug>
#include <QMainWindow>

int main(int argc, char** argv)
{
    int exitStatus = EXIT_SUCCESS;

    mbox::Manager::setPythonHome(PYTHON_HOME);
    mbox::Manager::setCommandLineArguments(argc, argv);
    mbox::Manager& pyncppManager = mbox::Manager::instance();

    if (pyncppManager.errorOccured())
    {
       qCritical() << QString("Python initialization error: %1").arg(pyncppManager.errorMessage());
       exitStatus = EXIT_FAILURE;
    }
    else
    {
        try
        {
            QApplication app(argc, argv);
            mbox::Module::import("musicbox.executable").callMethod("init");
            exitStatus = app.exec();
        }
        catch (mbox::Exception& e)
        {
            qCritical() << "Python error: " << e.what();
            exitStatus = EXIT_FAILURE;
        }
    }

    mbox::Manager::destroyInstance();
    return exitStatus;
}
