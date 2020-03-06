from Chariot import Chariot
from constants import *

class Cannon(Chariot):
    def __init__(self, board, color: str, pos: str, gen):
        super().__init__(board, color, pos, gen, CANNON)

    def is_unobstructed(self, dest_pos: tuple, **kwargs):
        if self.is_capture(dest_pos):
            if super().is_unobstructed(dest_pos, 1):
                return True

            return False
        else:
            if super().is_unobstructed(dest_pos):
                return True

            return False

    def has_no_moves(self):
        if super().has_no_moves():
            for direction in DIR_DICT:
                row, col = self.get_pos()
                r_shift , c_shift = DIR_DICT[direction]
                row += 2 * r_shift
                col += 2 * c_shift
                while self.is_on_board(row, col):
                    piece = self.get_piece_at_pos((row, col))
                    if piece is not None and piece.get_color() != self.get_color():
                        return False

                    row += r_shift
                    col += c_shift

            return True

        return False

    def get_screen(self, direction):
        screen = None
        row, col = self.get_pos()
        r_shift, c_shift = DIR_DICT[direction]

        row += r_shift
        col += c_shift

        while screen is None and self.is_on_board(row, col):
            screen = self.get_piece_at_pos((row, col))
            row += r_shift
            col += c_shift

        return screen