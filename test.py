
class Type:
    def __init__(self, sprite, movements, attacks = None):
        self.movements = movements
        self.attacks = attacks
        if(self.attacks == None):
            self.attacks = movements
        self.sprite = sprite

pawnMoves = [[0,1]]
pawnAttacks = [[1,1], [-1,1]]
pawn = Type("test", pawnMoves, pawnAttacks)