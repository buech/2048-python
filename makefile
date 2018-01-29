CXXFLAGS += -std=c++11 -march=native -O3 -fPIC

all: utils.so

utils.so: utils.cpp utils.h
	$(CXX) $(CXXFLAGS) -shared -o $@ $<

clean:
	rm -f utils.so

.PHONY: all clean
