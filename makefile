CXXFLAGS = -std=c++11 -march=native -O3 -fPIC
FC = gfortran
F2PYFLAGS = --arch=-march=native --opt=-Ofast
MODNAME = utils_fortran

all: fort c

fort: $(MODNAME).so
c: utils.so

$(MODNAME).so: $(MODNAME).f90
	f2py -c $(F2PYFLAGS) -m $(MODNAME) $<

utils.so: utils.cpp
	$(CXX) $(CXXFLAGS) -shared -o $@ $<

test.x: $(MODNAME).f90
	$(FC) -o $@ $<

clean:
	rm -f $(MODNAME).so *.mod test.x utils.so

.PHONY: clean
