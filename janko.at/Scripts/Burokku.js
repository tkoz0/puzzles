/***********************************************************************
 Project:    Puzzle and Game Game Scripts
 Program:    Burokku
 Copyright:  (c) 2003-2013 by Otto Janko. All Rights Reserved.
 Homepage:   http://www.janko.at
 Mail:       homepage@janko.at
 -----------------------------------------------------------------------
 Rules:
 ~~~~~~
 a) Divide the diagram of size NxN along the grid lines in N
    non-overlapping regions containing N cells each.
 b) A region must not contain two cells with the same letter.
 -----------------------------------------------------------------------
 Usage of a cell's data:
 ~~~~~~~~~~~~~~~~~~~~~~~
 value: nil | number
 label: nil | letter
 areas: not used
 clues: not used
 -----------------------------------------------------------------------
 Usage of a line's data
 ~~~~~~~~~~~~~~~~~~~~~
 value = grid | line
*/

// TODO solver for variant 1
// TODO display the area size in the info line

function Burokku()
{
  // call the constructor of the superclass
  this.constructor();

  // populate the real puzzle name
  this.uis.puzzle = ["Burokku"];

  // supported variants
  var variant = {
    one: "1",
    two: "2" };

  // error codes
  var error = {
    none:     0,    // no error
    size:     1,    // the region is of the wrong size
    dplicate: 3};   // duplicate label in a region

  // enable dragging
  this.enable.dragging = true;

  // we have cell values and line markers
  this.enable.cells = true;
  this.enable.lines = !this.config.touchscreen;

  // user interface colors
  this.uic.done = "#dddddd";

  // populate the keyboard processor tables
  this.charToValue = this.charToValue.concat([
    '0', nil, '/', nil, '-', nil, ',', nil ]);

  // populate the lists of possible cell/line values
  // TODO cell values should only work on mouse devices, not touchscreens
  // this.cell.values =
  //   [1, 2, 3, 4, 5, 6, 7, 8, 9, nil];
  this.line.values =
    [this.line.wall, this.line.cross, this.line.grid];

  // configure the number processor
  this.cell.min = 1;
  this.cell.max = 9;

  /*********************************************************************
   * <reset>
   */
  this.reset2 = function()
  {
    // default variant
    if (!this.level.variant)
      this.level.variant = variant.one;

    // process the problem param
    if (this.level.problem)
    {
      var k = 0;
      var p = this.level.problem.trim().replace(/\s+/g, " ").split(" ");
      for (var y = 0; y < this.size.y; y++)
        for (var x = 0; x < this.size.x; x++)
        {
          var cell = this.board.c[x][y];
          var v = p[k++];
          if (v == "." || v == "-")
            cell.label = nil;
          else if (v >= "a" && v <= "z")
            cell.label = cross;
          else if (v >= "A" && v <= "A")
            cell.label = cross;
          else if (v >= "1" && v <= "9")
            cell.label = cross;
        }
    }

    // process the solution param
    if (this.level.solution)
    {
      var k = 0;
      var p = this.level.solution.trim().replace(/\s+/g, " ").split(" ");
      for (var y = 0; y < this.size.y; y++)
        for (var x = 0; x < this.size.x; x++)
        {
          var cell = this.board.c[x][y];
          var v = p[k++];
          if (v == "." || v == "-" || v == "0")
            cell.work = nil;
          else
            cell.work = parseInt(v);
        }

      // normalize of the solution specification in order to make
      // it comparable to another solution
      var n = 1;
      for (var x = 0; x < this.size.x; x++)
        for (var y = 0; y < this.size.y; y++)
          if (this.board.c[x][y].work != nil)
          {
            var w = this.board.c[x][y].work;
            for (var x1 = 0; x1 < this.size.x; x1++)
              for (var y1 = 0; y1 < this.size.y; y1++)
                if (this.board.c[x1][y1].work == w)
                {
                  this.board.c[x1][y1].solution = n;
                  this.board.c[x1][y1].work = nil;
                }
            n++;
          }

      // calculate the solution status of the vertical lines
      // out of the solution specification
      for (var x = 1; x < this.size.x; x++)
        for (var y = 0; y < this.size.y; y++)
          if (this.board.c[x][y].solution !=
                this.board.c[x-1][y].solution ||
              this.board.c[x][y].solution == nil &&
              this.board.c[x-1][y].solution == nil)
            this.board.v[x][y].solution = this.line.wall;
          else
            this.board.v[x][y].solution = this.line.grid;

      // calculate the solution status of the horizontal lines
      // out of the solution specification
      for (var y = 1; y < this.size.y; y++)
        for (var x = 0; x < this.size.x; x++)
          if (this.board.c[x][y].solution !=
                this.board.c[x][y-1].solution ||
              this.board.c[x][y].solution == nil &&
              this.board.c[x][y-1].solution == nil)
            this.board.h[x][y].solution = this.line.wall;
          else
            this.board.h[x][y].solution = this.line.grid;
    }

    // initialize the fixed lines
    for (var x = 0; x < this.size.x-1; x++)
      for (var y = 0; y < this.size.y; y++)
      {
        if (this.board.c[x][y].label == this.board.c[x+1][y].label &&
            this.board.c[x][y].label != nil)
        {
          this.board.v[x+1][y].value = this.line.wall;
          this.board.v[x+1][y].fixed = true;
        }
        else if (variant == variantTwo &&
          this.board.c[x][y].label + this.board.c[x+1][y].label + 2 == this.size.x)
        {
          this.board.v[x+1][y].value = this.line.none;
          this.board.v[x+1][y].fixed = true;
        }
      }
    for (var x = 0; x < this.size.x; x++)
      for (var y = 0; y < this.size.y-1; y++)
        if (this.board.c[x][y].label == this.board.c[x][y+1].label &&
            this.board.c[x][y].label != nil)
        {
          this.board.h[x][y+1].value = this.line.wall;
          this.board.h[x][y+1].fixed = true;
        }
        else if (variant == variantTwo &&
          this.board.c[x][y].label + this.board.c[x][y+1].label + 2 ==
            this.size.y)
        {
          this.board.h[x][y+1].value = this.line.none;
          this.board.h[x][y+1].fixed = true;
        }

    // the lines which are identical with the border of the diagram
    // are invalid
    for (var x = 0; x < this.size.x; x++)
    {
      this.board.h[x][0].valid = false;
      this.board.h[x][this.size.y].valid = false;
    }
    for (var y = 0; y < this.size.y; y++)
    {
      this.board.v[0][y].valid = false;
      this.board.v[this.size.x][y].valid = false;
    }
  }

  /*********************************************************************
   * <check>
   */
  this.check2 = function()
  {
    // TODO check
    this.solved = false;
  }

  /*********************************************************************
   * <onValues>
   * per default this displays the keypad in which the user can select
   * a value.
   * in our case this toggles between line and cell operation mode
   */
  this.onValues = function()
  {
    // do the default stuff
    if (!this.config.touchscreen)
      Object.getPrototypeOf(this).onValues.call(this);

    // toggle between line and cell mode
    else if (this.enable.lines)
    {
      this.enable.lines = false;
      this.enable.cells = true;
    }
    else
    {
      this.enable.lines = true;
      this.enable.cells = false;
    }
  }

  /*********************************************************************
   * <paintCell>
   */
  this.paintCell = function(cell)
  {
    // get the canvas context
    var g = this.canvas.getContext('2d');

    // paint the background
    if (cell.value == nil)
      g.fillStyle = this.uic.light[0]
    else
      g.fillStyle = this.uic.light[cell.value];
    g.fillRect(cell.px, cell.py, this.unit.x, this.unit.y);

    // shade the background in if the cell is colored by the user and
    // part of a finished area
    if (!cell.error && cell.color != 0)
    {
      var d = 5;
      g.save();
      g.beginPath();
      g.rect(cell.px + 0.5, cell.py + 0.5, this.unit.x, this.unit.y);
      g.clip();
      g.beginPath();
      g.strokeStyle = this.uic.light[cell.color];
      for (var k=d; k < this.unit.x*2; k = k+d)
      {
        g.moveTo(cell.py + k, cell.py);
        g.lineTo(cell.px, cell.py + k);
      }
      g.stroke();
      g.restore();
    }

    // paint the symbol Markers
    this.paintSymbolMarkers(cell);

    /* TODO paint the label in the upper left corner of the cell
    if (c.label != nil)
    {
      g.setColor(textColor);
      g.setFont(clueFont);
      FontMetrics fm = g.getFontMetrics();
      var xx = baseX + cellSize*c.x + 3;
      var yy = baseY + cellSize*c.y + fm.getAscent();
      g.drawString(String.valueOf((char)(c.label+'A')), xx, yy);
    }
    */

    // paint the caption
    if (cell.value != nil)
    {
      this.paintCaption(cell, cell.value.toString(),
        (cell.fixed) ? this.uic.clue : this.uic.text);
    }

    // paint the error markers
    if (cell.error != 0 && this.displayErrors)
    {
      if (cell.value != nil)
        this.paintErrorCircle(cell);
      else
        this.paintErrorDot(cell);
    }
  }

  /*********************************************************************
   * <paintLine>
   * paints a line. in this case we calculate the line style dynamically
   */
  this.paintLine = function(line)
  {
    // save the original value of the line
    var v = line.value;
    var x = line.x;
    var y = line.y;

    // do not touch fixed lines
    if (line.fixed)
      ;

    // vertical line
    else if (line.type == this.item.vline)
    {
      // there are always lines around "1"-cells
      if (this.board.c[x-1][y].value == 1 ||
               this.board.c[x][y].value == 1)
        line.value = this.line.wall;

      // the two adjacent cells have the same value
      else if (this.board.c[x-1][y].value == this.board.c[x][y].value)
        // there is never a line between two no-empty cells with
        // the same value
        if (this.board.c[x][y].value != nil)
          line.value = this.line.none;
        // the value of the line between two empty cells is user-defined
        else
          ;

      // the two adjacent cells have different values
      else if (this.board.c[x-1][y].value != nil &&
               this.board.c[x][y].value != nil)
        // there is always a line between two no-empty cells with
        // a different value
        line.value = this.line.wall;

      // there is always a wall between a completed area and an
      // empty cell
      else if (this.board.c[x-1][y].value != nil &&
              !this.board.c[x-1][y].error ||
               this.board.c[x][y].value != nil &&
              !this.board.c[x][y].error)
        line.value = this.line.wall;

      // the value of the line between an empty cell and a non-empty
      // is user-defined
      else
        ;
    }

    // horizontal line
    else if (line.type == this.item.hline)
    {
      // there are always lines around "1"-cells
      if (this.board.c[x][y-1].value == 1 ||
          this.board.c[x][y].value == 1)
        line.value = this.line.wall;

      // the two adjacent cells have the same value
      else if (this.board.c[x][y-1].value == this.board.c[x][y].value)
        // there is never a line between two no-empty cells with
        // the same value
        if (this.board.c[x][y].value != nil)
          line.value = this.line.none;
        // the value of the line between empty cells is user-defined
        else
          ;

      // the two adjacent cells have different values
      else if (this.board.c[x][y-1].value != nil &&
               this.board.c[x][y].value != nil)
        // there is always a line between two no-empty cells with
        // a different value
        line.value = this.line.wall;

      // there is always a wall between a completed area and an
      // empty cell
      else if (this.board.c[x][y-1].value != nil &&
              !this.board.c[x][y-1].error ||
               this.board.c[x][y].value != nil &&
              !this.board.c[x][y].error)
        line.value = this.line.wall;

      // the value of the line between an empty cell and a non-empty
      // is user-defined
      else
        ;
    }

    // paint the line
    Object.getPrototypeOf(this).paintLine.call(this, line);

    // restore the original value of the line
    line.value = v;
  }

  /*********************************************************************
   * <paintCurrentValue>
   */
  this.paintCurrentValue = function()
  {
    var e = this.uie.value;
    var g = e.getContext('2d');

    g.fillStyle = this.uic.white;
    g.fillRect(0, 0, e.width, e.height);

    g.fillStyle = this.uic.none;
    g.strokeStyle = this.uic.black;

    if (this.enable.lines && !this.enable.cells)
      this.paintCaption2(g, "#", null, 0, 0, e.width, e.height, 90);
    else if (this.current.type != this.item.cell)
      this.paintCaption2(g, "1", null, 0, 0, e.width, e.height, 90);
    else if (this.current.value != nil)
      this.paintCaption2(g, this.current.value, null,
        0, 0, e.width, e.height, 90);
  }
}

/***********************************************************************
 * RUN
 */

Burokku.prototype = new Puzzle;

/***********************************************************************
 * THE END
 **********************************************************************/
