from Chariot import Chariot
from constants import *

class Cannon(Chariot):
    def __init__(self, board, color: str, pos: str, gen):
        super().__init__(board, color, pos, gen, CANNON)

    def is_unobstructed(self, dest_pos: tuple, num_allowed_between: int = 0):
        if self.is_capture(dest_pos):
            if super().is_unobstructed(dest_pos, 1):
                return True

            return False
        else:
            if super().is_unobstructed(dest_pos):
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
