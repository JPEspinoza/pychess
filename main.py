from enum import Enum

class Type:
    def __init__(self, movements, attacks = None):
        self.movements = movements
        if (attacks == None):
            self.attacks = movements

class Types(Enum):
    #can move one column, attack one column and one row
    pawn = Type([[0,1]], [[1,1], [-1,1]])
    #can move in any direction
    king = Type([[True, True]])

class Piece():
    def __init__(self, column, row, type):
        self.column = column
        self.row = row
        self.type = type

#declare pieces like this
pawn1 = Piece(1,0, Types.pawn)

