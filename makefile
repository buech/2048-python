CC = gcc-7
CFLAGS = -march=native -Ofast -fPIC
FC = gfortran
F2PYFLAGS = --arch=-march=native --opt=-Ofast
MODNAME = utils_fortran

all: fort c

fort: $(MODNAME).so
c: utils.so

$(MODNAME).so: $(MODNAME).f90
	f2py -c $(F2PYFLAGS) -m $(MODNAME) $<

utils.so: utils_c.c
	$(CC) $(CFLAGS) -shared -o $@ $<

test.x: $(MODNAME).f90
	$(FC) -o $@ $<

clean:
	rm -f $(MODNAME).so $(MODNAME).mod test.x utils.so

.PHONY: clean
