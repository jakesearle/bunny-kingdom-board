import random

from space_types import Type


def irange(start, stop):
    return range(start, stop + 1)


def cell_string(cell):
    if cell is None:
        return "❌"
    elif cell == Type.FISH:
        return "🐟"
    elif cell == Type.WOOD:
        return "🌳"
    elif cell == Type.CARROT:
        return "🥕"
    elif cell == Type.MOUNTAIN:
        return "🗻"
    elif cell == Type.CITY:
        return "🏙️"
    elif cell == Type.FIELD:
        return "⬜️️"
    return cell


def print_board(board):
    string = "ij 0   1  2  3  4   5  6  7  8   9\n"
    for i, row in enumerate(board):
        string += f"{i}  "
        for cell in row:
            string += cell_string(cell) + " "
        string += "\n"
    print(string)
    return string


def fractional_chance(i, j):
    random_number = random.random()
    return random_number <= i / j
