CXXFLAGS += -std=c++11 -march=native -O3 -fPIC
FC = gfortran
F2PY = f2py2.7
F2PYFLAGS = --arch=-march=native --opt=-Ofast
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

.PHONY: clean
