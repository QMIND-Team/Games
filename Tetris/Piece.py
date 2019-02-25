from enum import Enum


class BitMaps(Enum):
    I = [[[True], [True], [True], [True]], [[True, True, True, True]]]
    O = [[[True, True], [True, True]]]
    T = [[[False, True, False], [True, True, True]], [[False, True], [True, True], [False, True]], [[True, True, True], [False, True, False]], [[True, False], [True, True], [True, False]]]
    S = [[[True, False], [True, True], [False, True]], [[True, True, False], [False, True, True]]]
    Z = [[[True, False], [True, True], [False, True]], [[False, True, True], [True, True, False]]]
    J = [[[True, True], [False, True], [False, True]], [[True, True, True], [True, False, False]], [[True, False], [True, False], [True, True]], [[False, False, True], [True, True, True]]]
    L = [[[True, True], [True, False], [True, False]], [[True, False, False], [True, True, True]], [[False, True], [False, True], [True, True]], [[True, True, True], [False, False, True]]]


intToBitMaps = [BitMaps.I, BitMaps.O, BitMaps.T, BitMaps.S, BitMaps.Z, BitMaps.Z, BitMaps.J, BitMaps.L]

class Piece(object):
    def __init__(self, bitMaps):
        self.bitMaps = bitMaps  # rename to something like "type" or "Tetrominoe"
        self.ori = 0
        self.col = 3
        self.row = 36

    def getBitMap(self, ori=None):
        if ori is None:
            ori = self.ori
        return self.bitMaps.value[ori]

    def width(self, ori=None):
        if ori is not None:
            return len(self.bitMaps.value[ori][0])
        else:
            return len(self.getBitMap()[0])

    def height(self, ori=None):
        if ori is not None:
            return len(self.getBitMap(ori=ori))
        else:
            return len(self.getBitMap())

    def numOrientations(self):
        return len(self.bitMaps.value)
