//##############################################################################
function Grid (w, h) {
  this.width  = w;
  this.height = h;

  this.grid = [];

  this._init();
}
//##############################################################################
Grid.prototype._init = function () {
  var r, c;

  for (r = 0; r < this.height; r+=1) {
    this.grid[r] = [];
    for (c = 0; c < this.width; c+=1) {
      this.grid[r][c] = null;
    }
  }

};
//##############################################################################
Grid.prototype.clear = function () {
  this._init();
};
//##############################################################################
Grid.prototype.set = function (r,c,value) {
  this.grid[r][c] = value;
};
//##############################################################################
Grid.prototype.get = function (r,c) {
  return (this.grid[r][c]);
};
//##############################################################################
module.exports = Grid;
