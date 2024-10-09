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

    ############################################################################
    # CTest
    ############################################################################

    add_test(NAME ${PROJECT_NAME}_no_gui
        COMMAND "${venv_python}" -m musicbox --test no-gui
        WORKING_DIRECTORY "${venv_bin}"
        )

    add_test(NAME ${PROJECT_NAME}_gui
        COMMAND "${venv_python}" -m musicbox --test gui
        WORKING_DIRECTORY "${venv_bin}"
        )

    set_property(TEST ${PROJECT_NAME}_no_gui PROPERTY LABELS TEST_NO_GUI)
    set_property(TEST ${PROJECT_NAME}_gui PROPERTY LABELS TEST_GUI)

endif()
