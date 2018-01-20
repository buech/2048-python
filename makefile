FC = gfortran
F2PYFLAGS = --arch=-march=native --opt=-Ofast
MODNAME = utils_fortran

$(MODNAME).so: $(MODNAME).f90
	f2py -c $(F2PYFLAGS) -m $(MODNAME) $<

utils.so: utils_c.c
	$(CC) -march=native -Ofast -fPIC -shared -o $@ $<

test.x: $(MODNAME).f90
	$(FC) -o $@ $<

clean:
	rm -f $(MODNAME).so $(MODNAME).mod test.x utils.so

.PHONY: clean
