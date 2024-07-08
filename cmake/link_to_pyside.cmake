# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

execute_process(
    COMMAND ${CMAKE_COMMAND} -E env otool -L "${TARGET_PATH}"
    OUTPUT_VARIABLE output
    )

string(REPLACE "\n" ";" output ${output})

foreach(line ${output})
    if(line MATCHES "^(.*/(Qt.*\\.framework/Versions/.*/Qt[^/(]*)) .*$")
        string(STRIP ${CMAKE_MATCH_1} path)
        execute_process(
            COMMAND ${CMAKE_INSTALL_NAME_TOOL}
            -change "${path}" "@rpath/${CMAKE_MATCH_2}"
            "${TARGET_PATH}"
            )
    endif()
endforeach()
