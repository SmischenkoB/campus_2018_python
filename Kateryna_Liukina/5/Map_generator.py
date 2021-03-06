from random import choice
from math import floor


def generate_map(map_size, percent_of_traps, percent_of_treasures):
    """
    Function generate map for dungeon game
    Args:
        map_size(list(int)): map size
        percent_of_traps(float): percent of traps
        percent_of_treasures(float): percent of treasures
    Returns:
        list(list(int))
    """
    game_map = [[0] * map_size[0] for i in range(map_size[0])]

    number_of_traps = max(1, floor(map_size[0] * map_size[1] * percent_of_traps))
    number_of_treasures = max(1, floor(map_size[0] * map_size[1] * percent_of_treasures))

    generate_specific_item(game_map, number_of_traps, 1)
    generate_specific_item(game_map, number_of_treasures, 2)

    return game_map


def generate_specific_item(game_map, number_of_item, game_item):
    """
    Function generate number_of_item game_item on game_map
    Args:
        game_map(list(list(int))): game map
        number_of_item(int): number of item
        game_item(int): 1 - trap, 2 - treasure
    Returns:
        none
    """
    for i in range(number_of_item):

        coor = generate_coordinates(game_map)

        game_map[coor[0]][coor[1]] = game_item


def generate_coordinates(game_map):
    """
    Function generate coordinates without traps and treasure on game_map
    Args:
        game_map(list(list(int))): game map
    Returns:
        list(int)
    """
    row = choice(range(len(game_map)))
    column = choice(range(len(game_map[0])))

    while game_map[row][column] != 0:
        row = choice(range(len(game_map)))
        column = choice(range(len(game_map[0])))

    return [row, column]

