import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVYBLUE = (60, 60, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (230, 230, 230)

BGCOLOR = WHITE
TEXTCOLOR = BLACK

# Original was 640 x 640

WINDOWWIDTH = 1400
WINDOWHEIGHT = 800



DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

class Graphics:
    def __init__(self):
        #  ________
        # | LAYOUT |
        #  --------

        self.first_time = True

        self.gap_factor = 1.5


        # 'Current'
        self.current = {'font': 'freesansbold.ttf',
                        'size': 32,
                        'color': BLACK,
                        'x': 10,
                        'y': 20}

        # Ready Flip
        self.flip = {'font': 'freesansbold.ttf',
                     'size': 20,
                     'color': BLACK,
                     'x': 20,
                     'y': 60}

        # Tiles
        self.tile = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x_0': 150,
                     'y_0': 38,
                     'x_gap': 30,
                     'y_gap': 50}

        # 'Your Words'
        self.your = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x': 10,
                     'y': 100,
                     'y_gap': 70}

        # Your Words
        self.self_words = {'font': 'freesansbold.ttf',
                     'size': 48,
                     'color': BLACK,
                     'x': 30,
                     'y': self.your['y'] + self.your['y_gap'],
                     'x_gap': 150,
                     'y_gap': 50}

        # 'Opponent's Words'
        self.opp = {'font': 'freesansbold.ttf',
                    'size': 32,
                    'color': BLACK,
                    'x': WINDOWWIDTH / 2 + 10,
                    'y': 100,
                    'y_gap': 70}


        # Opponent's Words
        self.opp_words = {'font': 'freesansbold.ttf',
                          'size': 48,
                          'color': BLACK,
                          'x': WINDOWWIDTH / 2 + 30,
                          'y': self.opp['y'] + self.opp['y_gap'],
                          'x_gap': 150,
                          'y_gap': 50}

        self.color_taken = BLUE

        # Guess
        self.guess = {'font': 'freesansbold.ttf',
                      'size': 32,
                      'color': BLACK,
                      'x': 10,
                      'y': WINDOWHEIGHT - 140}

        # Status
        self.status = {'font': 'freesansbold.ttf',
                       'size': 20,
                       'color': BLACK,
                       'x': 10,
                       'y': WINDOWHEIGHT - 100}

        self.fontObjs = {'current': pygame.font.Font(self.current['font'], self.current['size']),
                         'tile': pygame.font.Font(self.tile['font'], self.tile['size']),
                         'your': pygame.font.Font(self.your['font'], self.your['size']),
                         'self_words': pygame.font.Font(self.self_words['font'], self.self_words['size']),
                         'guess': pygame.font.Font(self.guess['font'], self.guess['size']),
                         'status': pygame.font.Font(self.status['font'], self.status['size']),
                         'flip': pygame.font.Font(self.flip['font'], self.flip['size']),
                         'opp': pygame.font.Font(self.your['font'], self.your['size']),
                         'opp_words': pygame.font.Font(self.self_words['font'], self.self_words['size']),
                         }

        self.SurfObjs = {'current': self.fontObjs['current'].render('Current: ', True, self.current['color']),
                         'tiles_list': [],
                         'your': self.fontObjs['your'].render('Your Words: ', True, self.your['color']),
                         'self_words_list': [],
                         'opp': self.fontObjs['opp'].render('Opponent\'s Words: ', True, self.opp['color']),
                         'opp_words_list': [],
                         'guess': self.fontObjs['guess'].render('Take: ', True, self.guess['color']),
                         'status': self.fontObjs['status'].render('', True, self.status['color']),
                         'flip': self.fontObjs['flip'].render('', True, self.flip['color'])
                         }

        # Load tile images
        self.tile_dict = {}

        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            self.tile_dict[letter] = pygame.image.load(letter + '.png')

        self.word_space_y = self.guess['y'] - self.your['y']
        self.word_space_x = WINDOWWIDTH / 2

        self.words_per_column = int(self.word_space_y / (self.self_words['size'] * self.gap_factor))

    def flatten(self, list):
        flat_list = []
        for sublist in list:
            for item in sublist:
                flat_list.append(item)
        return flat_list

    def __numwords_to_fontsize(self, numwords):
        if numwords <= self.words_per_column * 2:
            return int(self.self_words['size']), int(self.self_words['y_gap'] / 1.25)
        else:
            return int(self.self_words['size']/2), int(self.self_words['y_gap'] / 2)
            """
            elif 6 < numwords <= 10:
                return int(self.self_words['size'] / 3), int(self.self_words['y_gap'] / 3)
            elif 10 < numwords <= 20:
                return int(self.self_words['size'] / 5), int(self.self_words['y_gap'] / 5)
            elif 20 < numwords <= 50:
                return int(self.self_words['size'] / 8), int(self.self_words['y_gap'] / 8)
            """

    def __numtiles_to_fontsize(self, numtiles):
        if numtiles <= 20:
            return self.tile['size'], self.tile['y_gap'], self.tile['x_gap']
        elif 10 < numtiles <= 40:
            return int(self.tile['size'] / 1.5), int(self.tile['y_gap'] / 1.5), int(self.tile['x_gap'] / 1.5)
        elif 40 < numtiles <= 60:
            return int(self.tile['size'] / 2), int(self.tile['y_gap'] / 2), int(self.tile['x_gap'] / 2)
        elif 60 < numtiles <= 144:
            return int(self.tile['size'] / 4), int(self.tile['y_gap'] / 4), int(self.tile['x_gap'] / 4)

    def display_text(self, SurfaceObj, x, y):
        textRectObj = SurfaceObj.get_rect()
        textRectObj.topleft = (x, y)
        DISPLAYSURF.blit(SurfaceObj, textRectObj)
        return textRectObj

    def display_text_tiles(self, SurfaceObj, x, y):
        textRectObj = SurfaceObj.get_rect()
        textRectObj.center = (x, y)
        DISPLAYSURF.blit(SurfaceObj, textRectObj)
        return textRectObj

    def display_tile(self, tile, size, x, y):
        SurfaceObj = pygame.transform.smoothscale(self.tile_dict[tile.lower()], (size, size))
        textRectObj = SurfaceObj.get_rect()
        textRectObj.center = (x, y)
        DISPLAYSURF.blit(SurfaceObj, textRectObj)

        return textRectObj

    def display_word(self, word, size, x, y):
        # Outputs a surface object of the word in tile images
        textRectObj_list = []
        current_x = x

        for letter in word:
            SurfaceObj = pygame.transform.smoothscale(self.tile_dict[letter.lower()], (size, size))
            textRectObj = SurfaceObj.get_rect()
            textRectObj.center = (current_x, y)
            DISPLAYSURF.blit(SurfaceObj, textRectObj)

            textRectObj_list.append(textRectObj)
            current_x += size

        return textRectObj_list

    def printstatus(self, game, player, graphics_to_update, guess, status, taker):

        gap_btwn_cols = 20

        rects_to_update = []

        if player == 0:
            self_words_list = game.player1words_list
            self_words = game.player1words
            opp_words_list = game.player2words_list
            opp_words = game.player2words
        else:
            self_words_list = game.player2words_list
            self_words = game.player2words
            opp_words_list = game.player1words_list
            opp_words = game.player1words

        # Make the surface objects (or lists of surface objects)

        size_tiles, y_gap_tile, x_gap_tile = self.__numtiles_to_fontsize(len(game.current))
        size_words, y_gap_words = self.__numwords_to_fontsize(len(self_words_list))
        size_opp_words, y_gap_opp_words = self.__numwords_to_fontsize(len(opp_words_list))

        if 'flip' in graphics_to_update or 'flip_status' in graphics_to_update:
            print(f"Updating flip status to {game.flip_status}!")
            self.SurfObjs['flip'] = self.fontObjs['flip'].render(game.flip_status, True, self.flip['color'])

        if 'guess' in graphics_to_update:
            self.SurfObjs['guess'] = self.fontObjs['guess'].render('Take: ' + guess, True, self.guess['color'])

        if 'status' in graphics_to_update:
            print(f"UPDATING STATUS: {status}")
            self.SurfObjs['status'] = self.fontObjs['status'].render(status, True, self.status['color'])

        # Display all the surface objects created above

        DISPLAYSURF.fill(BGCOLOR)

        y_tile = self.tile['y_0']
        x_tile = self.tile['x_0']

        rect_tiles = self.display_text(self.SurfObjs['current'], self.current['x'], self.current['y'])

        rect_tiles_list = []

        for i, tile in enumerate(game.current):
            x_tile = x_tile + size_tiles + 5

            rect_tiles_list.append(self.display_tile(tile, size_tiles, x_tile, y_tile))

            if i % 10 == 9:
                y_tile = y_tile + size_tiles + 5
                x_tile = self.tile['x_0']

        _ = self.display_text(self.SurfObjs['your'], self.your['x'], self.your['y'])

        rect_self_list = []

        x_words_local = self.self_words['x']
        y_words_local = self.self_words['y']

        rect_self_list = []

        past_first_column = False
        for i, word in enumerate(self_words_list):

            print(f"Displaying {word}")
            print(f"initial y value: {y_words_local}")

            if y_words_local >= self.guess['y'] - size_words or past_first_column:
                past_first_column = True

                print(f"i {i}")
                print(f"words per columns: {self.words_per_column}")

                adjacent_word_i = int(i - self.words_per_column)
                print(f"adjacent word: {adjacent_word_i}")
                print(f"adjacent word's y: {rect_self_list[adjacent_word_i][-1].center[1]}")
                x_words_local = rect_self_list[adjacent_word_i][-1].right + gap_btwn_cols + size_tiles
                y_words_local = rect_self_list[adjacent_word_i][-1].center[1]

            print(f"after new column y value: {y_words_local}")

            rect_self_list.append(self.display_word(word, size_words, x_words_local, y_words_local))

            y_words_local = y_words_local + size_words * self.gap_factor

            print(f"end of loop y value: {y_words_local}")

        rect_self_list = self.flatten(rect_self_list)

        rect_guess = self.display_text(self.SurfObjs['guess'], self.guess['x'], self.guess['y'])

        _ = self.display_text(self.SurfObjs['opp'], self.opp['x'], self.opp['y'])

        x_opp_words_local = self.opp_words['x']
        y_opp_words_local = self.opp_words['y']

        rect_opp_list = []

        past_first_column = False
        for i, word in enumerate(opp_words_list):

            if y_opp_words_local >= self.guess['y'] - size_opp_words or past_first_column:
                past_first_column = True

                adjacent_word_i = int(i - self.words_per_column)
                x_opp_words_local = rect_opp_list[adjacent_word_i][-1].right + gap_btwn_cols + size_tiles
                y_opp_words_local = rect_opp_list[adjacent_word_i][-1].center[1]

            rect_opp_list.append(self.display_word(word, size_opp_words, x_opp_words_local, y_opp_words_local))

            y_opp_words_local = y_opp_words_local + size_opp_words * self.gap_factor

        rect_opp_list = self.flatten(rect_opp_list)

        rect_flip = self.display_text(self.SurfObjs['flip'], self.flip['x'], self.flip['y'])

        rect_status = self.display_text(self.SurfObjs['status'], self.status['x'], self.status['y'])

        if 'flip' in graphics_to_update or 'flip_status' in graphics_to_update:
            rects_to_update.append(rect_flip)
        if 'tiles' in graphics_to_update:
            rects_to_update = rects_to_update + rect_tiles_list
        if 'self_words' in graphics_to_update:
            rects_to_update = rects_to_update + rect_self_list
        if 'opp_words' in graphics_to_update:
            rects_to_update = rects_to_update + rect_opp_list
        if 'guess' in graphics_to_update:
            rects_to_update.append(rect_guess)
        if 'status' in graphics_to_update:
            rects_to_update.append(rect_status)

        if self.first_time:
            pygame.display.update()
            self.first_time = False
        else:
            print(f"{rects_to_update}")
            pygame.display.update(rects_to_update)
