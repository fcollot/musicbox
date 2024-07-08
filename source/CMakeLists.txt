# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

macro(set_qt_paths target_or_path)

    if(TARGET ${target_or_path})
        add_custom_command(TARGET ${target_or_path} POST_BUILD
            COMMAND ${CMAKE_COMMAND}
            -D "TARGET_PATH=$<TARGET_FILE:${target_or_path}>"
            -D "CMAKE_INSTALL_NAME_TOOL=${CMAKE_INSTALL_NAME_TOOL}"
            -P "${PROJECT_SOURCE_DIR}/cmake/link_to_pyside.cmake"
            VERBATIM
            )
    else()
        execute_process(
            COMMAND ${CMAKE_COMMAND}
            -D "TARGET_PATH=${target_or_path}"
            -D "CMAKE_INSTALL_NAME_TOOL=${CMAKE_INSTALL_NAME_TOOL}"
            -P "${PROJECT_SOURCE_DIR}/cmake/link_to_pyside.cmake"
            )
    endif()
endmacro()

set(qt_components
    Core
    Widgets
    )

find_package(${MBOX_QT_PACKAGE} REQUIRED COMPONENTS ${qt_components})

################################################################################
# Subdirectories
################################################################################

add_subdirectory(core)
add_subdirectory(plugins)

if(MBOX_STANDALONE)
    add_subdirectory(standalone)
endif()

add_custom_target(mbox_pip_install ALL
    COMMAND pyncpp_executable -m pip install
    "${MBOX_PACKAGE_ROOT}/musicbox"
    "${MBOX_PACKAGE_ROOT}/musicbox_plugins"
    VERBATIM
    )

add_dependencies(mbox_pip_install mbox_python_package mbox_python_plugins)

################################################################################
# Config module
################################################################################

#foreach(config ${CMAKE_CONFIGURATION_TYPES} ${CMAKE_BUILD_TYPE})

#    set(share_dir ${PYNCPP_ROOT_BASE}/${config}/${PYNCPP_SHARE_SUBDIR})

#    file(COPY_FILE
#        "${CMAKE_CURRENT_SOURCE_DIR}/pyncppConfig_pyncpp.cmake"
#        "${share_dir}/pyncppConfig_pyncpp.cmake"
#        )

#    install(FILES
#        "${share_dir}/pyncppConfig_pyncpp.cmake"
#        CONFIGURATIONS ${config}
#        DESTINATION "${PYNCPP_SHARE_SUBDIR}"
#        )

#endforeach()
