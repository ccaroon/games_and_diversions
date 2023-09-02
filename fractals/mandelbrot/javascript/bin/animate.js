#!/usr/bin/env node
var Mandelbrot = require('../lib/mandelbrot');
var AsciiCanvas = require('../../../../shared/lib/ascii_canvas');
//##############################################################################
var m = new Mandelbrot(-2, 1, -1, 1),
  c = new AsciiCanvas(195, 65),
  i = 1;

var run = function () {
  m.compute(i, c);
  c.display();
  i += 1;
  if (i <= 50) {
    setTimeout(run, 250);
  }
}
run();
