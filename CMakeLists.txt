set(MEMORYCHECK_COMMAND_OPTIONS "--gen-suppressions=all --error-exitcode=-1 --leak-check=full --trace-children=yes --track-origins=yes" CACHE STRING "" FORCE)
if(EXISTS "${CMAKE_CURRENT_LIST_DIR}/sup")
    set(MEMORYCHECK_SUPPRESSIONS_FILE "${CMAKE_CURRENT_LIST_DIR}/sup" CACHE STRING "" FORCE)
endif()
include (CTest)
add_executable(main main.cpp)
add_test (main ./main)
add_test (main2 ./main)
add_test (main3 ./main)
set_tests_properties(main3 PROPERTIES LABELS skip)
add_test (main4 ./main)
add_test (main5 ./main)
add_test (nofail true)

#add_custom_target(cat Testing/Temporary/MemoryChecker.1.log | sed -e  "s/==[0-9]*==.*$//g" | grep -v "^$"^C

