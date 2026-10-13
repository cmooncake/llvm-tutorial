#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Verifier.h"
#include "llvm/Support/raw_ostream.h"

#include <memory>

int main() {
  llvm::LLVMContext context;
  auto module = std::make_unique<llvm::Module>("chapter03", context);
  llvm::IRBuilder<> builder(context);

  llvm::Type *i32 = builder.getInt32Ty();
  llvm::FunctionType *functionType =
      llvm::FunctionType::get(i32, {i32, i32}, false);
  llvm::Function *function = llvm::Function::Create(
      functionType, llvm::Function::ExternalLinkage, "mul_add", *module);

  auto argument = function->arg_begin();
  llvm::Value *lhs = &*argument++;
  lhs->setName("lhs");
  llvm::Value *rhs = &*argument;
  rhs->setName("rhs");

  llvm::BasicBlock *entry =
      llvm::BasicBlock::Create(context, "entry", function);
  builder.SetInsertPoint(entry);

  llvm::Value *product = builder.CreateMul(lhs, rhs, "product");
  llvm::Value *result = builder.CreateAdd(
      product, llvm::ConstantInt::get(i32, 7), "result");
  builder.CreateRet(result);

  if (llvm::verifyFunction(*function, &llvm::errs()) ||
      llvm::verifyModule(*module, &llvm::errs())) {
    llvm::errs() << "generated invalid LLVM IR\n";
    return 1;
  }

  module->print(llvm::outs(), nullptr);
  return 0;
}

