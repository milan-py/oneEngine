from enum import Enum


class CardTypes(Enum):
    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2
    NUMBER_3 = 3
    NUMBER_4 = 4
    NUMBER_5 = 5
    NUMBER_6 = 6
    NUMBER_7 = 7
    NUMBER_8 = 8
    NUMBER_9 = 9
    BLOCK = 10
    ROTATE = 11
    ADD2 = 12
    COLOR_SELECT = 13
    ADD4 = 14


class Colors(Enum):
    BLUE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3
    BLACK = 4


class Directions(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1
