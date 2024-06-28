# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

################################################################################
# Install packages
################################################################################

set(packages
    ${MBOX_PYSIDE_PACKAGE}
    )

add_custom_target(mbox_python_packages ALL
    COMMAND pyncpp_executable -m pip install ${packages}
    VERBATIM
    )

################################################################################
# Config files
################################################################################

foreach(config ${CMAKE_CONFIGURATION_TYPES} ${CMAKE_BUILD_TYPE})

    set(prefix_dir "${MBOX_ROOT_BASE}/${config}")
    set(share_dir "${prefix_dir}/${MBOX_SHARE_SUBDIR}")

    configure_package_config_file("${CMAKE_CURRENT_SOURCE_DIR}/QtConfig.cmake.in" "${share_dir}/${MBOX_QT_PACKAGE}Config.cmake"
        INSTALL_PREFIX "${prefix_dir}"
        INSTALL_DESTINATION "${MBOX_ROOT}/${MBOX_SHARE_SUBDIR}"
        )

    write_basic_package_version_file("${share_dir}//${MBOX_QT_PACKAGE}ConfigVersion.cmake"
        VERSION ${${MBOX_QT_PACKAGE}_VERSION_MAJOR}.${${MBOX_QT_PACKAGE}_VERSION_MINOR}
        COMPATIBILITY SameMinorVersion
        )

    install(FILES
        "${share_dir}/${MBOX_QT_PACKAGE}Config.cmake"
        "${share_dir}/${MBOX_QT_PACKAGE}ConfigVersion.cmake"
        CONFIGURATIONS ${config}
        DESTINATION "${MBOX_SHARE_SUBDIR}"
        )

endforeach()
