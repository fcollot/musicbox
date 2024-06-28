# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Dependencies
################################################################################

set(qt_components
    Core
    Widgets
    )

find_package(Qt${MBOX_QT_VERSION_MAJOR} REQUIRED COMPONENTS ${qt_components})

################################################################################
# Files
################################################################################

set(headers
    musicbox.h
    musicbox/conversion.h
    musicbox/conversion/qobject.h
    musicbox/gui.h
    musicbox/gui/console.h
    )

set(sources
    musicbox/conversion/qobject.cpp
    musicbox/gui/console.cpp
    )

################################################################################
# Library
################################################################################

add_library(mbox_cpp_api SHARED
    ${headers}
    ${sources}
    )

add_dependencies(mbox_cpp_api mbox_python_packages)

################################################################################
# Compile definitions
################################################################################

target_compile_definitions(mbox_cpp_api PUBLIC
    MBOX_QT_VERSION_MAJOR=${MBOX_QT_VERSION_MAJOR}
    MBOX_SHIBOKEN_PACKAGE="shiboken${MBOX_PYSIDE_VERSION_MAJOR}"
    )

################################################################################
# Includes
################################################################################

set(qt_includes)

foreach(component ${qt_components})
    get_target_property(qt_include Qt${MBOX_QT_VERSION_MAJOR}::${component} INTERFACE_INCLUDE_DIRECTORIES)
    list(APPEND qt_includes "${qt_include}")
endforeach()

list(REMOVE_DUPLICATES qt_includes)

target_include_directories(mbox_cpp_api
    PRIVATE
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>/mbox"
    PUBLIC
    ${qt_includes}
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>"
    "$<INSTALL_INTERFACE:${MBOX_INCLUDE_SUBDIR}/musicbox>"
    )

################################################################################
# Link
################################################################################

set(qt_libraries)

if(MBOX_USE_QT5)
    set(version_subdir 5)
else()
    set(version_subdir A)
endif()

foreach(component ${qt_components})
    if(APPLE)
        set(library "Qt${component}.framework/Versions/${version_subdir}/Qt${component}")
    else()
        set(library "Qt${component}${CMAKE_SHARED_LIBRARY_SUFFIX}")
    endif()

    if(WIN32)
        set(library_dir "${MBOX_ROOT}/${PYNCPP_PYTHON_SUBDIR}/lib/site-packages")
    else()
        set(library_dir "${MBOX_ROOT}/${PYNCPP_PYTHON_SUBDIR}/lib/python${PYNCPP_PYTHON_VERSION_MAJOR}.${PYNCPP_PYTHON_VERSION_MINOR}/site-packages")
    endif()

    string(APPEND library_dir "/PySide${MBOX_PYSIDE_VERSION_MAJOR}/Qt/lib")

    list(APPEND qt_libraries "${library_dir}/${library}")
endforeach()

target_link_libraries(mbox_cpp_api PUBLIC
    pyncpp_cpp_api
    ${qt_libraries}
    )

################################################################################
# Install/Export
################################################################################

install(TARGETS mbox_cpp_api
    EXPORT mbox_cpp_api_export

    RUNTIME
    DESTINATION "${MBOX_RUNTIME_SUBDIR}"
    COMPONENT Runtime

    LIBRARY
    DESTINATION "${MBOX_LIBRARY_SUBDIR}"
    COMPONENT Runtime

    ARCHIVE
    DESTINATION "${MBOX_ARCHIVE_SUBDIR}"
    )

install(EXPORT mbox_cpp_api_export
    DESTINATION "${MBOX_SHARE_SUBDIR}"
    )

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/"
    DESTINATION "${MBOX_INCLUDE_SUBDIR}/musicbox"
    FILES_MATCHING PATTERN "*.h"
    PATTERN "CMakeLists.txt" EXCLUDE
    )
