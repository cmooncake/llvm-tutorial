module {
  func.func @main() -> i32 {
    %lo = arith.constant 0 : index
    %hi = arith.constant 10 : index
    %step = arith.constant 1 : index
    %zero = arith.constant 0 : i32
    %sum = scf.for %i = %lo to %hi step %step iter_args(%acc = %zero) -> (i32) {
      %value = arith.index_cast %i : index to i32
      %next = arith.addi %acc, %value : i32
      scf.yield %next : i32
    }
    %expected = arith.constant 45 : i32
    %bad = arith.cmpi ne, %sum, %expected : i32
    %status = arith.extui %bad : i1 to i32
    return %status : i32
  }
}
