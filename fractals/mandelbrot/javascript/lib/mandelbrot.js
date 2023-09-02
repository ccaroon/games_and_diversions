//##############################################################################
function Mandelbrot(xMin, xMax, yMin, yMax) {
  this.xMin = xMin;
  this.xMax = xMax;
  this.yMin = yMin;
  this.yMax = yMax;
}
//##############################################################################
Mandelbrot.prototype.compute = function (iterations, canvas) {
  var x,y;
  var xStep, yStep;
  var z,zi,newZ,newZI;
  var colour;
  var i,j,k;
  var inSet;

  /* these are used for calculating the points corresponding to the pixels */
  xStep = (this.xMax - this.xMin) / canvas.width;
  yStep = (this.yMax - this.yMin) / canvas.height;

  x = this.xMin;
  y = this.yMin;
  for (i = 0; i < canvas.height; i++)
  {
    for (j = 0; j < canvas.width; j++)
    {
      z = 0;
      zi = 0;
      inSet = true;
      for (k = 0; k < iterations; k++)
      {
        /* z^2 = (a+bi)(a+bi) = a^2 + 2abi - b^2 */
        newZ = (z*z) - (zi*zi) + x;
        newZI = 2*z*zi + y;
        z = newZ;
        zi = newZI;
        if( ((z*z) + (zi*zi)) > 4 )
        {
          inSet = false;
          colour = k;
          k = iterations;
        }
      }

      if (inSet)
      {
        canvas.set(i, j, 0);
      }
      else
      {
        canvas.set(i, j, colour);
      }

      x += xStep;
    }

    y += yStep;
    x = this.xMin;
  }
}
//##############################################################################
module.exports = Mandelbrot;
