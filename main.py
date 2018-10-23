from enum import Enum

class Type:
    def __init__(self, moves, attacks):
        self.moves = moves
        self.attacks = attacks
        pass

class Types(Enum):
    pass

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

class Piece:
    def __init__(self, type, position):
        position.__init__(self, position)
        self.type = type