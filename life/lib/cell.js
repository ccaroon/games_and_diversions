//##############################################################################
function Cell (alive) {
  this.is_alive = alive;
}
// ##############################################################################
Cell.prototype.die = function () {
  this.is_alive = false;
};
//##############################################################################
Cell.prototype.is_alive = function () {
  return (this.is_alive);
};
// ##############################################################################
Cell.prototype.is_dead = function () {
  return (!this.is_alive);
};
//##############################################################################
module.exports = Cell;
