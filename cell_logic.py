from const import MAX_COORD
from util import irange


def has_any(board, tile_type):
    return any([cell == tile_type for row in board for cell in row])


def area_touches_type(board, tl_br_points, tile_type):
    all_coords = get_coords_tlbr(*tl_br_points)
    all_neighbors = unique_neighbors_of_group(all_coords)
    return any([get_tile(board, n) == tile_type for n in all_neighbors])


def unique_neighbors_of_group(list_of_coords):
    neighbors_per_coord = [get_neighbors(c) for c in list_of_coords]
    return list(set([n for neighbors in neighbors_per_coord for n in neighbors if n not in list_of_coords]))


def filter_edge_groups(groups):
    edges = [g for g in groups if 0 in g[0]]
    non_edges = [g for g in groups if g not in edges]
    return edges, non_edges


def is_edge_group(group):
    return any([0 in coord or MAX_COORD in coord for coord in group])


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


def get_cluster(board, coord):
    curr_type = get_tile(board, coord)
    checked = {coord}
    cluster = {coord}
    neighbors = get_neighbors(coord)
    while neighbors:
        curr_coord = neighbors.pop()
        checked.add(curr_coord)
        if get_tile(board, curr_coord) != curr_type:
            continue

        cluster.add(curr_coord)
        new_neighbors = [n for n in get_neighbors(curr_coord) if n not in checked]
        neighbors.extend(new_neighbors)
    return cluster
