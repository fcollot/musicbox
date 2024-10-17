# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Python package
################################################################################

file(GLOB_RECURSE sources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.py"
    )

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/setup.py"
    "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
    @ONLY)

if(UNIX OR MED_SYMLINK_SOURCE_PACKAGE)
    set(link_command create_symlink)
else()
    set(link_command copy_directory)
endif()

add_custom_target(med_package ALL
    COMMAND ${CMAKE_COMMAND} -E make_directory "${MED_PACKAGE_ROOT}/pymedinria"
    COMMAND ${CMAKE_COMMAND} -E rm -rf "${MED_PACKAGE_ROOT}/pymedinria/pymedinria"
    COMMAND ${CMAKE_COMMAND} -E ${link_command} "${CMAKE_CURRENT_SOURCE_DIR}/pymedinria" "${MED_PACKAGE_ROOT}/pymedinria/pymedinria"
    COMMAND ${CMAKE_COMMAND} -E copy_if_different "${CMAKE_CURRENT_BINARY_DIR}/setup.py" "${MED_PACKAGE_ROOT}/pymedinria/"
    SOURCES ${sources}
    VERBATIM
    )

################################################################################
# Virtual env
################################################################################

if(MED_VIRTUAL_ENV)
    find_package(Python 3 REQUIRED)

    if(NOT Python_FOUND)
        message(FATAL_ERROR "Cannot find Python 3 to create the virtual environment.")
    endif()

    add_custom_target(med_create_venv ALL
        COMMAND ${Python_EXECUTABLE} -m venv --without-pip "${MED_VIRTUAL_ENV_ROOT}"
        VERBATIM
        )

    if(WIN32)
        set(venv_bin "${MED_VIRTUAL_ENV_ROOT}/Scripts")
        set(venv_python "${venv_bin}/python.exe")
    else()
        set(venv_bin "${MED_VIRTUAL_ENV_ROOT}/bin")
        set(venv_python "${venv_bin}/python3")
    endif()

    add_custom_target(med_install_venv ALL
        COMMAND "${venv_python}" -m ensurepip
        COMMAND "${venv_python}" -m pip install build
        COMMAND "${venv_python}" -m pip install -e "${MED_PACKAGE_ROOT}/pymedinria"
        WORKING_DIRECTORY "${venv_bin}"
        VERBATIM
        )

    add_dependencies(med_install_venv med_create_venv med_package)

    ############################################################################
    # Runner targets
    ############################################################################

    add_custom_target(med_run_application
        COMMAND "${venv_python}" -m pymedinria
        WORKING_DIRECTORY "${venv_bin}"
        VERBATIM
        )

    add_dependencies(med_run_application med_install_venv)

    add_custom_target(med_run_tests
        COMMAND "${venv_python}" -m pymedinria --test
        WORKING_DIRECTORY "${venv_bin}"
        VERBATIM
        )

    add_dependencies(med_run_tests med_install_venv)
    
    ############################################################################
    # Distribution
    ############################################################################

    add_custom_target(med_build_distribution ALL
        COMMAND "${venv_python}" -m build "${MED_PACKAGE_ROOT}/pymedinria"
        WORKING_DIRECTORY "${venv_bin}"
        VERBATIM
        )
        
    add_dependencies(med_build_distribution med_install_venv)

    ############################################################################
    # CTest
    ############################################################################

    add_test(NAME ${PROJECT_NAME}_no_gui
        COMMAND "${venv_python}" -m pymedinria --test no-gui
        WORKING_DIRECTORY "${venv_bin}"
        )

    add_test(NAME ${PROJECT_NAME}_gui
        COMMAND "${venv_python}" -m pymedinria --test gui
        WORKING_DIRECTORY "${venv_bin}"
        )

    set_property(TEST ${PROJECT_NAME}_no_gui PROPERTY LABELS TEST_NO_GUI)
    set_property(TEST ${PROJECT_NAME}_gui PROPERTY LABELS TEST_GUI)

endif()
