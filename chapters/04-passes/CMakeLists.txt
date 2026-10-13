cmake_minimum_required(VERSION 3.20)
project(Chapter04Passes LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(LLVM 21.1 REQUIRED CONFIG)

if(LLVM_PACKAGE_VERSION VERSION_GREATER_EQUAL 23)
  message(FATAL_ERROR "This chapter supports LLVM 21.1.x and 22.1.x, found ${LLVM_PACKAGE_VERSION}")
endif()

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(AddLLVM)
include(HandleLLVMOptions)

add_llvm_pass_plugin(TutorialPasses src/TutorialPasses.cpp)

