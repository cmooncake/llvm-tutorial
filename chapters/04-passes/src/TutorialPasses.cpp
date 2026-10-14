#include "llvm/ADT/StringRef.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instruction.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Plugins/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

namespace {

class PrintInstructionCountPass
    : public llvm::PassInfoMixin<PrintInstructionCountPass> {
public:
  llvm::PreservedAnalyses run(llvm::Function &function,
                              llvm::FunctionAnalysisManager &) {
    unsigned count = 0;
    for (const llvm::BasicBlock &block : function)
      count += block.size();

    llvm::errs() << function.getName() << ": " << count << " instructions\n";
    return llvm::PreservedAnalyses::all();
  }
};

class RemoveAddZeroPass : public llvm::PassInfoMixin<RemoveAddZeroPass> {
public:
  llvm::PreservedAnalyses run(llvm::Function &function,
                              llvm::FunctionAnalysisManager &) {
    bool changed = false;

    for (llvm::BasicBlock &block : function) {
      for (auto iterator = block.begin(); iterator != block.end();) {
        llvm::Instruction &instruction = *iterator++;
        auto *binary = llvm::dyn_cast<llvm::BinaryOperator>(&instruction);
        if (!binary || binary->getOpcode() != llvm::Instruction::Add)
          continue;

        llvm::Value *replacement = nullptr;
        if (auto *rhs = llvm::dyn_cast<llvm::ConstantInt>(binary->getOperand(1));
            rhs && rhs->isZero()) {
          replacement = binary->getOperand(0);
        } else if (auto *lhs =
                       llvm::dyn_cast<llvm::ConstantInt>(binary->getOperand(0));
                   lhs && lhs->isZero()) {
          replacement = binary->getOperand(1);
        }

        if (!replacement)
          continue;

        binary->replaceAllUsesWith(replacement);
        binary->eraseFromParent();
        changed = true;
      }
    }

    return changed ? llvm::PreservedAnalyses::none()
                   : llvm::PreservedAnalyses::all();
  }
};

} // namespace

llvm::PassPluginLibraryInfo getTutorialPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "TutorialPasses", LLVM_VERSION_STRING,
          [](llvm::PassBuilder &passBuilder) {
            passBuilder.registerPipelineParsingCallback(
                [](llvm::StringRef name, llvm::FunctionPassManager &manager,
                   llvm::ArrayRef<llvm::PassBuilder::PipelineElement>) {
                  if (name == "print-inst-count") {
                    manager.addPass(PrintInstructionCountPass());
                    return true;
                  }
                  if (name == "remove-add-zero") {
                    manager.addPass(RemoveAddZeroPass());
                    return true;
                  }
                  return false;
                });
          }};
}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return getTutorialPassPluginInfo();
}

