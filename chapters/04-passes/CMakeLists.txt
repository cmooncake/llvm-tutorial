cmake_minimum_required(VERSION 3.20)
project(Chapter04Passes LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT LLVM_FOUND)
  find_package(LLVM REQUIRED CONFIG)
endif()
include(${CMAKE_CURRENT_LIST_DIR}/../../cmake/LLVMVersion.cmake)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(AddLLVM)

include_directories(SYSTEM ${LLVM_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

add_llvm_pass_plugin(TutorialPasses src/TutorialPasses.cpp)

