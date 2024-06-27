# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

foreach(qt_version 5 6)
        if(EXISTS "${CMAKE_CURRENT_LIST_DIR}/Qt${qt_version}Config.cmake")
            set(Qt${qt_version}_DIR "${CMAKE_CURRENT_LIST_DIR}")

#            find_dependency(Qt${qt_version}
#                COMPONENTS Core
#                )

            if(NOT NO_PYNCPP_QT_TARGETS)
                include("${CMAKE_CURRENT_LIST_DIR}/pyncpp_qt_cpp_api_${qt_version}_export.cmake")
                set(pyncpp_QT${qt_version}_LIBRARY pyncpp_qt_cpp_api_${qt_version})
            endif()

            set(pyncpp_qt${qt_version}_FOUND TRUE)
        endif()
endforeach()
