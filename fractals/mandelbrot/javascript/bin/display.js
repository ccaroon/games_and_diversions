#!/usr/bin/env node
var Mandelbrot  = require('../lib/mandelbrot');
var AsciiCanvas = require('../../shared/lib/ascii_canvas');
//##############################################################################
var m = new Mandelbrot(-2,1,-1,1),
    c = new AsciiCanvas(195,65);

m.compute(150, c);
c.display();
