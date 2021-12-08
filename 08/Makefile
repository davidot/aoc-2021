CXXFLAGS=-Wall -Wextra -std=c++20 -pedantic -O2

.PHONY: test
test: main sample1.txt
	./main sample1.txt

.PHONY: test2
test2: main sample2.txt
	./main sample2.txt

.PHONY: run
run: main input.txt
	./main input.txt

main: main.cpp
	$(CXX) $(CXXFLAGS) -o main main.cpp
