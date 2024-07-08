# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Files
################################################################################

set(sources
    main.cpp
    )

################################################################################
# Library
################################################################################

add_executable(mbox_executable_cpp
    ${sources}
    )

################################################################################
# Target properties
################################################################################

if(UNIX)
    set(rpath ${CMAKE_INSTALL_RPATH})

    if(APPLE)
        set(rpath_prefix "@executable_path")
    else()
        set(rpath_prefix "\$ORIGIN")
    endif()

    file(RELATIVE_PATH relative_lib_dir "/${MBOX_STANDALONE_RUNTIME_SUBDIR}" "/${MBOX_STANDALONE_LIBRARY_SUBDIR}")
    list(APPEND rpath "${rpath_prefix}/${relative_lib_dir}")

    file(RELATIVE_PATH relative_lib_dir "/${MBOX_PACKAGE_RUNTIME_SUBDIR}" "/packages/musicbox/${MBOX_PACKAGE_LIBRARY_SUBDIR}")
    list(APPEND rpath "${rpath_prefix}/${relative_lib_dir}")

    if(WIN32)
        set(qt_lib_dir "${PYNCPP_PYTHON_SUBDIR}/lib/site-packages")
    else()
        set(qt_lib_dir "${PYNCPP_PYTHON_SUBDIR}/lib/python${PYNCPP_PYTHON_VERSION_MAJOR}.${PYNCPP_PYTHON_VERSION_MINOR}/site-packages")
    endif()

    string(APPEND qt_lib_dir "/${MBOX_PYSIDE_PACKAGE}/Qt/lib")
    file(RELATIVE_PATH relative_qt_lib_dir "/${MBOX_STANDALONE_RUNTIME_SUBDIR}" "/${qt_lib_dir}")
    list(APPEND rpath "${rpath_prefix}/${relative_qt_lib_dir}")

    set_target_properties(mbox_executable_cpp PROPERTIES
        INSTALL_RPATH "${rpath}"
        )
endif()

set_target_properties(mbox_executable_cpp PROPERTIES
    OUTPUT_NAME MusicBox
    RUNTIME_OUTPUT_DIRECTORY "${MBOX_ROOT}/${MBOX_STANDALONE_RUNTIME_SUBDIR}"
    LIBRARY_OUTPUT_DIRECTORY "${MBOX_ROOT}/${MBOX_STANDALONE_LIBRARY_SUBDIR}"
    ARCHIVE_OUTPUT_DIRECTORY "${MBOX_ROOT}/${MBOX_STANDALONE_ARCHIVE_SUBDIR}"
    )

################################################################################
# Compile definitions
################################################################################

file(RELATIVE_PATH relative_python_dir "/${MBOX_STANDALONE_RUNTIME_SUBDIR}" "/${PYNCPP_PYTHON_SUBDIR}")

target_compile_definitions(mbox_executable_cpp PUBLIC
    PYTHON_HOME="${relative_python_dir}"
    )

################################################################################
# Link
################################################################################

target_link_libraries(mbox_executable_cpp PUBLIC
    mbox_library_cpp
    )

if(MBOX_USE_QT5)
    set(qt_package Qt5)
    set(version_subdir 5)
else()
    set(qt_package Qt6)
    set(version_subdir A)
endif()

#add_custom_target(foo2 ALL
#    COMMAND ${CMAKE_INSTALL_NAME_TOOL} -change
#    $<TARGET_FILE:${qt_package}::Core>
#    "@rpath/QtCore.framework/Versions/${version_subdir}/QtCore"
#    $<TARGET_FILE:mbox_executable_cpp>
#    COMMAND ${CMAKE_INSTALL_NAME_TOOL} -change
#    $<TARGET_FILE:${qt_package}::Widgets>
#    "@rpath/QtWidgets.framework/Versions/${version_subdir}/QtWidgets"
#    $<TARGET_FILE:mbox_executable_cpp>
#    COMMAND ${CMAKE_INSTALL_NAME_TOOL} -change
#    $<TARGET_FILE:${qt_package}::Gui>
#    "@rpath/QtGui.framework/Versions/${version_subdir}/QtGui"
#    $<TARGET_FILE:mbox_executable_cpp>
#    VERBATIM
#    )

set_qt_paths(mbox_executable_cpp)

################################################################################
# Install/Export
################################################################################

install(TARGETS mbox_executable_cpp
    RUNTIME
    DESTINATION "${MBOX_RUNTIME_SUBDIR}"
    )
