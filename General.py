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

        blocking_pos = piece.find_blocking_pos(self._pos)
        blocking_piece = self.get_piece_at_pos(blocking_pos)

        if blocking_piece is not None:
            return False

        return True

    def find_threats_in_dir(self, direction: str, pos: tuple = None):
        self.update_dir_pieces(direction, pos)
        pieces_in_dir = self._pieces_in_dir[direction]

        if pos is None:
            cur_row, cur_col = self._pos
        else:
            cur_row, cur_col = pos

        for piece in pieces_in_dir:
            piece_type = piece.get_type()
            piece_color = piece.get_color()

            if piece_color != self.get_color():
                if piece.can_move((cur_row, cur_col)):
                    return True

                piece_idx = pieces_in_dir.index(piece)
                if (piece_type == GENERAL and piece_idx == 0) or (piece_type == CANNON and piece_idx == 1):
                    return True

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

    def get_blocking_pos(self):  # TODO refactor
        threats = self._general.get_threats()
        block_sets = []
        s_screen = None

        for i in range(len(threats)):
            if threats[i].get_type() == CANNON:
                scr_dir = self._board.get_direction_to_pos(threats[i].get_pos(), self._general.get_pos())
                screen = threats[i].get_screen(scr_dir)
                cannon_block = self.find_blocking_pos(threats[i].get_pos()) + [threats[i].get_pos()]
                if screen.get_pos() in cannon_block:
                    cannon_block.remove(screen.get_pos())

                if screen.get_color() == self._color:
                    s_screen = screen, cannon_block

                if screen.get_type() == CANNON and s_screen is None:
                    return set(), None
                else:
                    block_sets.append(set(cannon_block))

            elif threats[i].get_type() != HORSE:
                block_sets.append(set(self.find_blocking_pos(threats[i].get_pos()) + [threats[i].get_pos()]))
            else:
                block_sets.append({threats[i].find_blocking_pos(self._general.get_pos()), threats[i].get_pos()})

        blocking_pos = block_sets[0]
        for i in range(1, len(block_sets)):
            blocking_pos.intersection(block_sets[i])

        if s_screen is not None:
            if len(blocking_pos) == 0:
                if block_sets[0] == s_screen[1]:
                    blocking_pos = set()
                for i in range(1, len(block_sets)):
                    if i == 1 and len(blocking_pos) == 0:
                        blocking_pos.union(block_sets[i])
                    else:
                        blocking_pos.intersection(block_sets[i])

            s_screen = s_screen[0]

        return blocking_pos, s_screen

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
