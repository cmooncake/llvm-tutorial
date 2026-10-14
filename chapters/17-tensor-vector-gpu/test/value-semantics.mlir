module {
  func.func @main() -> i32 {
    %c0 = arith.constant 0 : index
    %one = arith.constant 1 : i32
    %two = arith.constant 2 : i32
    %three = arith.constant 3 : i32
    %empty = tensor.empty() : tensor<4xi32>
    %a = linalg.fill ins(%one : i32) outs(%empty : tensor<4xi32>) -> tensor<4xi32>
    %b = tensor.insert %two into %a[%c0] : tensor<4xi32>
    // Both values remain live: reusing a's buffer without a copy is incorrect.
    %old = tensor.extract %a[%c0] : tensor<4xi32>
    %new = tensor.extract %b[%c0] : tensor<4xi32>
    %sum = arith.addi %old, %new : i32
    %bad = arith.cmpi ne, %sum, %three : i32
    %status = arith.extui %bad : i1 to i32
    return %status : i32
  }
}
