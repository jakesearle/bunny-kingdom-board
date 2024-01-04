import copy
import random

from cell_logic import get_empty_edges, is_adjacent_to, set_tile, get_all_empty_neighbors, get_neighbors, get_tile, \
    valid_places, filter_edge_groups, area_touches_type, set_area, get_coords_tlbr, unique_neighbors_of_group, \
    get_cluster, has_any
from const import BOARD_SIZE, FISH_GROUP_SIZES, N_WOOD, N_MOUNTAINS, N_CARROTS, N_CITIES
from space_types import Type
from util import print_board, fractional_chance, irange


def generate():
    board = [[None for _1 in range(BOARD_SIZE)] for _2 in range(BOARD_SIZE)]
    if generate_fish(board) is False:
        print("Failed at generating fish. Trying again...")
        generate()
    if generate_wood(board) is False:
        print("Failed at generating wood. Trying again...")
        generate()
    if generate_mountains(board) is False:
        print("Failed at generating mountains. Trying again...")
        generate()
    if generate_carrots(board) is False:
        print("Failed at generating carrots. Trying again...")
        generate()
    if generate_cities(board) is False:
        print("Failed at generating carrots. Trying again...")
        generate()
    fill_blanks(board)
    print_board(board)


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
    return True


def generate_wood(board):
    n_wood_remaining = N_WOOD
    while n_wood_remaining > 0:
        tile_size = random_wood_tile_size(n_wood_remaining)
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
    return True


def generate_mountains(board):
    # Generate 1x2 tiles until finished
    tiles_to_generate = N_MOUNTAINS
    while tiles_to_generate > 0:
        tiles_to_generate -= 2
        all_places = valid_places(board, (1, 2))
        mountain_touchers = filter_touches_valid_mountains(board, all_places)
        isolated_mountains = filter_isolated_mountains(board, all_places)
        if mountain_touchers and isolated_mountains:
            if fractional_chance(3, 4):
                group = random.choice(mountain_touchers)
            else:
                group = random.choice(isolated_mountains)
        elif mountain_touchers:
            group = random.choice(mountain_touchers)
        else:
            group = random.choice(isolated_mountains)
        set_area(board, group, Type.MOUNTAIN)
    return True


def generate_carrots(board):
    n_remaining = N_CARROTS
    while n_remaining > 0:
        tile_size = random_carrot_tile_size(n_remaining)
        n_remaining -= tile_size
        valid_spots = valid_places(board, (1, tile_size))
        valid_spots = [spot for spot in valid_spots if not area_touches_type(board, spot, Type.CARROT)]
        edge_spots, inner_spots = filter_edge_groups(valid_spots)

        if edge_spots and inner_spots:
            want_to_be_inner = fractional_chance(7, 8)
            if want_to_be_inner:
                group = random.choice(inner_spots)
            else:
                group = random.choice(edge_spots)
        elif edge_spots:
            group = random.choice(edge_spots)
        elif inner_spots:
            group = random.choice(inner_spots)
        else:
            return False
        set_area(board, group, Type.CARROT)
    return True


def generate_cities(board):
    for _ in range(N_CITIES):
        all_spots = valid_places(board, (1, 1))
        valid_spots = [s for s in all_spots if not area_touches_type(board, s, Type.CITY)]
        assert len(valid_spots) <= len(all_spots)
        group = random.choice(valid_spots)
        set_area(board, group, Type.CITY)
    return True


def fill_blanks(board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                board[i][j] = Type.FIELD


def random_wood_tile_size(n_wood_remaining):
    if n_wood_remaining <= 2:
        return random.choice(irange(1, n_wood_remaining))
    else:
        return random.choice(range(1, 4))


def random_carrot_tile_size(n_carrots_remaining):
    if n_carrots_remaining == 1:
        return 1
    return random.choice(irange(1, 2))


def filter_touches_valid_mountains(board, places):
    if not has_any(board, Type.MOUNTAIN):
        return []
    return [p for p in places if touches_valid_mountains(board, p)]


def touches_valid_mountains(board, place):
    all_cells = get_coords_tlbr(*place)
    # Get all neighbors
    neighbors = unique_neighbors_of_group(all_cells)
    # Get all mountain neighbors
    m_neighbors = [n for n in neighbors if get_tile(board, n) == Type.MOUNTAIN]
    # if none, return false
    if not m_neighbors:
        return False
    if makes_a_big_mountain_cluster(board, place):
        return False
    return True


def filter_isolated_mountains(board, places):
    if not has_any(board, Type.MOUNTAIN):
        return places
    return [p for p in places if not area_touches_type(board, p, Type.MOUNTAIN)]


def makes_a_big_mountain_cluster(board, place):
    test_board = copy.deepcopy(board)
    set_area(test_board, place, Type.MOUNTAIN)
    for i, row in enumerate(test_board):
        for j, cell in enumerate(row):
            if cell is None or cell != Type.MOUNTAIN:
                continue
            cluster = get_cluster(test_board, (i, j))
            if len(cluster) > 4:
                return True
    return False
