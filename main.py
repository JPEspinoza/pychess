from enum import Enum

class Type:
    def __init__(self, movements, attacks = None):
        self.movements = movements
        if (attacks == None):
            self.attacks = movements

class Types(Enum):
    pawn = Type([[0,1]], [[1,1], [-1,1]])

class Piece:
    def __init__(self, column, row, type):
        self.column = column
        self.row = row
        self.type = type

#declare pieces like this
pawn1 = Piece(1,0, Types.pawn)

