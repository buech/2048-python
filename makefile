CXXFLAGS ?= -march=native -O3
CXXFLAGS += -std=c++11 -Wall -Wextra -pedantic -fPIC
FC = gfortran
F2PY = f2py
F2PYFLAGS = --quiet --arch=-march=native --opt=-Ofast
MODNAME = utils_fortran

all: fort c

fort: $(MODNAME).so
c: utils_cpp.so

$(MODNAME).so: $(MODNAME).f90
	$(F2PY) -c $(F2PYFLAGS) -m $(MODNAME) $<

utils_cpp.so: utils.cpp utils.h
	$(CXX) $(CXXFLAGS) -shared -o $@ $<

test.x: $(MODNAME).f90
	$(FC) -o $@ $<

clean:
	rm -f $(MODNAME).so *.mod test.x utils_cpp.so
	rm -rf $(MODNAME).so.dSYM

.PHONY: clean
