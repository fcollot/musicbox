// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#ifdef WIN32
    #ifdef mbox_cpp_api_EXPORTS
        #define MBOX_EXPORT __declspec(dllexport)
    #else
        #define MBOX_EXPORT __declspec(dllimport)
    #endif
#else
    #define MBOX_EXPORT
#endif
