# Variables
CC = clang
CFLAGS = -Wall -pedantic -std=c99 -fPIC
PYTHON_INCLUDE = /usr/include/python3.11
PYTHON_LIB = /usr/lib/python3.11
LD_LIBRARY_PATH = `pwd`

# Targets
all: phylib.o libphylib.so phylib_wrap.c phylib.py phylib_wrap.o _phylib.so

phylib.o: phylib.c
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm

phylib_wrap.c phylib.py: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I$(PYTHON_INCLUDE) -o phylib_wrap.o

_phylib.so: phylib_wrap.o
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L$(PYTHON_LIB) -lpython3.11 -lphylib -o _phylib.so

clean:
	rm -f *.o *.so phylib.py phylib_wrap.c
