.PHONY: test
test: main.native main.byte ../sample.txt
	./main.native ../sample.txt

.PHONY: run
run: main.native main.byte ../input.txt
	./main.native ../input.txt

main.native: main.ml
	ocamlopt -o main.native main.ml

main.byte: main.ml
	ocamlc -o main.byte main.ml
