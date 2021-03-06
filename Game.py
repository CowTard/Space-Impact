from Classes.Characters.Player import *
from Classes.Characters.Enemy import *
from Classes.Levels.Camera import Camera
from Classes.Levels.Level import Level
from Config.ConfigParser import ConfigParser
from Explosions import *


class Game:
    """
    Class responsible for managing the game itself and Pygame objects
    """

    def __init__(self):
        """
        Constructor of the class. Reads and parses configuration files as well as initiates game objects
        """

        # Read configuration file
        self.config = ConfigParser('./Config/config.ini')

        # Create Pygame related objects
        pygame.init()
        pygame.key.set_repeat(10, 10)
        self.screen = pygame.display.set_mode((self.config.game_config.width, self.config.game_config.height),
                                              pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.config.game_config.title)

        # Create Sprite containers
        self.enemies_sprites = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group
        self.background_sprites = pygame.sprite.Group()

        # Camera
        self.camera = Camera(self.config.game_config.width, self.config.game_config.height)

        # Create Player object
        self.player = Player((0, 0), 100)

        # Load initial level
        self.load_level(1)

    def load_level(self, level=1):
        """
        Function responsible for loading a specific level passed as argument.
        :param level: Desired level or 1 by default
        """

        level_loaded = Level(level)

        # Load background(s)
        self.background_sprites.add(level_loaded.backgrounds)

        # calculating size of level
        y_axis_length = len(level_loaded.get_map())
        x_axis_length = len(level_loaded.get_map()[0])

        for y in range(y_axis_length):
            for x in range(x_axis_length):
                if level_loaded.get_map()[y][x] == '.':
                    pass
                elif level_loaded.get_map()[y][x] == 'A':
                    self.enemies_sprites.add(Enemy((x * 64, y * 64), 100))


    def game_loop(self):
        """
        Function that handles everything in the game
        :return: void
        """

        while True:

            # Handling inputs
            movm = (0, 0)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    movm = self.input_handle(event)
                elif event.type == pygame.QUIT:
                    pygame.quit()

            delta = self.clock.tick(60) / 1000

            if self.player.retrieve_health_information() <= 0:
                break

            # Update enemies and player's location
            self.enemies_sprites.update(delta)
            self.player.update_with_constrains(movm, (self.config.game_config.width, self.config.game_config.height))

            backMov = ( (movm[0] + 1) * -1, 0)

            # Update and draw Background
            self.background_sprites.update(backMov)
            self.background_sprites.draw(self.screen)

            # Draw Enemies and Player
            self.enemies_sprites.update(backMov)
            self.enemies_sprites.draw(self.screen)

            self.screen.blit(self.player.image, self.player)

            pygame.display.flip()

        pygame.quit()

    @staticmethod
    def input_handle(event):
        """
        Function responsible for handling the input
        :return: Tuple
        """

        if event.key is pygame.K_w or event.key is pygame.K_UP:
            return 0, -1
        elif event.key is pygame.K_s or event.key is pygame.K_DOWN:
            return 0, 1
        elif event.key is pygame.K_a or event.key is pygame.K_LEFT:
            return -1, 0
        elif event.key is pygame.K_d or event.key is pygame.K_RIGHT:
            return 1, 0
        else:
            return 0, 0



