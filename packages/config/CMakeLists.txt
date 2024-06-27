# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

install(FILES
    "${CMAKE_CURRENT_SOURCE_DIR}/pyncppConfig_qt.cmake"
    DESTINATION "${pyncpp_SHARE_SUBDIR}"
    )

foreach(qt_version ${qt_versions})

    if(qt_version EQUAL 5)
        set(pyside_version 2)
    else()
        set(pyside_version 6)
    endif()

    pyncpp_wrap_package_config(Qt${qt_version} ${qt_version} PySide${pyside_version} "Qt")

    install(FILES
        "${CMAKE_CURRENT_BINARY_DIR}/Qt${qt_version}Config.cmake"
        DESTINATION "${pyncpp_SHARE_SUBDIR}"
        )

    set(Qt${qt_version}_DIR "${CMAKE_CURRENT_BINARY_DIR}" PARENT_SCOPE)

endforeach()
