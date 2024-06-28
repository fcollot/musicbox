# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

cmake_minimum_required(VERSION 3.19)

include(CMakePackageConfigHelpers)
include(FetchContent)

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
    message(STATUS "Version number generated from git: ${MBOX_VERSION_MAJOR}.${MBOX_VERSION_MINOR}.${MBOX_VERSION_PATCH}")
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
# Settings
################################################################################

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

get_property(GENERATOR_IS_MULTI_CONFIG GLOBAL PROPERTY GENERATOR_IS_MULTI_CONFIG)

if(NOT GENERATOR_IS_MULTI_CONFIG AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

set(FETCHCONTENT_BASE_DIR "${CMAKE_BINARY_DIR}")

if(APPLE)
    option(MBOX_MACOS_BUNDLE "Build as a bundle" ON)
endif()

option(MBOX_STANDALONE "Build standalone application" ON)

set(MBOX_APPLICATION_NAME "NoName" CACHE STRING "The name of the embedding application")

if(APPLE AND MBOX_MACOS_BUNDLE)
    if(MBOX_STANDALONE)
        set(MBOX_MACOS_BUNDLE_NAME "MusicBox")
    else()
        set(MBOX_MACOS_BUNDLE_NAME "${MBOX_APPLICATION_NAME}")
endif()

option(MBOX_USE_QT5 "Build with Qt5 instead of Qt6" OFF)

if(MBOX_USE_QT5)
    set(qt_package Qt5)
else()
    set(qt_package Qt6)
endif()

find_package(${qt_package} REQUIRED)

################################################################################
# Paths
################################################################################

set(MBOX_ROOT_BASE "${CMAKE_CURRENT_BINARY_DIR}")
set(MBOX_ROOT "${MBOX_ROOT_BASE}/$<CONFIG>")

if(UNIX)
    if(APPLE AND MBOX_MACOS_BUNDLE)
        set(contents_subdir "${MBOX_MACOS_BUNDLE_NAME}.app/Contents")
        set(library_subdir "${contents_subdir}/Frameworks")

        if(MBOX_STANDALONE)
            set(runtime_subdir "${contents_subdir}/MacOS")
        else()
            set(runtime_subdir "bin")
        endif()
    else()
        set(runtime_subdir "bin")
        set(library_subdir "lib")
    endif()

    set(archive_subdir "lib")
    set(share_subdir "share/cmake/mbox")
else()
    set(runtime_subdir "bin")
    set(library_subdir "bin")
    set(archive_subdir "libs")
    set(share_subdir "cmake")
endif()

set(MBOX_RUNTIME_SUBDIR "${runtime_subdir}" CACHE PATH "")
set(MBOX_LIBRARY_SUBDIR "${library_subdir}" CACHE PATH "")
set(MBOX_ARCHIVE_SUBDIR "${archive_subdir}" CACHE PATH "")
set(MBOX_SHARE_SUBDIR "${share_subdir}" CACHE PATH "")
set(MBOX_INCLUDE_SUBDIR "include" CACHE PATH "")
set(MBOX_UTILS_SUBDIR "bin" CACHE PATH "")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${MBOX_ROOT}/${MBOX_RUNTIME_SUBDIR}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${MBOX_ROOT}/${MBOX_LIBRARY_SUBDIR}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${MBOX_ROOT}/${MBOX_ARCHIVE_SUBDIR}")

################################################################################
# Subdirectories
################################################################################

add_subdirectory(pyncpp)
add_subdirectory(packages)
add_subdirectory(source)
