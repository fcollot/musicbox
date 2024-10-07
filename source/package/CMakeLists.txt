# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

file(GLOB_RECURSE sources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.py"
    )

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/setup.py"
    "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
    @ONLY)

if(MBOX_SYMLINK_SOURCE_PACKAGE)
    set(link_command create_symlink)
else()
    set(link_command copy_directory)
endif()

add_custom_target(mbox_package ALL
    COMMAND ${CMAKE_COMMAND} -E make_directory "${MBOX_PACKAGE_ROOT}/musicbox"
    COMMAND ${CMAKE_COMMAND} -E ${link_command} "${CMAKE_CURRENT_SOURCE_DIR}/musicbox" "${MBOX_PACKAGE_ROOT}/musicbox/musicbox"
    COMMAND ${CMAKE_COMMAND} -E copy_if_different "${CMAKE_CURRENT_BINARY_DIR}/setup.py" "${MBOX_PACKAGE_ROOT}/musicbox/"
    SOURCES ${sources}
    VERBATIM
    )

if(MBOX_VIRTUAL_ENV)
    find_package(Python 3 REQUIRED)

    if(NOT Python_FOUND)
        message(FATAL_ERROR "Cannot find Python 3 to create the virtual environment.")
    endif()

    add_custom_target(mbox_create_venv ALL
        COMMAND ${Python_EXECUTABLE} -m venv "${MBOX_VIRTUAL_ENV_ROOT}"
        VERBATIM
        )

    if(WIN32)
        set(venv_bin "${MBOX_VIRTUAL_ENV_ROOT}/Scripts")
        set(venv_python "${venv_bin}/python.exe")
    else()
        set(venv_bin "${MBOX_VIRTUAL_ENV_ROOT}/bin")
        set(venv_python "${venv_bin}/python3")
    endif()

    add_custom_target(mbox_install_venv ALL
        COMMAND "${venv_python}" -m pip install -e "${MBOX_PACKAGE_ROOT}/musicbox"
        WORKING_DIRECTORY "${venv_bin}"
        VERBATIM
        )
    add_dependencies(mbox_install_venv mbox_create_venv mbox_package)

    add_dependencies(mbox_install_venv mbox_create_venv mbox_package)

    add_custom_target(mbox_run_application
        COMMAND "${venv_python}" -m musicbox
        WORKING_DIRECTORY "${venv_bin}"
        VERBATIM
        )

    add_dependencies(mbox_run_application mbox_install_venv)

    add_custom_target(mbox_run_tests
        COMMAND "${venv_python}" -m musicbox --test
        WORKING_DIRECTORY "${venv_bin}"
        VERBATIM
        )

    add_dependencies(mbox_run_tests mbox_install_venv)

    add_test(NAME "NO GUI: MusicBox package test"
        COMMAND "${venv_python}" -m musicbox --test no-gui
        WORKING_DIRECTORY "${venv_bin}"
        )

    add_test(NAME "GUI: MusicBox package test"
        COMMAND "${venv_python}" -m musicbox --test gui
        WORKING_DIRECTORY "${venv_bin}"
        )
endif()
