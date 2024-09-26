# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

file(GLOB_RECURSE sources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.py"
    )

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/setup.py"
    "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
    @ONLY)

add_custom_target(mbox_package ALL
    COMMAND ${CMAKE_COMMAND} -E make_directory "${MBOX_PACKAGE_ROOT}/musicbox"
    COMMAND ${CMAKE_COMMAND} -E create_symlink "${CMAKE_CURRENT_SOURCE_DIR}/musicbox" "${MBOX_PACKAGE_ROOT}/musicbox/musicbox"
    COMMAND ${CMAKE_COMMAND} -E copy_if_different "${CMAKE_CURRENT_BINARY_DIR}/setup.py" "${MBOX_PACKAGE_ROOT}/musicbox/"
    SOURCES ${sources}
    VERBATIM
    )

if(MBOX_VIRTUAL_ENV)
    find_package(Python 3 REQUIRED)

    add_custom_target(mbox_create_venv ALL
        COMMAND ${Python_EXECUTABLE} -m venv "${MBOX_VIRTUAL_ENV_ROOT}"
        VERBATIM
        )

    add_custom_target(mbox_install_venv ALL
        COMMAND "${MBOX_VIRTUAL_ENV_ROOT}/bin/python3" -m pip install -e "${MBOX_PACKAGE_ROOT}/musicbox"
        WORKING_DIRECTORY "${MBOX_VIRTUAL_ENV_ROOT}/bin"
        VERBATIM
        )
endif()
