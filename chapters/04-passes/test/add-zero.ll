; RUN: opt -load-pass-plugin %llvmshlibdir/TutorialPasses%shlibext \
; RUN:   -passes=remove-add-zero -S %s | FileCheck %s

define i32 @right_zero(i32 %x) {
; CHECK-LABEL: define i32 @right_zero
; CHECK-NEXT: ret i32 %x
  %sum = add i32 %x, 0
  ret i32 %sum
}

define i32 @left_zero(i32 %x) {
; CHECK-LABEL: define i32 @left_zero
; CHECK-NEXT: ret i32 %x
  %sum = add i32 0, %x
  ret i32 %sum
}

define i32 @nonzero(i32 %x) {
; CHECK-LABEL: define i32 @nonzero
; CHECK: %sum = add i32 %x, 1
  %sum = add i32 %x, 1
  ret i32 %sum
}

define float @float_zero(float %x) {
; CHECK-LABEL: define float @float_zero
; CHECK: %sum = fadd float %x, 0.000000e+00
  %sum = fadd float %x, 0.000000e+00
  ret float %sum
}

