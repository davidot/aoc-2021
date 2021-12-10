CXXFLAGS=-Wall -Wextra -std=c++20 -pedantic -O2

.PHONY: test
test: main sample.txt
	./main sample.txt

.PHONY: run
run: main input.txt
	./main input.txt

main: main.cpp
	$(CXX) $(CXXFLAGS) -o main main.cpp
