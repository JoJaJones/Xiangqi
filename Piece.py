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

    def is_unobstructed(self, dest_pos: tuple, num_allowed_between: int = 0):  # TODO
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
            return self.is_capture(dest_pos)

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
        # valid pos
        if not self.is_valid_pos(end_pos):
            return False

        # unobstructed
        if not self.is_unobstructed(end_pos):
            return False

        # causes_check
        if pieces_turn:
            if self._general.is_in_check():  # TODO General move error
                return self.ends_check(end_pos)
            else:
                return not self.causes_check(end_pos)

        return True

    def ends_check(self, end_pos: tuple):  # TODO screen logic
        if not self.causes_check(end_pos):
            threats = self._general.get_threats()
            blocking_pos = set()
            for i in range(len(threats)):
                if threats[i].get_type() == CANNON:
                    scr_dir = self._board.get_direction_to_pos(threats[i].get_pos(), self._general.get_pos())
                    screen = threats[i].get_screen(scr_dir)
                    if screen == self:
                        cannon_block = self.find_blocking_pos(threats[i].get_pos())
                        return end_pos not in cannon_block
                    screen_pos = screen.get_pos()

                if i == 0:
                    if threats[i].get_type() != HORSE:
                        blocking_pos = set(self.find_blocking_pos(threats[i].get_pos()) + [threats[i].get_pos()])
                    else:
                        blocking_pos = {threats[i].get_blocking_pos(self._general.get_pos()), threats[i].get_pos()}
                else:
                    if threats[i].get_type() != HORSE:
                        blocking_pos.intersection(set(self.find_blocking_pos(threats[i].get_pos()) + [threats[i].get_pos()]))
                    else:
                        blocking_pos.intersection({threats[i].get_blocking_pos(self._general.get_pos()), threats[i].get_pos()})

                if threats[i].get_type() == CANNON and screen_pos in blocking_pos:
                    blocking_pos.remove(screen.get_pos())

            if end_pos in blocking_pos:
                return True
            else:
                return False

        return False

    def find_blocking_pos(self, pos: tuple, direction: str = None):  # TODO
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

    def causes_check(self, end_pos: tuple):  # TODO
        temp = self._general.get_rel_horses()

        horses = [horse for horse in temp if horse is not None and
                  horse.get_type() == HORSE and horse.get_color() != self._color]

        for horse in horses:
            if horse.get_blocking_pos() == self._pos:
                return True

        row, col = self._pos
        g_row, g_col = self._general.get_pos()
        e_row, e_col = end_pos

        if row == g_row or col == g_col:
            if row == g_row:
                if e_row != row and self.leaving_dir_causes_check():
                    return True

            if col == g_col:
                if e_col != col and self.leaving_dir_causes_check():
                    return True

            if self.is_capture(end_pos) and self.capture_causes_check(end_pos):
                return True

        elif e_row == g_row or e_col == g_col:
            if self.entering_dir_causes_check(end_pos):
                return True

        return False

    def leaving_dir_causes_check(self):  # TODO
        orth_pieces = self._general.get_orth_pieces()
        for direction in DIR_DICT:
            if self in orth_pieces[direction]:
                orth_pieces = orth_pieces[direction]
                idx = orth_pieces.index(self)
                break

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

    def capture_causes_check(self, end_pos: tuple):  # TODO
        orth_pieces = self._general.get_orth_pieces()
        target_piece = self.get_piece_at_pos(end_pos)
        for direction in DIR_DICT:
            if target_piece in orth_pieces[direction]:
                orth_pieces = orth_pieces[direction]
                break

        if type(orth_pieces) == dict:
            return False
        else:
            idx = orth_pieces.index(target_piece)

        if self in orth_pieces:
            s_idx = orth_pieces.index(self)
        else:
            s_idx = None

        if idx > 3 and (s_idx is None or s_idx > 1):
            return False

        if s_idx == 0:
            if idx > 1 and orth_pieces[1].get_type() == CHARIOT and orth_pieces[1].get_color() != self._color:
                return True

            if (idx > 3 or idx == 1) and orth_pieces[2].get_type() == CANNON and orth_pieces[2].get_color() != self._color:
                return True

            return False

        if s_idx == 1:
            if orth_pieces[2].get_type() == CANNON and orth_pieces[2].get_color() != self._color:
                if idx == 0 or idx > 2:
                    return True

            return False

        return False

    def entering_dir_causes_check(self, end_pos: tuple):  # TODO
        s_row, s_col = self._pos
        g_row, g_col = self._general.get_pos()
        e_row, e_col = end_pos

        if self.is_capture(end_pos) and self.capture_causes_check(end_pos):
            return True

        end_dir = None

        for direction in DIR_DICT:
            r_shift, c_shift = DIR_DICT[direction]
            if abs(e_row - (g_row + r_shift)) < abs(e_row - g_row) or abs(e_col - (g_col + r_shift)) < abs(e_col - g_col):
                end_dir = direction
                break

        pieces = self._general.get_orth_pieces()[end_dir]

        if pieces[0].get_type() != CANNON:
            return False
        elif pieces[0].get_color() == self._color:
            return False
        elif abs(e_row - g_row) > abs(pieces[0].get_pos()[0] - g_row):
            return False
        elif abs(e_col - g_col) > abs(pieces[0].get_pos()[1] - g_col):
            return False

        return True


