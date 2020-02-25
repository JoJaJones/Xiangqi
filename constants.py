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