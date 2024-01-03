from enum import Enum
import random

BOARD_SIZE = 10
FISH_GROUP_SIZES = [7, 4, 2, 2]
N_WOOD = 15


class Type(Enum):
    FISH = 1
    WOOD = 2
    CARROT = 3
    MOUNTAIN = 4
    CITY = 5
    FIELD = 6


def generate():
    board = [[None for _1 in range(BOARD_SIZE)] for _2 in range(BOARD_SIZE)]
    if generate_fish(board) is False:
        print("Failed at generating fish. Trying again...")
        generate()
    # TODO:
    # if generate_wood(board) is False:
    #     print("Failed at generating wood. Trying again...")
    #     generate()


def generate_wood(board):
    n_wood_remaining = N_WOOD
    while n_wood_remaining > 0:
        # tile_size = random_tile_size(n_wood_remaining)
        tile_size = 3
        print(tile_size)
        n_wood_remaining -= tile_size
        valid = valid_places(board, (1, tile_size))
        is_edge_wood = fractional_chance(3, 4)


# group = [( (1,2), (3,4) ), ...]
def filter_edge_groups(groups):
    return [g for g in groups if 0 in g[0]]


# group_size = (4, 5)
def valid_places(board, group_size):
    group_width, group_height = group_size
    valid = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is not None:
                continue
            # Rotatable
            if is_valid_place(board, i, j, group_width, group_height):
                valid.append(((i, j), (i + group_width, j + group_height)))
            if is_valid_place(board, i, j, group_height, group_width):
                valid.append(((i, j), (i + group_height, j + group_width)))
    return valid


def is_valid_place(board, i, j, w, h):
    if i + w > len(board) or j + h > len(board[0]):
        return False
    cells = get_cells_in_area(board, i, j, w, h)
    return all([c is None for c in cells])


def get_cells_in_area(board, i, j, w, h):
    window = []
    for row in range(i, i + w):
        window_row = board[row][j:j + h]
        window.extend(window_row)
    return window


def get_coords_in_area(i, j, w, h):
    coords = []
    for x in range(i, i + w):
        for y in range(j, j + h):
            coords.append((x, y))
    return coords


def fractional_chance(i, j):
    random_number = random.random()
    return random_number <= i / j


def random_tile_size(n_wood_remaining):
    if n_wood_remaining <= 2:
        return random.choice(range(1, n_wood_remaining + 1))
    else:
        return random.choice(range(1, 4))


def generate_fish(board):
    for group_size in FISH_GROUP_SIZES:
        current_group = []
        for tiles in range(group_size):
            if not current_group:
                empty_edges = get_empty_edges(board)
                valid_edges = [cell for cell in empty_edges if not is_adjacent_to(board, cell, Type.FISH)]
                if not valid_edges:
                    return False
                random_edge = random.choice(valid_edges)
                set_tile(board, random_edge, Type.FISH)
                current_group.append(random_edge)
                continue
            empty_neighbors = get_all_empty_neighbors(board, current_group)
            okay_neighbors = []
            for test_space in empty_neighbors:
                is_okay = True
                for test_neighbor in get_neighbors(test_space):
                    if test_neighbor not in current_group and get_tile(board, test_neighbor) == Type.FISH:
                        is_okay = False
                        break
                if is_okay:
                    okay_neighbors.append(test_space)
            if not okay_neighbors:
                return False
            new_neighbor = random.choice(okay_neighbors)
            set_tile(board, new_neighbor, Type.FISH)
            current_group.append(new_neighbor)
    print_board(board)
    return True


def is_adjacent_to(board, coord, adjacent_type):
    for neighbor in get_neighbors(coord):
        if get_tile(board, neighbor) == adjacent_type:
            return True
    return False


def set_tile(board, coord, tile_type):
    board[coord[0]][coord[1]] = tile_type


def set_all_tiles(board, coord_list, tile_type):
    for c in coord_list:
        set_tile(board, c, tile_type)


def get_tile(board, coord):
    return board[coord[0]][coord[1]]


def get_all_empty_neighbors(board, coords):
    empty_coords = set()
    for c in coords:
        n = get_empty_neighbors(board, c)
        empty_coords = empty_coords.union(set(n))
    return list(empty_coords)


def get_empty_neighbors(board, coord):
    neighbor_coords = get_neighbors(coord)
    return [n for n in neighbor_coords if board[n[0]][n[1]] is None]


def get_neighbors(coord):
    neighbors = []
    if coord[0] != 0:
        neighbors.append((coord[0] - 1, coord[1]))
    if coord[0] != BOARD_SIZE - 1:
        neighbors.append((coord[0] + 1, coord[1]))
    if coord[1] != 0:
        neighbors.append((coord[0], coord[1] - 1))
    if coord[1] != BOARD_SIZE - 1:
        neighbors.append((coord[0], coord[1] + 1))
    return neighbors


def get_empty_edges(board):
    open_coords = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if ((i == 0 or i == BOARD_SIZE - 1
                 or j == 0 or j == BOARD_SIZE - 1)
                    and cell is None):
                open_coords.append((i, j))
    return open_coords


def print_board(board):
    string = ""
    for row in board:
        for cell in row:
            string += cell_string(cell) + " "
        string += "\n"
    print(string)
    return string


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
        return "🏜️"
    print(cell)


def main():
    generate()


if __name__ == '__main__':
    main()
