#ifndef MINILANG_RUNTIME_H
#define MINILANG_RUNTIME_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
void ml_print_i32(int32_t value);
void ml_print_bool(int32_t value);
void ml_trap(int32_t code);
#ifdef __cplusplus
}
#endif
#endif
