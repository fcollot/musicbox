# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION 3.19)

################################################################################
# Version
################################################################################

find_package(Git)
set(_success FALSE)

if(GIT_EXECUTABLE)
    execute_process(COMMAND ${GIT_EXECUTABLE} describe --tags --always
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        OUTPUT_VARIABLE _git_describe
        )

    if (_git_describe MATCHES "^v([0-9]+)\\.([0-9]+)(-([0-9]+))?.*$")
        set(MBOX_VERSION_MAJOR ${CMAKE_MATCH_1})
        set(MBOX_VERSION_MINOR ${CMAKE_MATCH_2})
        if(CMAKE_MATCH_4)
            set(MBOX_VERSION_PATCH ${CMAKE_MATCH_4})
        else()
            set(MBOX_VERSION_PATCH 0)
        endif()
        set(_success TRUE)
    endif()
endif()

if(_success)
    message(STATUS "MusicBox version number generated from git: ${MBOX_VERSION_MAJOR}.${MBOX_VERSION_MINOR}.${MBOX_VERSION_PATCH}")
else()
    set(MBOX_VERSION_MAJOR 0)
    set(MBOX_VERSION_MINOR 0)
    set(MBOX_VERSION_PATCH 0)
    message(WARNING "Cannot use git to generate a version number. Defaulting to 0.0.0")
endif()

################################################################################
# Project
################################################################################

set(MBOX_VERSION "${MBOX_VERSION_MAJOR}.${MBOX_VERSION_MINOR}.${MBOX_VERSION_PATCH}")

project(musicbox VERSION "${MBOX_VERSION}")

################################################################################
# CMake modules
################################################################################

include(CMakeDependentOption)
include(CTest)

################################################################################
# Settings
################################################################################

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

get_property(GENERATOR_IS_MULTI_CONFIG GLOBAL PROPERTY GENERATOR_IS_MULTI_CONFIG)

if(NOT GENERATOR_IS_MULTI_CONFIG AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

set(FETCHCONTENT_BASE_DIR "${CMAKE_BINARY_DIR}")

set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

option(MBOX_STANDALONE "Build standalone" OFF)

if(APPLE)
    cmake_dependent_option(MBOX_MACOS_BUNDLE "Build standalone as a bundle" ON "MBOX_STANDALONE" OFF)
endif()

cmake_dependent_option(MBOX_VIRTUAL_ENV "Create a virtual environment in the build directory" OFF "NOT MBOX_STANDALONE" OFF)

if(WIN32)
    string(CONCAT symlink_message
        "Use a symbolic link to the Python package in the source tree, so that"
        " modifications to the source code directly affects the packaged installed"
        " in the buile tree."
        )
    option(MBOX_SYMLINK_SOURCE_PACKAGE ${symlink_message} OFF)
else()
    option(MBOX_USE_QT5 "Use Qt5 instead of Qt6" OFF)
endif()

if(MBOX_USE_QT5)
    set(MBOX_QT_PACKAGE "Qt5")
    set(MBOX_PYSIDE_PACKAGE "PySide2")
    set(MBOX_SHIBOKEN_PACKAGE "shiboken2")
else()
    set(MBOX_QT_PACKAGE "Qt6")
    set(MBOX_PYSIDE_PACKAGE "PySide6")
    set(MBOX_SHIBOKEN_PACKAGE "shiboken6")
endif()

################################################################################
# Paths
################################################################################

set(MBOX_ROOT_BASE "${CMAKE_CURRENT_BINARY_DIR}")
set(MBOX_ROOT "${MBOX_ROOT_BASE}/$<CONFIG>")
set(MBOX_PACKAGE_ROOT "${MBOX_ROOT}/packages")
set(MBOX_VIRTUAL_ENV_ROOT "${MBOX_ROOT}/venv")

if(UNIX)
    if(APPLE AND MBOX_MACOS_BUNDLE)
        set(contents_subdir "MusicBox.app/Contents")
        set(MBOX_STANDALONE_LIBRARY_SUBDIR "${contents_subdir}/Frameworks")
        set(MBOX_STANDALONE_RUNTIME_SUBDIR "${contents_subdir}/MacOS")
    else()
        set(MBOX_STANDALONE_RUNTIME_SUBDIR "bin")
        set(MBOX_STANDALONE_LIBRARY_SUBDIR "lib")
    endif()

    set(MBOX_PACKAGE_RUNTIME_SUBDIR "bin")
    set(MBOX_PACKAGE_LIBRARY_SUBDIR "lib")
    set(MBOX_PACKAGE_ARCHIVE_SUBDIR "lib")
    set(MBOX_PACKAGE_SHARE_SUBDIR "share/cmake/mbox")
else()
    set(MBOX_STANDALONE_RUNTIME_SUBDIR "bin")
    set(MBOX_STANDALONE_LIBRARY_SUBDIR "bin")
    set(MBOX_PACKAGE_RUNTIME_SUBDIR "bin")
    set(MBOX_PACKAGE_LIBRARY_SUBDIR "bin")
    set(MBOX_PACKAGE_ARCHIVE_SUBDIR "libs")
    set(MBOX_PACKAGE_SHARE_SUBDIR "cmake")
endif()

set(MBOX_PACKAGE_INCLUDE_SUBDIR "include")

################################################################################
# Subdirectories
################################################################################

add_subdirectory(source)
