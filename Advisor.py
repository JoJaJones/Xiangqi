from Piece import Piece
from constants import *

class Advisor(Piece):
    def __init__(self, board, color: str, pos: str, gen: Piece):
        super().__init__(board, ADVISOR, color, pos, gen)

    def is_valid_pos(self, dest_pos):
        if super().is_valid_pos(dest_pos):
            cur_row, cur_col = self._pos
            if abs(cur_row - dest_pos[0]) != 1:
                return False

            if abs(cur_col - dest_pos[1]) != 1:
                return False

            if self._board_ref.leaves_palace(self._pos, dest_pos):
                return False

            return True

        return False

    def has_no_moves(self):
        for r in range(-1, 2, 2):
            for c in range(-1, 2, 2):
                row, col = self.get_pos()
                row += r
                col += c

                if self.can_move((row, col)):
                    return False

        return True
