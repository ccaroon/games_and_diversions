# Mandelbrot in Python with PyGame

## Notes
Suppose the center is the (cx, cy) and the length you want to display is (lx, ly), you can use the following scaling formula:

x0 = cx + (i/width - 0.5)*lx;

y0 = cy + (j/width - 0.5)*ly;

What it does is to 
1. Scale down the pixel to the unit interval `(0 <= i/width < 1)`
2. Shift the center `(-0.5 <= i/width-0.5 < 0.5)`
3. Scale up to your desired dimension `(-0.5*lx <= (i/width-0.5)*lx < 0.5*lx)`
4. Shift it to the center you've given
