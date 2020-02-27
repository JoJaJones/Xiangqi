from Piece import Piece
from constants import *


class General(Piece):
    def __init__(self, board, color):
        if color == RED:
            pos = "e1"
        else:
            pos = "e10"

        super().__init__(board, GENERAL, color, pos, self)

        self._pieces_in_dir = {}

    def is_in_check(self, pos=None):
        if pos is not None and not self.is_valid_pos(pos):
            return True

        for direction in DIR_DICT:
            if self.find_threats_in_dir(direction, pos):
                return True

        for horse in HORSE_LIST:
            if self.horse_is_threat(horse, pos):
                return True

        return False

    def horse_is_threat(self, horse: tuple, pos: tuple = None):
        piece = self.get_relative_piece(horse, pos)

        if piece is None or piece.get_type() != HORSE:
            return False

        if piece.get_color() == self.get_color():
            return False

        # if abs(horse[0]) > abs(horse[1]):
        #     row_shift = 1
        #     if horse[0] < 0:
        #         row_shift *= -1
        #
        #     col_shift = horse[1]
        # else:
        #     row_shift = horse[0]
        #
        #     col_shift = 1
        #     if horse[1] < 0:
        #         col_shift *= -1

        blocking_pos = piece.get_blocking_pos(self._pos)
        blocking_piece = self.get_relative_piece(blocking_pos, pos)

        if blocking_piece is not None:
            return False

        if pos is None:
            pos = self._pos

        threat_pos = ((pos[0] + horse[0]), (pos[1] + horse[1]))

        return True

    def find_threats_in_dir(self, direction: str, pos: tuple = None):
        blocking_pieces = 0
        self.update_dir_pieces(direction, pos)

        if pos is None:
            cur_row, cur_col = self._pos
        else:
            cur_row, cur_col = pos

        for piece in self._pieces_in_dir[direction]:

            piece_type = piece.get_type()
            piece_color = piece.get_color()
            p_row, p_col = piece.get_pos()

            if self.get_color() == BLACK:
                soldier_dir_adjust = 1
            else:
                soldier_dir_adjust = -1

            if piece_color != self.get_color() and blocking_pieces < 2:
                if piece_type == SOLDIER and (abs(cur_col - p_col) == 1 ^ cur_row - p_row == soldier_dir_adjust):
                    return True
                elif piece_type == CANNON and blocking_pieces == 1:
                    return True
                elif (piece_type == CHARIOT or piece_type == GENERAL) and blocking_pieces == 0:
                    return True

            blocking_pieces += 1

        return False

    def ends_check(self, end_pos: tuple):
        return not self.is_in_check(end_pos)

    def causes_check(self, end_pos: tuple):
        return self.is_in_check(end_pos)

    def is_valid_pos(self, dest_pos):
        start_row, start_col = self._pos
        end_row, end_col = dest_pos
        if super().is_valid_pos(dest_pos):
            if self._board.leaves_palace(self._pos, dest_pos):
                return False

            if start_row != end_row and start_col != end_col:
                return False

            return True

        return False

    def get_rel_horses(self):
        horses = []
        for horse in HORSE_LIST:
            horses.append(self.get_relative_piece(horse))

        return horses

    def get_orth_pieces(self):
        self.update_dir_pieces()
        return self._pieces_in_dir

    def get_threats(self):
        threats = []
        for horse in HORSE_LIST:
            if self.horse_is_threat(horse):
                threats.append(self.get_relative_piece(horse))

        for direction in DIR_DICT:
            if self.find_threats_in_dir(direction):
                threats += [threat for threat in self._pieces_in_dir[direction]
                            if threat.get_color() != self.get_color() and threat.can_move(self.get_pos(), False)]

        return threats

    def update_dir_pieces(self, direction: str = None, pos: tuple = None):
        if direction is None:
            dir_list = [direction for direction in DIR_DICT]
        else:
            dir_list = [direction]

        for direction in dir_list:
            self._pieces_in_dir[direction] = []

            if pos is None:
                cur_row, cur_col = self._pos
            else:
                cur_row, cur_col = pos

            r_shift, c_shift = DIR_DICT[direction]

            cur_r_shift = r_shift
            cur_c_shift = c_shift

            while self.is_on_board(cur_row + cur_r_shift, cur_col + cur_c_shift):
                piece = self.get_relative_piece((cur_r_shift, cur_c_shift), pos)
                if piece is not None:
                    self._pieces_in_dir[direction].append(piece)

                cur_r_shift += r_shift
                cur_c_shift += c_shift