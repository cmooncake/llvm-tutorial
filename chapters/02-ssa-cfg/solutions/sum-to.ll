define i32 @sum_to(i32 %n) {
entry:
  %has_work = icmp sgt i32 %n, 0
  br i1 %has_work, label %loop, label %exit

loop:
  %i = phi i32 [ 0, %entry ], [ %next_i, %loop ]
  %sum = phi i32 [ 0, %entry ], [ %next_sum, %loop ]
  %next_sum = add i32 %sum, %i
  %next_i = add i32 %i, 1
  %continue = icmp slt i32 %next_i, %n
  br i1 %continue, label %loop, label %exit

exit:
  %result = phi i32 [ 0, %entry ], [ %next_sum, %loop ]
  ret i32 %result
}

