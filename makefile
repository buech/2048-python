FC = gfortran
F2PYFLAGS = --arch=-march=native --opt=-Ofast
MODNAME = utils_fortran

$(MODNAME).so: $(MODNAME).f90
	f2py -c $(F2PYFLAGS) -m $(MODNAME) $<

test.x: $(MODNAME).f90
	$(FC) -o $@ $<

.PHONY: clean

clean:
	rm -rf *.so *.so.* *.mod *.x
