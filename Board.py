from constants import *


class Board:
    def __init__(self):
        self._positions = []
        self._ltr_dict = {}

        for row in range(NUM_ROWS):
            self._positions.append([])
            for col in range(NUM_COLS):
                self._positions[row].append(None)

        row_ltrs = "abcdefghi"
        for i in range(len(row_ltrs)):
            self._ltr_dict[row_ltrs[i]] = i
            self._ltr_dict[i] = row_ltrs[i]

    def get_pos(self, pos: tuple):
        row, col = pos
        return self._positions[row][col]

    def set_pos(self, pos: tuple, piece=None):
        row, col = pos
        self._positions[row][col] = piece

    def get_positions(self):
        return self._positions

    def convert_to_row_col(self, pos: str):
        col = self._ltr_dict[pos[0]]
        row = int(pos[1:])-1

        return row, col

    def convert_to_ltr_num(self, pos: tuple):
        row, col = pos

        return self._positions[col] + str(row + 1)

    def is_in_palace(self, pos, color=None):
        if type(pos) == str:
            row, col = self.convert_to_row_col(pos)
        else:
            row, col = pos

        in_palace_col = 3 <= col <= 5

        in_red = 2 >= row >= 0
        in_red = in_red and in_palace_col

        in_black = 9 >= row >= 7
        in_black = in_black and in_palace_col

        if color is None:
            return in_black or in_red
        elif color == RED:
            return in_red
        else:
            return in_black

    def leaves_palace(self, start_pos, end_pos):
        if self.is_in_palace(start_pos) and not self.is_in_palace(end_pos):
            return True
        else:
            return False

    def enters_palace(self, start_pos, end_pos):
        if not self.is_in_palace(start_pos) and self.is_in_palace(end_pos):
            return True
        else:
            return False

    def crosses_river(self, start_pos, end_pos):
        if type(start_pos) == str:
            start_pos = self.convert_to_row_col(start_pos)

        if type(end_pos) == str:
            end_pos = self.convert_to_row_col(end_pos)

        start_row = start_pos[0]
        end_row = end_pos[0]

        min_row = min(start_row, end_row)
        max_row = max(start_row, end_row)

        if min_row <= 4 and max_row >= 5:
            return True
        else:
            return False

    def get_direction_to_pos(self, source_pos: tuple, dest_pos: tuple):
        s_row, s_col = source_pos

        d_row, d_col = dest_pos

        if s_row == d_row:
            if s_col < d_col:
                return RIGHT
            else:
                return LEFT
        elif s_col == d_col:
            if s_row > d_row:
                return UP
            else:
                return DOWN
        else:
            return None