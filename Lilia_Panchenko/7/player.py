from logger import debug_decorator
from logger import info_decorator
from random import choice


class Player:

    def __init__(self):

        self.bag = 0
        self.hp = 3
        self.islost = False
        self.iswon = False


    def set_player_name(self, name):
        self.name = name

    @debug_decorator
    @info_decorator
    def pick_treasure(self):

        self.bag += 1
        if self.bag >= 3:
            self.iswon = True


    @debug_decorator
    @info_decorator
    def pick_trap(self):

        self.hp -= 1
        if self.hp <= 0:
            self.islost = True


    @debug_decorator
    @info_decorator
    def input_direction(self):

        player_choice = input('Where do you want to move:\n')
        player_choice.casefold()

        available_choices = ['up', 'down', 'left', 'right', 'save', 'exit']
        while not player_choice in available_choices:
            player_choice = input("I'm sorry, I don't understand your choice.\nTry once more:\n")
            player_choice.casefold()

        return player_choice


    @debug_decorator
    @info_decorator
    def spawn_player(self, game_map):

        self.position = choice(range(game_map.mapsize * game_map.mapsize))

        row, col = self.position // game_map.mapsize, self.position % game_map.mapsize

        while game_map.game_map[row][col] == -1 or game_map.game_map[row][col] == 1:

            self.position = choice(range(game_map.mapsize * game_map.mapsize))
            row, col = self.position // game_map.mapsize, self.position % game_map.mapsize

        self.position = []
        self.position.append(row)
        self.position.append(col)
