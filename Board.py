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

    def get_positions(self):
        return self._positions

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

    def get_relative_piece(self, source_pos: tuple, pos_shift: tuple):
        s_row, s_col = source_pos
        r_shift, c_shift = pos_shift

        if self.is_on_board(s_row + r_shift, s_col + c_shift):
            return self._positions[s_row + r_shift][s_col + c_shift]
        else:
            return None

    def set_pos(self, pos: tuple, piece=None):
        row, col = pos
        self._positions[row][col] = piece

    def is_on_board(self, row: int, col: int):
        if col > 8 or col < 0:
            return False

        if row > 9 or row < 0:
            return False

        return True

    def convert_to_row_col(self, pos: str):
        col = self._ltr_dict[pos[0]]
        row = int(pos[1:])-1

        return row, col

    def convert_to_ltr_num(self, pos: tuple):
        row, col = pos

        return self._ltr_dict[col] + str(row + 1)

    def is_in_palace(self, pos: tuple, color: str = None):
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

    def leaves_palace(self, start_pos: tuple, end_pos: tuple):
        if self.is_in_palace(start_pos) and not self.is_in_palace(end_pos):
            return True
        else:
            return False

    def crosses_river(self, start_pos: tuple, end_pos: tuple):
        start_row = start_pos[0]
        end_row = end_pos[0]

        min_row = min(start_row, end_row)
        max_row = max(start_row, end_row)

        if min_row <= 4 and max_row >= 5:
            return True
        else:
            return False

    def print_board(self):
        print_dict = {SOLDIER: "S", CHARIOT: "T", ADVISOR: "A", CANNON: "C", ELEPHANT: "E", GENERAL: "G", HORSE: "H",
                      None: " "}
        color_dict = {RED: "\033[91m", BLACK: "\033[35m", None: "\033[97m"}
        board_table = self._positions
        for row in range(-1, len(board_table)):
            if row == -1:
                print("    ", end="")
                for col in range(len(board_table[0])):
                    print(" {} ".format("abcdefghi"[col]), end="")
            else:
                print(f" {row + 1:2d} ", end="")
                for col in range(len(board_table[row])):
                    piece = board_table[row][col]
                    if piece is None:
                        color = color_dict[None]
                        p_type = print_dict[None]
                    else:
                        color = color_dict[piece.get_color()]
                        p_type = print_dict[piece.get_type()]
                    if (0 <= row <= 2 or 7 <= row <= 9) and 3 <= col <= 5:
                        print(f"<{color}{p_type}\033[00m>", end="")
                    elif row == 4:
                        print(f"'{color}{p_type}\033[00m'", end="")
                    elif row == 5:
                        print(f",{color}{p_type}\033[00m,", end="")
                    else:
                        print(f"[{color}{p_type}\033[00m]", end="")

            print("")
