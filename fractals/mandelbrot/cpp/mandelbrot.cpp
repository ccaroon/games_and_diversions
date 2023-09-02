#include <stdio.h>
#include "mandelbrot.h"

// -----------------------------------------------------------------------------
Mandelbrot::Mandelbrot(int xMin, int xMax, int yMin, int yMax) {
    this->xMin = xMin;
    this->xMax = xMax;
    this->yMin = yMin;
    this->yMax = yMax;
}
// -----------------------------------------------------------------------------
void Mandelbrot::compute(int iterations) {
    double x,y;
    double xStep, yStep;
    double z,zi,newZ,newZI;
    int colour;
    int i,j,k;
    bool inSet;

    /* these are used for calculating the points corresponding to the pixels */
    xStep = (this->xMax - this->xMin) / (double)this->width;
    yStep = (this->yMax - this->yMin) / (double)this->height;

    x = this->xMin;
    y = this->yMin;
    for (i = 0; i < this->height; i++) {
        for (j = 0; j < this->width; j++) {
          z = 0;
          zi = 0;
          inSet = true;
          for (k = 0; k < iterations; k++) {
            /* z^2 = (a+bi)(a+bi) = a^2 + 2abi - b^2 */
            newZ = (z*z) - (zi*zi) + x;
            newZI = 2*z*zi + y;
            z = newZ;
            zi = newZI;
            if( ((z*z) + (zi*zi)) > 4 ) {
              inSet = false;
              colour = k;
              k = iterations;
            }
          }

          if (inSet) {
            this->buffer[i][j] = 0x00;
          }
          else {
            this->buffer[i][j] = colour;
          }

          x += xStep;
        }

        y += yStep;
        x = this->xMin;
    }
}
// -----------------------------------------------------------------------------
int* Mandelbrot::getRow(int row) {
    return (this->buffer[row]);
}
// -----------------------------------------------------------------------------
void Mandelbrot::display2(void) {
    int x, y, *row;

    for (y = 0; y < this->height; y++) {
        row = this->getRow(y);

        for (x = 0; x < this->width; x++) {
            if (row[x] > 0) {
                printf("+");
            }
            else {
                printf(" ");
            }
        }
        printf("\n");
    }
}
// -----------------------------------------------------------------------------
void Mandelbrot::display(void) {
    int x, y;

    for (y = 0; y < this->height; y++) {
        for (x = 0; x < this->width; x++) {
            if (this->buffer[y][x] > 0) {
                printf("+");
            }
            else {
                printf(" ");
            }
        }
        printf("\n");
    }
}
// -----------------------------------------------------------------------------
