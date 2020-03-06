from Piece import Piece
from constants import *


class Horse(Piece):
    def __init__(self, board, color: str, pos: str, gen: Piece):
        super().__init__(board, HORSE, color, pos, gen)

    def is_valid_pos(self, dest_pos: tuple):
        if super().is_valid_pos(dest_pos):
            start_row, start_col = self._pos
            end_row, end_col = dest_pos

            if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1:
                return True
            elif abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
                return True

        return False

    def is_unobstructed(self, dest_pos: tuple, **kwargs):
        if super().is_unobstructed(dest_pos):
            start_row, start_col = self._pos
            end_row, end_col = dest_pos

            if abs(start_row-end_row) > abs(start_col-end_col):
                blocking_pos = (start_row + end_row) // 2, start_col
            else:
                blocking_pos = start_row, (start_col + end_col) // 2

            piece = self.get_piece_at_pos(blocking_pos)

            if piece is None:
                return True

        return False

    def find_blocking_pos(self, pos: tuple = None, direction: str = None):
        row, col = self.get_pos()
        if pos is None:
            block_pos = {}
            if row - 2 >= 0:
                block_pos[UP] = row - 1, col

            if col - 2 >= 0:
                block_pos[LEFT] = row, col - 1

            if row + 2 < 10:
                block_pos[DOWN] = row + 1, col

            if col + 2 < 9:
                block_pos[RIGHT] = row, col + 1

            return block_pos
        else:
            if abs(row - pos[0]) == 2:
                return (row + pos[0]) // 2, col
            else:
                return row, (col + pos[1]) // 2
