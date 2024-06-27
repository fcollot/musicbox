# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Settings
################################################################################

if(APPLE)
    set(PYNCPP_MACOS_BUNDLE ${MBOX_MACOS_BUNDLE} CACHE BOOL "")
    set(PYNCPP_MACOS_BUNDLE_NAME "${MBOX_APPLICATION_NAME}" CACHE STRING "")
endif()

################################################################################
# Fetch content
################################################################################

FetchContent_Declare(
    pyncpp
    GIT_REPOSITORY "https://github.com/fcollot/pyncpp.git"
    GIT_TAG integration
    GIT_SHALLOW False
    GIT_PROGRESS True
    )

FetchContent_MakeAvailable(pyncpp)
