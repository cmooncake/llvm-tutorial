cmake_minimum_required(VERSION 3.20)
project(Chapter03CppApi LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT LLVM_FOUND)
  find_package(LLVM REQUIRED CONFIG)
endif()
include(${CMAKE_CURRENT_LIST_DIR}/../../cmake/LLVMVersion.cmake)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake from ${LLVM_DIR}")

separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND "${LLVM_DEFINITIONS}")

add_executable(ir-generator src/ir_generator.cpp)
target_include_directories(ir-generator SYSTEM PRIVATE ${LLVM_INCLUDE_DIRS})
target_compile_options(ir-generator PRIVATE ${LLVM_DEFINITIONS_LIST})

if(LLVM_LINK_LLVM_DYLIB)
  target_link_libraries(ir-generator PRIVATE LLVM)
else()
  llvm_map_components_to_libnames(LLVM_LIBS core support)
  target_link_libraries(ir-generator PRIVATE ${LLVM_LIBS})
endif()

