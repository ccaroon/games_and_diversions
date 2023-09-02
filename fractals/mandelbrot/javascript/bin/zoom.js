#!/usr/bin/env node
var Mandelbrot  = require('../lib/mandelbrot');
var AsciiCanvas = require('../../shared/lib/ascii_canvas');
//##############################################################################
var m = new Mandelbrot(-1, 1, -1, 1),
    p = new AsciiCanvas(160,60);

m.compute(100, p);
p.display();
