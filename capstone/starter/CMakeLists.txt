cmake_minimum_required(VERSION 3.20)
project(MiniLangStudent LANGUAGES CXX)
add_executable(minilang main.cpp)
target_compile_features(minilang PRIVATE cxx_std_20)
