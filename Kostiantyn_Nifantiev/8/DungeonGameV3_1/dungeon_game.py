import pickle
from dungeon_logger import my_logger
from dungeon_logger import log_decorator
from game_map import DungeonMap
from game_map import PlayerMap
from character import Player


class Game:
    """
    Main game class
    Contains other game classes: dungeon map, player map, player itself
    """
    def __init__(self):

        self.dungeon_map = DungeonMap()
        self.player_map = PlayerMap()
        self.player = Player()


    @log_decorator
    def setup_new_game(self):
        """
        This function is used to generate new map of size, specified by user
        """
        while True:

            map_request = input('Enter preferable map size in format "width:height", or just press enter to play with default map:\n')
            my_logger.info("Generating map...")

            if not len(map_request):

                map_size = [20, 10]
                break

            else:

                try:

                    map_size = [int(token) for token in map_request.split(':')]
                    break

                except ValueError as val_error:

                    my_logger.exception(val_error)
                    my_logger.error("Try to enter map size once again!")

        self.dungeon_map.set_map_size(*map_size)
        self.dungeon_map.generate_map()
        my_logger.info("Map has been generated successfully!")

        self.player_map.set_map_size(*map_size)
        self.player_map.init_map()

        self.player.reset()
        self.player.randomize_initial_position(self.dungeon_map)


    @log_decorator
    def setup_game(self):
        """
        Game startup method: user should choose between playing new game or loading save
        """
        my_logger.debug("Game start choice")
        start_game_choice = input('Enter "y" if you want to play a new game or\n"load" if you want to load existing game:\n')
        my_logger.debug("Game start choice handling")

        if start_game_choice == "load":

            try:

                self.load_game()

            except (FileNotFoundError, pickle.UnpicklingError) as file_error:

                my_logger.exception(file_error)
                
                if isinstance(file_error, FileNotFoundError):

                    my_logger.error("There is no dungeon.sav file! Start a new game instead!")

                elif isinstance(file_error, pickle.UnpicklingError):

                    my_logger.error("dungeon.sav file is corrupted! Start a new game instead!")

                self.setup_new_game()

        else:

            self.setup_new_game()

        self.player_map.update_map(self.dungeon_map, self.player.player_x, self.player.player_y)
        self.player_map.draw_map()


    @log_decorator
    def load_game(self):
        """
        Game load (pickle!)
        """
        my_logger.info("Loading game...")
        in_file = open('dungeon.sav', 'rb')
        
        data = pickle.load(in_file)

        [self.dungeon_map.dungeon_map, 
        self.dungeon_map.map_size, 
        self.player_map.dungeon_map, 
        self.player.player_x,
        self.player.player_y,
        self.player.health,
        self.player.treasures] = data
        my_logger.info("Game has been loaded!")


    @log_decorator
    def save_game(self):
        """
        Game save (pickle!)
        """
        data = [self.dungeon_map.dungeon_map, 
                self.dungeon_map.map_size, 
                self.player_map.dungeon_map, 
                self.player.player_x,
                self.player.player_y,
                self.player.health,
                self.player.treasures]

        try:

            out_file = open('dungeon.sav', 'wb')

        except PermissionError as premission_error:

            my_logger.exception(premission_error)
            my_logger.error("Unable to save game! So sorry! But you can play again!")

        pickle.dump(data, out_file)


    @log_decorator
    def run_farame(self):
        """
        Game frame. Returns true if game could be resumed and false otherwise
        """
        ret_value = True
        move = input('\nEnter your move, please (w - up, d - right, s - down, a - left), or "save" for save game:\n')

        if move == "save":

            self.save_game()
            ret_value = False

        self.player.make_move(move, *self.dungeon_map.map_size)

        self.player_map.update_map(self.dungeon_map, self.player.player_x, self.player.player_y)
        self.player_map.draw_map()


        if self.dungeon_map.get_cell_content(self.player.player_x, self.player.player_y) == 'T':

            self.dungeon_map.set_cell_content(self.player.player_x, self.player.player_y, '-')
            self.player.add_treasure()

        elif self.dungeon_map.get_cell_content(self.player.player_x, self.player.player_y) == 'X':

            self.dungeon_map.set_cell_content(self.player.player_x, self.player.player_y, '-')
            self.player.apply_damage()

        self.player.draw_character()
     
        if self.player.is_dead():

            my_logger.info("\n}}}This is a trap! You loose!{{{\n")
            ret_value = False

        elif self.player.is_winner():

            my_logger.info("\n>>>This is a treasure! You are victorious!<<<\n")
            ret_value = False

        return ret_value
