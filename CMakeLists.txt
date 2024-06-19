# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION 3.19)

include(CMakePackageConfigHelpers)
include(ExternalProject)

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

    if (_git_describe MATCHES "^v\\.([0-9]+)\\.([0-9]+)(-([0-9]+))?.*$")
        set(MBX_VERSION_MAJOR ${CMAKE_MATCH_1})
        set(MBX_VERSION_MINOR ${CMAKE_MATCH_2})
        if(CMAKE_MATCH_4)
            set(MBX_VERSION_PATCH ${CMAKE_MATCH_4})
        else()
            set(MBX_VERSION_PATCH 0)
        endif()
        set(_success TRUE)
    endif()
endif()

if(_success)
    message(STATUS "Version number generated from git: ${MBX_VERSION_MAJOR}.${MBX_VERSION_MINOR}.${MBX_VERSION_PATCH}")
else()
    set(MBX_VERSION_MAJOR 0)
    set(MBX_VERSION_MINOR 0)
    set(MBX_VERSION_PATCH 0)
    message(WARNING "Cannot use git to generate a version number. Defaulting to 0.0.0")
endif()

################################################################################
# Project
################################################################################

set(MBX_VERSION "${MBX_VERSION_MAJOR}.${MBX_VERSION_MINOR}.${MBX_VERSION_PATCH}")
project(musicbox VERSION "${MBX_VERSION}")

################################################################################
# Settings
################################################################################

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

get_property(GENERATOR_IS_MULTI_CONFIG GLOBAL PROPERTY GENERATOR_IS_MULTI_CONFIG)

if(NOT GENERATOR_IS_MULTI_CONFIG AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE RelWithDebInfo)
endif()

set(MBX_APPLICATION_NAME MusicBox CACHE STRING "The name of the standalone or embedding application")

if(APPLE)
    option(MBX_MACOS_BUNDLE "Build as a bundle" ON)
    set(MBX_MACOS_BUNDLE_NAME "mbox" CACHE STRING "")
endif()

set(MBX_STANDALONE TRUE CACHE STRING "Build standalone application")

################################################################################
# Paths
################################################################################

set(MBOX_ROOT "${CMAKE_BINARY_DIR}/$<CONFIG>")

if(UNIX)
    if(APPLE AND MBOX_MACOS_BUNDLE)
        set(contents_subdir "${MBOX_MACOS_BUNDLE_NAME}.app/Contents")
        set(MBOX_RUNTIME_SUBDIR "${contents_subdir}/MacOS")
        set(MBOX_LIBRARY_SUBDIR "${contents_subdir}/Frameworks")
    else()
        set(MBOX_RUNTIME_SUBDIR "bin")
        set(MBOX_LIBRARY_SUBDIR "lib")
    endif()

    set(MBOX_ARCHIVE_SUBDIR "lib")
    set(MBOX_SHARE_SUBDIR "share/cmake/mbox")
else()
    set(MBOX_RUNTIME_SUBDIR "bin")
    set(MBOX_LIBRARY_SUBDIR "bin")
    set(MBOX_ARCHIVE_SUBDIR "libs")
    set(MBOX_SHARE_SUBDIR "cmake")
endif()

set(MBOX_INCLUDE_SUBDIR "include")
set(MBOX_UTILS_SUBDIR "bin")
