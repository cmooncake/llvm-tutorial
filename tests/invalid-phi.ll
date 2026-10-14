; The merge block has two predecessors, but its phi lists only one.
define i32 @broken(i1 %condition) {
entry:
  br i1 %condition, label %left, label %right
left:
  br label %merge
right:
  br label %merge
merge:
  %value = phi i32 [ 1, %left ]
  ret i32 %value
}
