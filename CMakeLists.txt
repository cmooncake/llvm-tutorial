cmake_minimum_required(VERSION 3.20)
project(LLVMTutorial LANGUAGES C CXX)

include(CTest)
option(TUTORIAL_ENABLE_MLIR "Enable graduate MLIR CPU laboratory tests" OFF)
find_package(LLVM REQUIRED CONFIG)
include(cmake/LLVMVersion.cmake)
add_subdirectory(chapters/03-cpp-api)
add_subdirectory(chapters/04-passes)

if(BUILD_TESTING)
  find_package(Python3 3.10 REQUIRED COMPONENTS Interpreter)
  # Tools must come from the SDK used for headers and libraries, never PATH.
  foreach(tool opt lli llvm-link llvm-as llvm-dis llc clang FileCheck)
    find_program(TUTORIAL_${tool} NAMES ${tool}
      PATHS "${LLVM_TOOLS_BINARY_DIR}" NO_DEFAULT_PATH REQUIRED)
  endforeach()
  set(TUTORIAL_IR_SET solutions CACHE STRING "IR inputs: solutions or exercises")
  set_property(CACHE TUTORIAL_IR_SET PROPERTY STRINGS solutions exercises)
  if(NOT TUTORIAL_IR_SET MATCHES "^(solutions|exercises)$")
    message(FATAL_ERROR "TUTORIAL_IR_SET must be solutions or exercises")
  endif()
  foreach(suite environment toolchain classify sum-to generator passes verifier negative-controls)
    add_test(NAME ${suite} COMMAND "${Python3_EXECUTABLE}"
      "${CMAKE_CURRENT_SOURCE_DIR}/tests/run.py" ${suite}
      --llvm-bin "${LLVM_TOOLS_BINARY_DIR}"
      --llvm-version "${LLVM_PACKAGE_VERSION}"
      --generator "$<TARGET_FILE:ir-generator>"
      --plugin "$<TARGET_FILE:TutorialPasses>"
      --ir-set "${TUTORIAL_IR_SET}")
    set_tests_properties(${suite} PROPERTIES TIMEOUT 90)
  endforeach()
  if(TUTORIAL_ENABLE_MLIR)
    foreach(tool mlir-opt mlir-translate)
      find_program(TUTORIAL_${tool} NAMES ${tool}
        PATHS "${LLVM_TOOLS_BINARY_DIR}" NO_DEFAULT_PATH REQUIRED)
    endforeach()
    foreach(suite scf bufferization diagnostic)
      add_test(NAME mlir-${suite} COMMAND "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/tests/mlir.py" ${suite}
        --llvm-bin "${LLVM_TOOLS_BINARY_DIR}" --version "${LLVM_PACKAGE_VERSION}"
        --output "${CMAKE_CURRENT_BINARY_DIR}/mlir-artifacts/${suite}")
      set_tests_properties(mlir-${suite} PROPERTIES TIMEOUT 120 LABELS "graduate;mlir")
    endforeach()
  endif()
endif()
