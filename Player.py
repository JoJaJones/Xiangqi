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

    def update(self):
        for pos in self._pieces:
            if self._pieces[pos].get_pos() is None:
                del self._pieces[pos]
                break

    def is_in_check(self, pos=None):
        return self._general.is_in_check(pos)

    def make_move(self, start_pos: str, end_pos: str):
        if start_pos not in self._pieces:
            return False

        if self._pieces[start_pos].move_piece(end_pos):
            self._pieces[end_pos] = self._pieces[start_pos]
            del self._pieces[start_pos]
            return True
        else:
            return False

    def get_general_pos(self):
        return self._general.get_pos()

    def general_can_move(self):
        g_row, g_col = self.get_general_pos()

        for direction in DIR_DICT:
                r_shift, c_shift = DIR_DICT[direction]
                if not self.is_in_check((g_row + r_shift, g_col + c_shift)):
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
                block_pos = piece.get_blocking_pos(self.get_general_pos())
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
        threat_types = set([threat.get_type() for threat in threats])
        if len(threats) >= 3:
            return True

        if len(threats) == 1:
            for piece in self._pieces.values():
                if piece.can_move(threats[0].get_pos()):
                    return False

        orth_pieces = self._general.get_orth_pieces()
        if HORSE in threat_types and len(threat_types) == 1:
            blocking_pos = threats[0].get_blocking_pos()
            if len(threats) == 2 and threats[1].get_blocking_pos() != blocking_pos:
                return True

            for piece in self._pieces.values():
                if piece.can_move(blocking_pos):
                    return False

        elif HORSE in threat_types and len(threat_types) > 1:
            if CANNON in threat_types:
                if threats[0].get_type() == CANNON:
                    cannon = threats[0]
                    horse = threats[1]
                else:
                    cannon = threats[1]
                    horse = threats[0]

                c_row, c_col = cannon.get_pos()
                g_row, g_col = self._general.get_pos()

                if c_row > g_row:
                    direction = UP
                elif c_row < g_row:
                    direction = DOWN
                elif c_col > g_col:
                    direction = LEFT
                else:
                    direction = RIGHT

                screen = cannon.get_screen(direction)
                if screen.get_color() == self._color:
                    return screen.can_move(horse.get_pos()) or screen.can_move(horse.get_blocking_pos())
        else:
            for direction in DIR_DICT:
                if self._general.find_threats_in_dir(direction):
                    if direction == UP:
                        scr_dir = DOWN
                    elif direction == DOWN:
                        scr_dir = UP
                    elif direction == LEFT:
                        scr_dir = RIGHT
                    else:
                        scr_dir = LEFT

                    blocking_pos = []
                    for piece in orth_pieces[direction]:
                        if piece.get_color() != self._color and piece.can_move(self._general.get_pos(), False):
                            if piece.get_type() == CANNON:
                                screen = piece.get_screen(scr_dir)
                                if screen.get_color() != self._color and screen.get_type() == CANNON:
                                    return True
                                elif screen.get_color() == self._color and not screen.has_no_moves():
                                    return False

                            blocking_pos = self.find_blocking_spots(piece.get_pos(), direction)
                            break

                    if len(blocking_pos) == 0:
                        return True
                    else:
                        for spot in blocking_pos:
                            for piece in self._pieces.values():
                                if piece.can_move(spot):
                                    return False

                        return True


    def find_blocking_spots(self, pos: tuple, direction: str):
        if direction == UP:
            search_dir = DOWN
        elif direction == DOWN:
            search_dir = UP
        elif direction == LEFT:
            search_dir = RIGHT
        else:
            search_dir = LEFT

        r_shift, c_shift = DIR_DICT[search_dir]
        row, col = pos

        row += r_shift
        col += c_shift


        blocking_pos = []
        while (row, col) != self._general.get_pos():
            if self._general.get_piece_at_pos((row, col)) is None:
                blocking_pos.append((row, col))
            row += r_shift
            col += c_shift

        return blocking_pos

    # def is_mate(self):
    #     row, col = self._general.get_pos()
    #
    #     if not self.is_in_check():
    #         return False
    #
    #     for direction in DIR_DICT:
    #         r_shift, c_shift = DIR_DICT[direction]
    #         if not self.is_in_check((row + r_shift, col + c_shift)):
    #             return False
    #
    #     pieces = self._general.get_threats()
    #     if pieces is not None:
    #         direction = pieces[1]
    #         pieces = pieces[0]
    #         if direction == HORSE:
    #             threat = pieces[0]
    #
    #         threat = None
    #         can_take = True
    #         for i in range(len(pieces)):
    #             if pieces[i].get_color() != self._color:
    #                 if threat is None and pieces[i].can_move(pieces[i].get_pos, self._general.get_pos()):
    #                     threat = pieces[i]
    #                     if i+1 < len(pieces) and pieces[i+1].get_type() == CANNON:
    #                         if pieces[i+1].get_color() != self._color:
    #                             can_take = False
    #
    #                     if threat.get_type() == CANNON and not can_take:
    #                         return True
    #
    #                     break
    #
    #         blocking_spots = self.get_target_pos(threat, can_take)
    #
    #         while len(blocking_spots) > 0:
    #             cur_target = blocking_spots[0]
    #             blocking_spots = blocking_spots[1:]
    #             for piece in self._pieces:
    #                 if piece != GENERAL:
    #                     if self._pieces[piece].can_move(self._pieces[piece].get_pos(), cur_target):
    #                         if not self.piece_is_blocking_check(self._pieces[piece]):
    #                             return False
    #
    #         return True
    #
    #     return False

    # def is_mate(self):  # TODO Cannon screen logic
    #     threat_list = []
    #     cannon_screen = None
    #
    #     row, col = self._general.get_pos()
    #
    #     if not self.is_in_check():
    #         return False
    #
    #     for direction in DIR_DICT:
    #         r_shift, c_shift = DIR_DICT[direction]
    #         if not self.is_in_check((row + r_shift, col + c_shift)):
    #             return False
    #
    #     threats = self._general.get_threats()
    #     num_moves = 0
    #     if threats is not None:
    #         blocking_spots = []
    #         for pieces in threats:
    #             direction = pieces[1]
    #             pieces = pieces[0]
    #             threat = None
    #             if direction == HORSE:
    #                 threat = pieces[0]
    #                 threat_list.append(HORSE)
    #
    #             can_take = True
    #             # for i in range(len(pieces)):
    #             #     if pieces[i].get_color() != self._color:
    #             #         if threat is None and pieces[i].can_move(pieces[i].get_pos, self._general.get_pos()):
    #             #             threat = pieces[i]
    #             #             if i + 1 < len(pieces) and pieces[i + 1].get_type() == CANNON:
    #             #                 if pieces[i + 1].get_color() != self._color:
    #             #                     can_take = False
    #             #
    #             #             if threat.get_type() == CANNON and not can_take:
    #             #                 return True
    #             #
    #             #             break
    #
    #             for i in range(len(pieces)):
    #                 if pieces[i].get_color() != self._color:
    #                     if pieces[i].can_move(pieces[i].get_pos, self._general.get_pos()):
    #                         threat_type = pieces[i].get_type()
    #                         threat_list.append(threat_type)
    #                         if pieces[i + 1].get_color() != self._color and pieces[i + 1].get_type() == CANNON:
    #                             can_take = False
    #
    #                         if threat_type == CANNON:
    #                             cannon_screen = pieces[i-1]
    #
    #
    #             blocking_spots.append(set(self.get_target_pos(threat, can_take)))
    #
    #         while len(blocking_spots) > 1:
    #             blocking_spots[0] = blocking_spots[0].intersection(blocking_spots[-1])
    #             blocking_spots = blocking_spots[:-1]
    #
    #         blocking_spots = list(blocking_spots[0])
    #
    #         while len(blocking_spots) > 0:
    #             cur_target = blocking_spots[0]
    #             blocking_spots = blocking_spots[1:]
    #             for piece in self._pieces:
    #                 if piece != GENERAL:
    #                     if self._pieces[piece].can_move(self._pieces[piece].get_pos(), cur_target):
    #                         if not self.piece_is_blocking_check(self._pieces[piece]):
    #                             num_moves += 1
    #
    #         return num_moves != 1
    #
    #     return False

    def piece_is_blocking_check(self, piece):
        orth_pieces = self._general.get_orth_pieces()
        for direction in orth_pieces:
            if piece in orth_pieces[direction]:
                if orth_pieces[direction].index(piece) == 0:
                    if len(orth_pieces[direction]) > 1:
                        threat = orth_pieces[direction][1]
                        if threat.get_type() == CHARIOT and threat.get_color() != self._color:
                            return True

                        if len(orth_pieces[direction]) > 2:
                            threat = orth_pieces[direction][2]
                            if threat.get_type() == CANNON and threat.get_color() != self._color:
                                return True

        return False

    def get_target_pos(self, piece, can_take=True):
        blocking_pos = []
        if can_take:
            blocking_pos.append(piece.get_pos())

        piece_type = piece.get_type()
        row, col = self._general.get_pos()

        if piece_type == HORSE:
            h_row, h_col = piece.get_pos()

            if abs(h_row - row) == 2:
                b_row = h_row + row
                b_row //= 2
                b_col = h_col
            else:
                b_col = h_col + col
                b_col //= 2
                b_row = h_row

            blocking_pos.append((b_row, b_col))
        elif piece_type != SOLDIER:
            p_row, p_col = piece.get_pos()
            if p_row == row:
                if p_col < col:
                    shift = -1
                else:
                    shift = 1
                for i in range(col, p_col, shift):
                    if i != col:
                        blocking_pos.append((row, i))
            else:
                if p_row < row:
                    shift = -1
                else:
                    shift = 1
                for i in range(row, p_row, shift):
                    if i != row:
                        blocking_pos.append((i, col))

        return blocking_pos
