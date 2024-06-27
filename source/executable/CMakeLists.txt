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

add_executable(mbox_executable
    ${sources}
    )

################################################################################
# Target properties
################################################################################

if(UNIX)
    file(RELATIVE_PATH relative_lib_dir "/${MBOX_RUNTIME_SUBDIR}" "/${MBOX_LIBRARY_SUBDIR}")

    if(APPLE)
        set(rpath "@executable_path/${relative_lib_dir}")
    else()
        set(rpath "\$ORIGIN/${relative_lib_dir}")
    endif()

    set_target_properties(mbox_executable PROPERTIES
        INSTALL_RPATH "${CMAKE_INSTALL_RPATH};${rpath}"
        )
endif()

set_target_properties(mbox_executable PROPERTIES
    OUTPUT_NAME ${MBOX_APPLICATION_NAME}
    )

################################################################################
# Compile definitions
################################################################################

file(RELATIVE_PATH relative_python_dir "/${MBOX_RUNTIME_SUBDIR}" "/${PYNCPP_PYTHON_SUBDIR}")

target_compile_definitions(mbox_executable PUBLIC
    PYTHON_HOME="${relative_python_dir}"
    )

################################################################################
# Link
################################################################################

target_link_libraries(mbox_executable PUBLIC
    mbox_cpp_api
    )

################################################################################
# Install/Export
################################################################################

install(TARGETS mbox_executable
    RUNTIME
    DESTINATION "${MBOX_RUNTIME_SUBDIR}"
    )
