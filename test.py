import pygame

class game(object):
    def __init__(self):
        # -------#
        # PYGAME #
        # -------#
        # Game window
        self.screen_width = 600
        self.screen_height = 400

        pg.init()
        try:
            pg.mixer.init()
        except:
            print("No sound.")
            self.sound = False

        # Set up the screen for rendering.
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height), 0, 32)

        self.background = pg.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250,250,250))

        # Set up text rendering.
        self.font = pg.font.Font(None, 36)

if __name__ == '__main__':
    print("Welcome to Anagrams")

    # Create the game object.
    game = game()

    """
    while True:
        quit = False
        game.printstatus()
        while True:
            key = input("Enter a word or press \'Return\' to flip:\n")
            if key == '':
                game.flip()
                break
            elif key == 'quit':
                quit = True
                break
            else:
                game.take(key.upper())

        if quit:
            print("Quitting game...")
            break
    """
