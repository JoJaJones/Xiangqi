NUM_ROWS = 10
NUM_COLS = 9

UNFINISHED = "UNFINISHED"
WINS = ["BLACK_WON", "RED_WON"]

GENERAL = "general"
ADVISOR = "advisor"
ELEPHANT = "elephant"
HORSE = "horse"
CHARIOT = "chariot"
CANNON = "cannon"
SOLDIER = "soldier"

RED = "red"
BLACK = "black"

UP = "up"
LEFT = "left"
RIGHT = "right"
DOWN = "down"

DIR_DICT = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}
HORSE_LIST = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]

PIECE_DICT = {GENERAL: (["e"], 0),
              ADVISOR: (["d", "f"], 0),
              ELEPHANT: (["c", "g"], 0),
              HORSE: (["b", "h"], 0),
              CHARIOT: (["a", "i"], 0),
              CANNON: (["b", "h"], 2),
              SOLDIER: (["a", "c", "e", "g", "i"], 3)}


class XiangqiGame:
    def __init__(self):
        self._board = Board()
        self._players = [Player(RED, self._board), Player(BLACK, self._board)]
        self._current_turn = 0
        self._game_state = UNFINISHED

    def get_game_state(self):
        return self._game_state

    def is_in_check(self, color: str):
        if color == RED:
            return self._players[0].is_in_check()
        elif color == BLACK:
            return self._players[1].is_in_check()
        else:
            return None

    def make_move(self, start_pos: str, end_pos: str):
        print(f"{start_pos} => {end_pos}", end="")
        if self._game_state == UNFINISHED:
            if self._players[self._current_turn].make_move(start_pos, end_pos):
                print("")
                self._current_turn ^= 1
                self._players[self._current_turn].update()

                if self._players[self._current_turn].is_mate() or self._players[self._current_turn].is_stalemate():
                    self._game_state = WINS[self._current_turn]

                self.print_board()

                return True

            print(" Invalid!")
            return False
        else:
            print(" Invalid! Game is over!")
            return False

    def print_board(self):
        self._board.print_board()


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
        dest_piece = self._board.get_pos(dest_pos)
        if dest_piece is not None and dest_piece.get_color() == self._color:
            return False

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
            block_pos, screen = self._general.get_blocking_pos()

            if screen is not None and screen == self:
                direction = self._board.get_direction_to_pos(self._general.get_pos(), self._pos)
                if self._pos[0] == self._general.get_pos()[0]:
                    idx = 0
                else:
                    idx = 1

                cannon = self._general.get_orth_pieces()[direction][1]
                general_pos = self._general.get_pos()[idx^1]

                is_still_screen = end_pos[idx] != self._general.get_pos()[idx]
                is_still_screen |= self._board.get_direction_to_pos(self._general.get_pos(), end_pos) != direction
                is_still_screen |= abs(end_pos[idx^1] - general_pos) > abs(cannon.get_pos()[idx^1] - general_pos)
                is_still_screen = not is_still_screen

                if not is_still_screen:
                    return not self.leaving_dir_causes_check(direction)
                else:
                    return False

            return end_pos in block_pos

        return False

    def find_blocking_pos(self, pos: tuple, direction: str = None):
        if direction is None:
            direction = self._board.get_direction_to_pos(pos, self._general.get_pos())

        r_shift, c_shift = DIR_DICT[direction]
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

            blocked_list = []
            for horse in horses:
                if horse.find_blocking_pos(self._general.get_pos()) == self._pos:
                    blocked_list.append(horse)

            if len(blocked_list) == 0:
                return False

            if len(blocked_list) > 1 or end_pos != blocked_list[0].get_pos():
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
                if screen.get_pos in cannon_block:
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

class Advisor(Piece):
    def __init__(self, board, color: str, pos: str, gen: Piece):
        super().__init__(board, ADVISOR, color, pos, gen)

    def is_valid_pos(self, dest_pos):
        if super().is_valid_pos(dest_pos):
            cur_row, cur_col = self._pos
            if abs(cur_row - dest_pos[0]) != 1:
                return False

            if abs(cur_col - dest_pos[1]) != 1:
                return False

            if self._board.leaves_palace(self._pos, dest_pos):
                return False

            return True

        return False

    def has_no_moves(self):
        for r in range(-1, 2, 2):
            for c in range(-1, 2, 2):
                row, col = self.get_pos()
                row += r
                col += c

                if self.can_move((row, col)):
                    return False

        return True

class Chariot(Piece):
    def __init__(self, board, color: str, pos: str, gen: Piece, type: str = CHARIOT):
        super().__init__(board, type, color, pos, gen, 9)

    def is_valid_pos(self, dest_pos):
        start_row, start_col = self._pos
        end_row, end_col = dest_pos

        if super().is_valid_pos(dest_pos):
            if start_row != end_row and start_col != end_col:
                return False

            return True

        return False
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
class Elephant(Piece):
    def __init__(self, board, color: str, pos: str, gen: Piece):
        super().__init__(board, ELEPHANT, color, pos, gen)

    def is_valid_pos(self, dest_pos: tuple):
        if super().is_valid_pos(dest_pos):
            cur_row, cur_col = self._pos
            if abs(cur_col - dest_pos[1]) != 2:
                return False

            if abs(cur_row - dest_pos[0]) != 2:
                return False

            if self._board.crosses_river(self._pos, dest_pos):
                return False

            return True

        return False

    def is_unobstructed(self, dest_pos: tuple, **kwargs):
        if super().is_unobstructed(dest_pos):
            cur_row, cur_col = self._pos

            block_row = (cur_row + dest_pos[0]) // 2
            block_col = (cur_col + dest_pos[1]) // 2

            piece = self.get_piece_at_pos((block_row, block_col))
            if piece is not None:
                return False

            return True

        return False

    def has_no_moves(self):
        for r in range(-2, 3, 4):
            for c in range(-2, 3, 4):
                row, col = self.get_pos()

                row += r
                col += c

                if self.can_move((row, col)):
                    return False

        return True


class Horse(Piece):
    def __init__(self, board, color: str, pos: str, gen: Piece):
        super().__init__(board, HORSE, color, pos, gen)

    def is_valid_pos(self, dest_pos: tuple):
        if super().is_valid_pos(dest_pos):
            start_row, start_col = self._pos
            end_row, end_col = dest_pos

            if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1:
                return True
            elif abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
                return True

        return False

    def is_unobstructed(self, dest_pos: tuple, **kwargs):
        if super().is_unobstructed(dest_pos):
            blocking_pos = self.find_blocking_pos(dest_pos)

            piece = self.get_piece_at_pos(blocking_pos)

            if piece is None:
                return True

        return False

    def find_blocking_pos(self, pos: tuple = None, direction: str = None):
        row, col = self.get_pos()

        if abs(row - pos[0]) == 2:
            return (row + pos[0]) // 2, col
        else:
            return row, (col + pos[1]) // 2

class Soldier(Piece):
    def __init__(self, board, color, pos, gen):
        super().__init__(board, SOLDIER, color, pos, gen)
        self._crossed_river = False

        if color == RED:
            self._row_shift = 1
        else:
            self._row_shift = -1

    def is_valid_pos(self, dest_pos):
        start_row, start_col = self._pos
        end_row, end_col = dest_pos

        if super().is_valid_pos(dest_pos):
            if not self._crossed_river:
                if start_row == end_row or start_col != end_col:
                    return False

                if start_row + self._row_shift != end_row:
                    return False
            else:
                if start_row != end_row and end_row != self._row_shift + start_row:
                    return False

            return True

    def move_piece(self, dest):
        cur_pos = self._pos
        if super().move_piece(dest):
            if self._board.crosses_river(cur_pos, self._pos):
                self._crossed_river = True

            return True

        return False

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

                if self._general.can_move(pos) and not self.is_in_check(pos):
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

        blocking_pos, screen = self._general.get_blocking_pos()

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
