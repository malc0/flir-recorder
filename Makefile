CC = gcc
CFLAGS = -std=gnu99 -O3 -march=native -Wall -g

PYTHON_INC = -I/usr/include/python3.4m -I/usr/lib64/python3.4/site-packages/numpy/core/include

all: cmx.so

cmx.c: cmx.pyx
	cython cmx.pyx

cmx.so: cmx.c
	$(CC) $(CFLAGS) -shared -fPIC -o cmx.so cmx.c $(PYTHON_INC)

clean:
	rm -f *.so cmx.c
