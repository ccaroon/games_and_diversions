// TODO: how to set initial state?

var Cell = require('../lib/cell');
var Grid = require('../lib/grid');
//##############################################################################
function Board (canvas) {
  this.canvas = canvas;
  this.grid   = new Grid(canvas.width, canvas.height);
}
//##############################################################################
Board.prototype.tick = function () {
  var that = this;

  // TODO: iterate over board and set on/off on canvas
  grid.iterate(function (r,c) {
    var cell = this.get(r,c);

// Any live cell with fewer than two live neighbours dies, as if caused by under-population
// Any live cell with two or three live neighbours lives on to the next generation.
// Any live cell with more than three live neighbours dies, as if by overcrowding.
// Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

    
  });

  this.display();
};
//##############################################################################
Board.prototype.display = function () {
  this.canvas.clear();

  // TODO: drawn new state on canvas

  // display canvas
  this.canvas.display();
};
// ##############################################################################
module.exports = Board;
