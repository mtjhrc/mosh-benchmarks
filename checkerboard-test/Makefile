CXXFLAGS = -Wall -Wextra -std=c++17

build: build/checkerboard build/input.termrec  

build/checkerboard: checkerboard.cpp
	$(CXX) $(CFLAGS) $(shell pkg-config --cflags --libs ncurses) -o build/checkerboard checkerboard.cpp

build/input.termrec: gen_input.py
	python3 gen_input.py
 
clean:
	rm build/*

.PHONY: clean
