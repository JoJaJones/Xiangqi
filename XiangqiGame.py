from Board import Board
from Player import Player
from constants import *

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
            return False

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
            print(" Invalid!")
            return False

    def print_board(self):
        print_dict = {SOLDIER:"S", CHARIOT: "T", ADVISOR: "A", CANNON: "C", ELEPHANT: "E", GENERAL: "G", HORSE: "H", None: " "}
        color_dict = {RED: "\033[91m", BLACK: "\033[35m", None: "\033[97m"}
        board_table = self._board.get_positions()
        for row in range(-1, len(board_table)):
            if row == -1:
                print("    ", end="")
                for col in range(len(board_table[0])):
                    print(" {} ".format("abcdefghi"[col]), end="")
            else:
                print(f" {row+1:2d} ", end="")
                for col in range(len(board_table[row])):
                    piece = self._board.get_pos((row,col))
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
        # input()