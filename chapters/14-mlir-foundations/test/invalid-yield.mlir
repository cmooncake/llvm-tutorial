module {
  func.func @broken() -> i32 {
    %c0 = arith.constant 0 : index
    %c1 = arith.constant 1 : index
    %zero = arith.constant 0 : i32
    %result = scf.for %i = %c0 to %c1 step %c1 iter_args(%acc = %zero) -> (i32) {
      scf.yield %c0 : index
    }
    return %result : i32
  }
}
