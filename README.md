*Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.*

# pyMedInria

A platform to develop ITK and VTK tools in Python for medInria and associated projects.

## Contents

* [Description](#description)
* [License](#license)
* [How to build](#how-to-build)
  * [Prerequisites](#prerequisites)
  * [Building the package](#building-the-package)
  * [Building the standalone](#building-the-standalone)
* [How to test](#how-to-test)
* [How to run](#how-to-run)
* [How to install](#how-to-install)

## Description

The platform consists of:

- a Python package containing the core components, an API for higher-level development, a Qt-based GUI library and a runnable application.
- an (optional) standalone application that wraps the Python application with an embedded interpreter.

*(This project is still under construction and most of these features are not fully implemented)*

The Python package will be available on PyPi in the near future.

## License

See [LICENSE-BSD-3-Clause](LICENSE-BSD-3-Clause.txt)

## How to build

### Prerequisites

#### Necessary:

Currently ony CMake >= 3.19 is necessary.

#### Optional:

Python >= 3.10 is required if the option to setup a virtual environment in the build tree is chosen.

If the option to build the standalone is chosen, a custom CPython interpreter will be built. The requirements for that can be found [here](https://github.com/python/cpython?tab=readme-ov-file#build-instructions).

#### Building the package:

Using CMake only (from the build directory):

```
cmake [<options>] <path-to-source-directory>
cmake --build .
```

The Python dstribution packages will be located at `<build_directory>/<build_type>/packages/pymedinria/dist`
(When not using a multi-config generator the default build type is `Release`)

To install a virtual environment in the build tree, set the `MED_VIRTUAL_ENV` cmake option to `TRUE`.

#### Building the standalone:

Follow the steps to build the Python package, but set the `MED_STANDALONE` cmake option to `TRUE`.

(*The standalone is not yet available*)

## How to test:

* Using CTest:

`ctest --verbose`

* Using the virtual environment:

`<build_directory>/<build_type>/venv/bin/python -m pymedinria --test all`\
(on Windows the path is `<build_directory>/<build_type>/venv/Scripts/python.exe`)

* Using the standalone (*not yet available*):

`./pymedinria --test all`

* From Python:

```
from pymedinria import dev
dev.run_tests()
```

## How to run:

* Using CMake:

```
cmake --build --target mbox_run_application
```

* Using the virtual environment:

`<build_directory>/<build_type>/venv/bin/python -m pymedinria`
(on Windows the path is `<build_directory>/<build_type>/venv/Scripts/python.exe`)

* Using the standalone (*not yet available*):

`./pymedinria`

* From Python:

```
from pymedinria import app
app.run()
```


## How to install

#### Python package:

Install one of the distribution packages using pip.
They are located at `<build_directory>/<build_type>/packages/pymedinria/dist`.

#### Standalone:

Not yet available.
