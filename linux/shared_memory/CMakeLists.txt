cmake_minimum_required(VERSION 3.2)

project(shared_memory_tutorial)

################
# Dependencies #
################
find_library(LibRT rt)
find_package(Threads REQUIRED)

###########
# Library #
###########
add_library(shared_memory
    STATIC 
    src/shared_memory_provider.cpp
    src/shared_memory_consumer.cpp
        include/shared_memory/shared_memory_base.h src/shared_memory_base.cpp)

set_target_properties(shared_memory
    PROPERTIES
        CXX_STANDARD 14
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS NO
)

target_include_directories(shared_memory
    PRIVATE
        include
    SYSTEM INTERFACE
        include
)

target_compile_options(shared_memory
    PRIVATE
        -Wall
        -Wextra
)

target_link_libraries(shared_memory
    PRIVATE
        ${LibRT}
        Threads::Threads
)

##############
# Executable #
##############
add_executable(shared_memory_provider src/provider.cpp)

target_link_libraries(shared_memory_provider
    PRIVATE
        shared_memory 
)

add_executable(shared_memory_consumer src/consumer.cpp)

target_link_libraries(shared_memory_consumer
    PRIVATE
        shared_memory
)