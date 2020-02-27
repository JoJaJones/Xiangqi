from Piece import Piece
from constants import *

class Soldier(Piece):
    def __init__(self, board, color, pos, gen):
        super().__init__(board, SOLDIER, color, pos, gen)
        self._crossed_river = False

        if color == RED:
            self._row_shift = 1
        else:
            self._row_shift = -1

    def is_valid_pos(self, dest_pos):
        start_row, start_col = self._pos
        end_row, end_col = dest_pos

        if super().is_valid_pos(dest_pos):
            if not self._crossed_river:
                if start_row == end_row:
                    return False

                if start_col != end_col:
                    return False

                if start_row + self._row_shift != end_row:
                    return False
            else:
                if start_row != end_row and end_row != self._row_shift + start_row:
                    return False

            return True

    def move_piece(self, dest):
        cur_pos = self._pos
        if super().move_piece(dest):
            if self._board.crosses_river(cur_pos, self._pos):
                self._crossed_river = True

            return True

        return False