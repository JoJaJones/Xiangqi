from Board import Board
from constants import *


class Piece:
    def __init__(self, board: Board, piece_type: str, color: str, pos: str, ref_piece, max_move_distance: int = 1):
        self._board = board
        self._type = piece_type
        self._color = color
        self._pos = self._board.convert_to_row_col(pos)
        self._board.set_pos(self._pos, self)
        self._general = ref_piece
        self._move_distance = max_move_distance

    def get_color(self):
        return self._color

    def get_type(self):
        return self._type

    def get_pos(self):
        return self._pos

    def get_piece_at_pos(self, pos: tuple):
        return self._board.get_pos(pos)

    def get_relative_piece(self, pos_shift: tuple, pos: tuple = None):
        if pos is None:
            pos = self._pos

        return self._board.get_relative_piece(pos, pos_shift)

    def set_pos(self, pos: tuple = None):
        if pos is None:  # clear piece from board
            self._board.set_pos(self._pos)
            self._pos = None
        else:  # update board and pos
            self._board.set_pos(pos, self)
            self._pos = pos

    def is_valid_pos(self, dest_pos: tuple):
        start_row, start_col = self._pos
        end_row, end_col = dest_pos

        if not self.is_on_board(end_row, end_col):
            return False

        if start_row == end_row and abs(end_col - start_col) > self._move_distance:
            return False

        if start_col == end_col and abs(end_row - start_row) > self._move_distance:
            return False

        dest_piece = self._board.get_pos(dest_pos)
        if dest_piece is not None and dest_piece.get_color() == self._color:
            return False

        return True

    def is_on_board(self, row: int, col: int):
        return self._board.is_on_board(row, col)

    def is_capture(self, pos: tuple):
        piece = self.get_piece_at_pos(pos)
        if piece is not None and piece.get_color() != self._color:
            return True
        else:
            return False

    def is_unobstructed(self, dest_pos: tuple, num_allowed_between: int = 0):
        row, col = self._pos
        end_row, end_col = dest_pos

        num_between = 0
        direction = self._board.get_direction_to_pos(self._pos, dest_pos)

        if direction is not None:
            r_shift, c_shift = DIR_DICT[direction]
            row += r_shift
            col += c_shift
            while self.is_on_board(row, col) and (col != end_col or row != end_row):
                if self.get_piece_at_pos((row, col)) is not None:
                    if num_between == num_allowed_between:
                        return False
                    else:
                        num_between += 1

                row += r_shift
                col += c_shift

        piece = self._board.get_pos((end_row, end_col))
        if piece is not None:
            return self.is_capture(dest_pos) and num_between == num_allowed_between

        return num_between == num_allowed_between

    def has_no_moves(self):
        for direction in DIR_DICT:
            row, col = self.get_pos()
            distance = 1
            while self.is_on_board(row, col) and distance <= self._move_distance:
                row += DIR_DICT[direction][0]
                col += DIR_DICT[direction][1]
                distance += 1
                if self.can_move((row, col)):
                    return False

        return True

    def move_piece(self, dest: str):
        dest_pos = self._board.convert_to_row_col(dest)
        if self.can_move(dest_pos):
            if self.is_capture(dest_pos):
                self._board.get_pos(dest_pos).set_pos()

            self.set_pos()
            self._pos = dest_pos
            self.set_pos(self._pos)

            return True

        return False

    def can_move(self, end_pos: tuple, pieces_turn: bool = True):
        if not self.is_valid_pos(end_pos):
            return False

        if not self.is_unobstructed(end_pos):
            return False

        if pieces_turn:
            if self._general.is_in_check():
                return self.ends_check(end_pos)
            else:
                return not self.causes_check(end_pos)

        return True

    def ends_check(self, end_pos: tuple):
        if not self.causes_check(end_pos):
            block_pos = self._general.get_blocking_pos()

            if type(block_pos) == tuple:
                block_pos, screen = block_pos
                if screen == self:
                    direction = self._board.get_direction_to_pos(self._general.get_pos(), self._pos)
                    return not self.leaving_dir_causes_check(direction)

            if end_pos in block_pos:
                return True
            else:
                return False

        return False

    def find_blocking_pos(self, pos: tuple, direction: str = None):
        if direction is None:
            search_dir = self._board.get_direction_to_pos(pos, self._general.get_pos())

        r_shift, c_shift = DIR_DICT[search_dir]
        row, col = pos

        row += r_shift
        col += c_shift

        blocking_pos = []
        while (row, col) != self._general.get_pos():
            piece = self._general.get_piece_at_pos((row, col))
            if piece is None:
                blocking_pos.append((row, col))

            row += r_shift
            col += c_shift

        return blocking_pos

    def causes_check(self, end_pos: tuple):
        s_row, s_col = self._pos
        g_row, g_col = self._general.get_pos()
        e_row, e_col = end_pos

        if abs(s_row - g_row) == 1 and abs(s_col - g_col) == 1:
            temp = self._general.get_rel_horses()

            horses = [horse for horse in temp if horse is not None and
                      horse.get_type() == HORSE and horse.get_color() != self._color]

            for horse in horses:
                if horse.find_blocking_pos() == self._pos:
                    return True

        if s_row == g_row or s_col == g_col:
            dir_from_gen = self._board.get_direction_to_pos(self._general.get_pos(), self._pos)
            dir_to_gen = self._board.get_direction_to_pos(self._pos, self._general.get_pos())
            move_dir = self._board.get_direction_to_pos(self._pos, end_pos)

            if move_dir != dir_from_gen and move_dir != dir_to_gen and self.leaving_dir_causes_check(dir_from_gen):
                return True

        if e_row == g_row or e_col == g_col:
            dir_from_gen = self._board.get_direction_to_pos(self._general.get_pos(), end_pos)
            if self.entering_dir_causes_check(end_pos, dir_from_gen):
                return True

        return False

    def leaving_dir_causes_check(self, direction: str):
        orth_pieces = self._general.get_orth_pieces()[direction]
        idx = orth_pieces.index(self)

        if len(orth_pieces) == 1:
            return False
        elif idx > 2 or idx == len(orth_pieces) - 1:
            return False
        elif len(orth_pieces) >= 3 and idx < 2 and orth_pieces[2].get_type() == CANNON \
                and orth_pieces[2].get_color() != self._color:
            return True
        elif len(orth_pieces) >= 2 and idx == 0 and \
                (orth_pieces[1].get_type() == CHARIOT or orth_pieces[1].get_type() == GENERAL) \
                and orth_pieces[1].get_color() != self._color:
            return True

        return False

    def capture_causes_check(self, end_pos: tuple, direction: str):
        orth_pieces = self._general.get_orth_pieces()[direction]
        target_piece = self.get_piece_at_pos(end_pos)

        idx = orth_pieces.index(target_piece)

        if self in orth_pieces:
            s_idx = orth_pieces.index(self)
        else:
            s_idx = None

        if idx > 3 and (s_idx is None or s_idx > 1):
            return False

        if s_idx == 1:
            if orth_pieces[2].get_type() == CANNON and orth_pieces[2].get_color() != self._color:
                if idx == 0 or idx > 2:
                    return True

            return False

        if idx > 1 and orth_pieces[1].get_type() == CHARIOT and orth_pieces[1].get_color() != self._color:
            return True

        if (idx > 3 or idx == 1) and orth_pieces[2].get_type() == CANNON and orth_pieces[2].get_color() != self._color:
            return True

        return False

    def entering_dir_causes_check(self, end_pos: tuple, direction: str):
        g_row, g_col = self._general.get_pos()
        e_row, e_col = end_pos

        if self.is_capture(end_pos) and self.capture_causes_check(end_pos, direction):
            return True

        pieces = self._general.get_orth_pieces()[direction]

        if len(pieces) == 0:
            return False
        elif pieces[0].get_type() != CANNON or pieces[0].get_color() == self._color:
            return False
        elif abs(e_row - g_row) > abs(pieces[0].get_pos()[0] - g_row):
            return False
        elif abs(e_col - g_col) > abs(pieces[0].get_pos()[1] - g_col):
            return False

        return True
