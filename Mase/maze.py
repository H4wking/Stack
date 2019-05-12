# Implements the Maze ADT using a 2-D array.
from arrays import Array2D
from lliststack import Stack

class Maze :
    # Define constants to represent contents of the maze cells.
    MAZE_WALL = "* "
    PATH_TOKEN = "x "
    TRIED_TOKEN = "o "

    # Creates a maze object with all cells marked as open.
    def __init__( self, num_rows, num_cols ):
        self._mazeCells = Array2D( num_rows, num_cols )
        self._startCell = None
        self._exitCell = None

    # Returns the number of rows in the maze.
    def num_rows( self ):
        return self._mazeCells.num_rows()

    # Returns the number of columns in the maze.
    def num_cols( self ):
        return self._mazeCells.num_cols()

    # Fills the indicated cell with a "wall" marker.
    def setWall( self, row, col ):
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._mazeCells[row, col] = self.MAZE_WALL

    # Sets the starting cell position.
    def setStart( self, row, col ):
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._startCell = _CellPosition( row, col )

    # Sets the exit cell position.
    def setExit( self, row, col ):
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._exitCell = _CellPosition( row, col )

    # Attempts to solve the maze by finding a path from the starting cell
    # to the exit. Returns True if a path is found and False otherwise.
    def findPath( self ):
        current = _CellPosition(self._startCell.row, self._startCell.col)
        self._markPath(current.row, current.col)
        options = [(current.row - 1, current.col), (current.row, current.col + 1),
                   (current.row + 1, current.col), (current.row, current.col - 1)]
        while not self._exitFound(current.row, current.col):
            for i, j in options:
                valid_found = False
                if self._validMove(i, j):
                    previous = _CellPosition(current.row, current.col)
                    valid_found = True
                    current = _CellPosition(i, j)
                    self._markPath(current.row, current.col)
                    self.draw()
                    break
            if not valid_found:
                options = [(previous.row - 1, previous.col), (previous.row, previous.col + 1),
                           (previous.row + 1, previous.col), (previous.row, previous.col - 1)]
                options.remove((current.row, current.col))
                self._markTried(current.row, current.col)
                current = previous
                self.draw()
            else:
                options = [(current.row - 1, current.col), (current.row, current.col + 1),
                           (current.row + 1, current.col), (current.row, current.col - 1)]
        return True




    # Resets the maze by removing all "path" and "tried" tokens.
    def reset( self ):
        pass

    # Prints a text-based representation of the maze.
    def draw( self ):
        maze = ""
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                maze += self._mazeCells[i, j] if self._mazeCells[i, j] else "  "
            maze += "\n"
        print(maze)

    # Returns True if the given cell position is a valid move.
    def _validMove( self, row, col ):
        return row >= 0 and row < self.num_rows() \
               and col >= 0 and col < self.num_cols() \
               and self._mazeCells[row, col] is None

    # Helper method to determine if the exit was found.
    def _exitFound( self, row, col ):
        return row == self._exitCell.row and col == self._exitCell.col

    # Drops a "tried" token at the given cell.
    def _markTried( self, row, col ):
        self._mazeCells[row, col] = self.TRIED_TOKEN

    # Drops a "path" token at the given cell.
    def _markPath( self, row, col ):
        self._mazeCells[row, col] = self.PATH_TOKEN

# Private storage class for holding a cell position.
class _CellPosition( object ):
    def __init__( self, row, col ):
        self.row = row
        self.col = col