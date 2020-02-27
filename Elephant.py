from Piece import Piece
from constants import *

class Elephant(Piece):
    def __init__(self, board, color: str, pos: str, gen: Piece):
        super().__init__(board, ELEPHANT, color, pos, gen)

    def is_valid_pos(self, dest_pos: tuple):
        if super().is_valid_pos(dest_pos):
            cur_row, cur_col = self._pos
            if abs(cur_col - dest_pos[1]) != 2:
                return False

            if abs(cur_row - dest_pos[0]) != 2:
                return False

            if self._board.crosses_river(self._pos, dest_pos):
                return False

            return True

        return False

    def is_unobstructed(self, dest_pos: tuple, **kwargs):
        if super().is_unobstructed(dest_pos):
            cur_row, cur_col = self._pos

            block_row = (cur_row + dest_pos[0]) // 2
            block_col = (cur_col + dest_pos[1]) // 2

            piece = self.get_piece_at_pos((block_row, block_col))
            if piece is not None:
                return False

            return True

        return False

    def has_no_moves(self):
        for r in range(-2, 3, 4):
            for c in range(-2, 3, 4):
                row, col = self.get_pos()

                row += r
                col += c

                if self.can_move((row, col)):
                    return False

        return True
