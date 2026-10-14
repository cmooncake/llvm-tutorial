if(NOT LLVM_PACKAGE_VERSION MATCHES "^22\\.1\\.")
  message(FATAL_ERROR "Course baseline is LLVM 22.1.x; found ${LLVM_PACKAGE_VERSION}. Set LLVM_DIR to the matching SDK.")
endif()
message(STATUS "Course LLVM SDK: ${LLVM_PACKAGE_VERSION} (${LLVM_DIR})")
