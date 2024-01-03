from enum import Enum
import random

SAMPLES = 1
BOARD_SIZE = 10
MAX_COORD = BOARD_SIZE - 1
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
    if generate_wood(board) is False:
        print("Failed at generating wood. Trying again...")
        generate()
    print_board(board)


def generate_wood(board):
    n_wood_remaining = N_WOOD
    while n_wood_remaining > 0:
        tile_size = random_tile_size(n_wood_remaining)
        n_wood_remaining -= tile_size
        valid_spots = valid_places(board, (1, tile_size))
        valid_spots = [spot for spot in valid_spots if not area_touches_type(board, spot, Type.WOOD)]
        edge_spots, inner_spots = filter_edge_groups(valid_spots)

        want_to_be_edge = False
        if edge_spots and inner_spots:
            want_to_be_edge = fractional_chance(3, 4)
        if want_to_be_edge or not inner_spots or (not want_to_be_edge and not inner_spots):
            group = random.choice(edge_spots)
        else:
            group = random.choice(inner_spots)

        set_area(board, group, Type.WOOD)


def area_touches_type(board, tl_br_points, tile_type):
    all_coords = get_coords_tlbr(*tl_br_points)
    all_neighbors = unique_neighbors_of_group(all_coords)
    return any([get_tile(board, n) == tile_type for n in all_neighbors])


def unique_neighbors_of_group(list_of_coords):
    neighbors_per_coord = [get_neighbors(c) for c in list_of_coords]
    return list(set([n for neighbors in neighbors_per_coord for n in neighbors if n not in list_of_coords]))


# group = [( (1,2), (3,4) ), ...]
def filter_edge_groups(groups):
    edges = [g for g in groups if 0 in g[0]]
    non_edges = [g for g in groups if g not in edges]
    return edges, non_edges


def is_edge_group(group):
    return any([0 in coord or MAX_COORD in coord for coord in group])


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
                valid.append(((i, j), (i + group_width - 1, j + group_height - 1)))
            if is_valid_place(board, i, j, group_height, group_width):
                valid.append(((i, j), (i + group_height - 1, j + group_width - 1)))
    return valid


def is_valid_place(board, i, j, w, h):
    if i + w - 1 > MAX_COORD or j + h - 1 > MAX_COORD:
        return False
    cells = get_cells_in_area(board, i, j, w, h)
    return all([c is None for c in cells])


def get_cells_in_area(board, i, j, w, h):
    window = []
    for row in range(i, i + w):
        window_row = board[row][j:j + h]
        window.extend(window_row)
    return window


def get_coords_in_block(i, j, w, h):
    coords = []
    for x in range(i, i + w):
        for y in range(j, j + h):
            coords.append((x, y))
    return coords


def get_coords_tlbr(tl, br):
    return [(i, j) for i in irange(tl[0], br[0]) for j in irange(tl[1], br[1])]


def fractional_chance(i, j):
    random_number = random.random()
    return random_number <= i / j


def random_tile_size(n_wood_remaining):
    if n_wood_remaining <= 2:
        return random.choice(irange(1, n_wood_remaining))
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
    assert get_tile(board, coord) is None
    board[coord[0]][coord[1]] = tile_type


def set_all_tiles(board, coord_list, tile_type):
    for c in coord_list:
        set_tile(board, c, tile_type)


def set_area(board, tl_br_coords, tile_type):
    coords = get_coords_tlbr(*tl_br_coords)
    set_all_tiles(board, coords, tile_type)


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
    if coord[0] != MAX_COORD:
        neighbors.append((coord[0] + 1, coord[1]))
    if coord[1] != 0:
        neighbors.append((coord[0], coord[1] - 1))
    if coord[1] != MAX_COORD:
        neighbors.append((coord[0], coord[1] + 1))
    return neighbors


def get_empty_edges(board):
    open_coords = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if ((i == 0 or i == MAX_COORD
                 or j == 0 or j == MAX_COORD)
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
    return cell


def irange(start, stop):
    return range(start, stop + 1)


def main():
    for i in range(SAMPLES):
        generate()


if __name__ == '__main__':
    main()
