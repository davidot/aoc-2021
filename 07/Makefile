CXXFLAGS=-Wall -Wextra -std=c++20 -pedantic -O2
INPUTS=sample.txt input.txt

.PHONY: test
test: main sample.txt
	./main sample.txt

.PHONY: run
run: main input.txt
	./main input.txt

main: main.cpp
	$(CXX) $(CXXFLAGS) -o main main.cpp
