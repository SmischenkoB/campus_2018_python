import dungeon_logger
import dungeon_decorators
import dun_player
import dun_map
import dungeon_serializer
import dungeon_exception


class Game:

    def __init__(self):

        self.player = dun_player.Player()
        self.dun_map = dun_map.DungeonMap(5)

        dungeon_logger.logger.info('Default map size = 3\n')
        command = input("Press 'Y' to change map size\n")
        command.lower()
        if command == 'y':

            self.set_map_size()
        

    def set_map_size(self):
        """
        :description: created new map with user size
        """
        size = ""
        while size.isdigit() == False:

            size = input("Enter new map size\n")

        try:
            size = int(size)
        except ValueError as error:
            dungeon_logger.logger(f'ValueError: {error}')
        self.dun_map = dun_map.DungeonMap(size)


    def init_game(self):
        """
        :description: initialize required data for game
        """

        self.dun_map.set_player_on_map(self.player)


    def run_game(self):
        """
        :description: run game frame
        """

        while self.player.hit_points > 0 and self.player.treasure_picked < 3:

            self.player.get_command()

            if self.player.command in dun_map.COMMANDS:

                try:
                    self.dun_map.process_move(self.player)
                except (dungeon_exception.CommandError, dungeon_exception.MapCageError) as error:
                    dungeon_logger.logger.info(f'Invalid Player command: {error}')
                
                self.dun_map.print_map()

            elif self.player.command in dun_player.MENU_COMMANDS:

                if self.player.command == 'save':

                    game = Game()
                    game.player = self.player
                    game.dun_map = self.dun_map
                    dungeon_serializer.serialize_dungeon_game(game)
                else:
                    
                    game = dungeon_serializer.deserialize_dungeon_game()
                    self.player = game.player
                    self.dun_game = game.dun_map

        if self.player.hit_points == 0:
            dungeon_logger.logger.info('You LOST')
        elif self.player.treasure_picked == 3:
            dungeon_logger.logger.info('You WON')


game = Game()
game.init_game()
game.run_game()
