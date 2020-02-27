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
