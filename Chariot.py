from Piece import Piece
from constants import *

class Chariot(Piece):
    def __init__(self, board, color: str, pos: str, gen: Piece, type: str = CHARIOT):
        super().__init__(board, type, color, pos, gen, 9)

    def is_valid_pos(self, dest_pos):
        start_row, start_col = self._pos
        end_row, end_col = dest_pos

        if super().is_valid_pos(dest_pos):
            if start_row != end_row and start_col != end_col:
                return False

            return True

        return False