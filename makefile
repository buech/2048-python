utils_fortran.so: utils_fortran.f90
	f2py -c --arch=-march=native --opt=-Ofast -m utils_fortran utils_fortran.f90

.PHONY: clean

clean:
	rm -rf *.so *.so.* *.mod
