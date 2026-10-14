; Executed by the root CTest suite using the actual CMake plugin target path.

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

define i32 @chain(i32 %x) {
; CHECK-LABEL: define i32 @chain
; CHECK-NEXT: ret i32 %x
  %a = add i32 %x, 0
  %b = add i32 0, %a
  ret i32 %b
}

define <2 x i32> @vector_zero(<2 x i32> %x) {
; CHECK-LABEL: define <2 x i32> @vector_zero
; CHECK: %sum = add <2 x i32> %x, zeroinitializer
  %sum = add <2 x i32> %x, zeroinitializer
  ret <2 x i32> %sum
}

