define i32 @classify(i32 %x) {
entry:
  %is_negative = icmp slt i32 %x, 0
  br i1 %is_negative, label %negative, label %nonnegative

negative:
  br label %exit

nonnegative:
  %is_positive = icmp sgt i32 %x, 0
  %positive_value = zext i1 %is_positive to i32
  br label %exit

exit:
  %result = phi i32 [ -1, %negative ], [ %positive_value, %nonnegative ]
  ret i32 %result
}

