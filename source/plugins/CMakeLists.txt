# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

file(GLOB_RECURSE python_files RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}/*.py"
    )

foreach(file ${python_files})
    configure_file("${CMAKE_CURRENT_SOURCE_DIR}/${file}"
        "${CMAKE_CURRENT_BINARY_DIR}/python/${file}"
        @ONLY
        )
endforeach()

add_custom_target(mbox_python_plugins ALL
    COMMAND ${CMAKE_COMMAND} -E copy_directory "${CMAKE_CURRENT_BINARY_DIR}/python" "${MBOX_PACKAGE_ROOT}/musicbox_plugins"
    VERBATIM
    )
