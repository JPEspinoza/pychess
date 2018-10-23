from enum import Enum

class Type:
    def __init__(self, moves, attacks):
        self.moves = moves
        self.attacks = attacks
        pass

class Types(Enum):
    king = Type.__init__(1,2)

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

class Piece:
    def __init__(self, type, position):
        position.__init__(self, position)
        self.type = type

