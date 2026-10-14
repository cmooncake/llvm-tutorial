#include <fstream>
#include <iostream>
#include <string>

// Integration shell only. Students implement front-end and back-end modules.
int main(int argc, char **argv) {
  if (argc < 3) {
    std::cerr << "usage: minilang check|run file.ml\n"
                 "       minilang emit-ir file.ml -o file.ll\n";
    return 2;
  }
  const std::string command = argv[1];
  const bool emit = command == "emit-ir";
  if ((command != "check" && command != "run" && !emit) ||
      (!emit && argc != 3) ||
      (emit && (argc != 5 || std::string(argv[3]) != "-o"))) {
    std::cerr << "invalid command or arguments\n";
    return 2;
  }
  std::ifstream source(argv[2], std::ios::binary);
  if (!source) {
    std::cerr << "cannot open source: " << argv[2] << '\n';
    return 2;
  }
  // A missing implementation must never masquerade as successful compilation.
  std::cerr << "student implementation required: " << command << '\n';
  return 78;
}
