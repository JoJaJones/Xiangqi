from Board import Board
from General import General
from Soldier import Soldier
from Horse import Horse
from Elephant import Elephant
from Advisor import Advisor
from Chariot import Chariot
from Cannon import Cannon
from constants import *


class Player:
    def __init__(self, color: str, board: Board):
        if color == RED:
            base_row = 1
            shift_multiplier = 1
        else:
            base_row = 10
            shift_multiplier = -1

        self._board = board

        self._color = color

        self._pieces = {}
        self._general = General(board, color)
        self._pieces[f"e{base_row}"] = self._general

        self._pieces[f"d{base_row}"] = Advisor(board, color, f"d{base_row}", self._general)
        self._pieces[f"f{base_row}"] = Advisor(board, color, f"f{base_row}", self._general)
        self._pieces[f"c{base_row}"] = Elephant(board, color, f"c{base_row}", self._general)
        self._pieces[f"g{base_row}"] = Elephant(board, color, f"g{base_row}", self._general)
        self._pieces[f"b{base_row}"] = Horse(board, color, f"b{base_row}", self._general)
        self._pieces[f"h{base_row}"] = Horse(board, color, f"h{base_row}", self._general)
        self._pieces[f"a{base_row}"] = Chariot(board, color, f"a{base_row}", self._general)
        self._pieces[f"i{base_row}"] = Chariot(board, color, f"i{base_row}", self._general)

        pos = f"b{base_row + (2 * shift_multiplier)}"
        self._pieces[pos] = Cannon(board, color, pos, self._general)
        pos = f"h{base_row + (2 * shift_multiplier)}"
        self._pieces[pos] = Cannon(board, color, pos, self._general)

        row = base_row + (3 * shift_multiplier)
        for ltr in "acegi":
            self._pieces[f"{ltr}{row}"] = Soldier(board, color, f"{ltr}{row}", self._general)

    def get_general_pos(self):
        return self._general.get_pos()

    def is_in_check(self, pos=None):
        return self._general.is_in_check(pos)

    def update(self):
        for pos in self._pieces:
            if self._pieces[pos].get_pos() is None:
                del self._pieces[pos]
                break

    def make_move(self, start_pos: str, end_pos: str):
        if start_pos not in self._pieces:
            return False

        if self._pieces[start_pos].move_piece(end_pos):
            self._pieces[end_pos] = self._pieces[start_pos]
            del self._pieces[start_pos]
            return True
        else:
            return False

    def general_can_move(self):
        g_row, g_col = self.get_general_pos()

        for direction in DIR_DICT:
                r_shift, c_shift = DIR_DICT[direction]
                pos = (g_row + r_shift, g_col + c_shift)

                if not self.is_in_check(pos):
                    return True

        return False

    def is_stalemate(self):
        if self.is_in_check():
            return False

        if self.general_can_move():
            return False

        pieces_to_check = {}

        for piece in self._pieces.values():
            if piece.get_type() != GENERAL:
                pieces_to_check[piece.get_pos()] = piece

        rel_horses = self._general.get_rel_horses()
        for piece in rel_horses:
            if piece is not None and piece.get_type() == HORSE and piece.get_color() != self._color:
                block_pos = piece.find_blocking_pos(self.get_general_pos())
                if block_pos in pieces_to_check:
                    del pieces_to_check[block_pos]

        pieces_list = list(pieces_to_check.keys())
        for piece in pieces_list:
            if pieces_to_check[piece].has_no_moves():
                del pieces_to_check[piece]

        if len(pieces_to_check) == 0:
            return True

        return False

    def is_mate(self):
        if not self.is_in_check():
            return False

        if self.general_can_move():
            return False

        threats = self._general.get_threats()
        if len(threats) == 0:
            return False

        if len(threats) >= 3:
            return True

        blocking_pos = self._general.get_blocking_pos()
        screen = None
        if type(blocking_pos) == tuple:
            blocking_pos, screen = blocking_pos

        if len(blocking_pos) == 0:
            return True

        for piece in self._pieces.values():
            if piece == screen:
                if not piece.has_no_moves():
                    return False
            else:
                for pos in blocking_pos:
                    if piece.can_move(pos):
                        return False

        return True
