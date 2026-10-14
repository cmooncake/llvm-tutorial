#include "runtime.h"
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

void ml_print_i32(int32_t value) { printf("%" PRId32 "\n", value); }
void ml_print_bool(int32_t value) { puts(value ? "true" : "false"); }
void ml_trap(int32_t code) {
  fprintf(stderr, "trap %" PRId32 "\n", code);
  exit(70);
}
