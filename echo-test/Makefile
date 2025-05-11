CFLAGS = -Wall -Wextra -std=c99

build: build/echo-test build/input.termrec  

build/echo-test: echo-test.c
	$(CC) $(CFLAGS) -o build/echo-test echo-test.c

build/input.termrec: gen_input.py
	python3 gen_input.py
 
clean:
	rm build/*

.PHONY: all clean results results/good-net results/ 
