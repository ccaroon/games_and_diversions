#include <stdio.h>
#include "mandelbrot.h"

int main(int argc, char **argv) {
    Mandelbrot *m = new Mandelbrot(-2,1,-1,1);

    m->compute(500);
    m->display2();

    return (0);
}
