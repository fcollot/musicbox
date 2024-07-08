# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Settings
################################################################################

set(PYNCPP_BUILD_EMBEDDABLE_PYTHON ${MBOX_BUILD_EMBEDDABLE_PYTHON} CACHE BOOL "")

set(PYNCPP_RUNTIME_SUBDIR "packages/musicbox/${MBOX_PACKAGE_RUNTIME_SUBDIR}" CACHE PATH "")
set(PYNCPP_LIBRARY_SUBDIR "packages/musicbox/${MBOX_PACKAGE_LIBRARY_SUBDIR}" CACHE PATH "")
set(PYNCPP_ARCHIVE_SUBDIR "packages/musicbox/${MBOX_PACKAGE_ARCHIVE_SUBDIR}" CACHE PATH "")

################################################################################
# Fetch content
################################################################################

FetchContent_Declare(
    pyncpp
    GIT_REPOSITORY "https://github.com/fcollot/pyncpp.git"
    GIT_TAG integration2
    GIT_SHALLOW False
    GIT_PROGRESS True
    )

FetchContent_MakeAvailable(pyncpp)
