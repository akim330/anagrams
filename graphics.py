import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVYBLUE = (60, 60, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BGCOLOR = WHITE
TEXTCOLOR = BLACK

WINDOWWIDTH = 640
WINDOWHEIGHT = 640

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

class Graphics:
    def __init__(self):
        #  ________
        # | LAYOUT |
        #  --------

        self.first_time = True


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
                     'y_gap': 50}

        # Your Words
        self.self_words = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x': 10,
                     'y': self.your['y'] + self.your['y_gap'],
                     'x_gap': 150,
                     'y_gap': 50}

        # 'Opponent's Words'
        self.opp = {'font': 'freesansbold.ttf',
                    'size': 32,
                    'color': BLACK,
                    'x': 300,
                    'y': 100,
                    'y_gap': 50}


        # Opponent's Words
        self.opp_words = {'font': 'freesansbold.ttf',
                          'size': 32,
                          'color': BLACK,
                          'x': 300,
                          'y': self.opp['y'] + self.opp['y_gap'],
                          'x_gap': 150,
                          'y_gap': 50}

        self.color_taken = BLUE

        # Guess
        self.guess = {'font': 'freesansbold.ttf',
                      'size': 32,
                      'color': BLACK,
                      'x': 10,
                      'y': 500}

        # Status
        self.status = {'font': 'freesansbold.ttf',
                       'size': 20,
                       'color': BLACK,
                       'x': 10,
                       'y': 550}

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


    def __numwords_to_fontsize(self, numwords):
        if numwords <= 6:
            return int(self.self_words['size'] / 1.25), int(self.self_words['y_gap'] / 1.25)
        elif 6 < numwords <= 10:
            return int(self.self_words['size'] / 1.75), int(self.self_words['y_gap'] / 1.75)
        elif 10 < numwords <= 20:
            return int(self.self_words['size'] / 2), int(self.self_words['y_gap'] / 2)
        elif 20 < numwords <= 50:
            return int(self.self_words['size'] / 3), int(self.self_words['y_gap'] / 3)

    def __numtiles_to_fontsize(self, numtiles):
        if numtiles <= 10:
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

    def printstatus(self, game, player, graphics_to_update, guess, status, taker):

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

        if 'flip' in graphics_to_update or 'flip_status' in graphics_to_update:
            print(f"Updating flip status to {game.flip_status}!")
            self.SurfObjs['flip'] = self.fontObjs['flip'].render(game.flip_status, True, self.flip['color'])


        if 'tiles' in graphics_to_update:
            print("UPDATING TILES")
            self.SurfObjs['tiles_list'] = []

            self.fontObjs['tile'] = pygame.font.Font(self.self_words['font'], size_tiles)

            for tile in game.current:
                self.SurfObjs['tiles_list'].append(self.fontObjs['tile'].render(tile, True, self.tile['color']))

        if 'self_words' in graphics_to_update:
            self.SurfObjs['self_words_list'] = []

            size_words, y_gap_words = self.__numwords_to_fontsize(len(self_words_list))
            self.fontObjs['self_words'] = pygame.font.Font(self.self_words['font'], size_words)

            if taker == 'self':
                print(f"BLUE; i: {game.new_word_i}")
                for i, word in enumerate(self_words_list):
                    if i == game.new_word_i:
                        print(f"FOUND BLUE")
                        self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.color_taken))
                    else:
                        self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.self_words['color']))
            else:
                print("NO BLUE")
                for word in self_words_list:
                    self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.self_words['color']))

        if 'opp_words' in graphics_to_update:
            self.SurfObjs['opp_words_list'] = []

            size_opp_words, y_gap_opp_words = self.__numwords_to_fontsize(len(opp_words_list))
            self.fontObjs['opp_words'] = pygame.font.Font(self.opp_words['font'], size_opp_words)

            if taker == 'opp':
                for i, word in enumerate(opp_words_list):
                    if i == game.new_word_i:
                        self.SurfObjs['opp_words_list'].append(self.fontObjs['opp_words'].render(word, True, self.color_taken))
                    else:
                        self.SurfObjs['opp_words_list'].append(self.fontObjs['opp_words'].render(word, True, self.opp_words['color']))
            else:
                for word in opp_words_list:
                    self.SurfObjs['opp_words_list'].append(self.fontObjs['opp_words'].render(word, True, self.opp_words['color']))

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

        for i, tile in enumerate(self.SurfObjs['tiles_list']):
            x_tile = x_tile + self.tile['x_gap']

            self.display_text_tiles(tile, x_tile, y_tile)

            if i % 20 == 19:
                y_tile = y_tile + y_gap_tile
                x_tile = self.tile['x_0']

        _ = self.display_text(self.SurfObjs['your'], self.your['x'], self.your['y'])


        x_words_local = self.self_words['x']
        y_words_local = self.self_words['y']

        rect_self_list = []

        for i, word in enumerate(self.SurfObjs['self_words_list']):

            rect_self_list.append(self.display_text(word, x_words_local, y_words_local))

            if i % 10 == 9:
                x_words_local = x_words_local + self.self_words['x_gap']
                y_words_local = self.self_words['y'] - self.self_words['y_gap']

            y_words_local = y_words_local + self.self_words['y_gap']

        rect_guess = self.display_text(self.SurfObjs['guess'], self.guess['x'], self.guess['y'])

        _ = self.display_text(self.SurfObjs['opp'], self.opp['x'], self.opp['y'])

        x_opp_words_local = self.opp_words['x']
        y_opp_words_local = self.opp_words['y']

        rect_opp_list = []

        for i, word in enumerate(self.SurfObjs['opp_words_list']):

            rect_opp_list.append(self.display_text(word, x_opp_words_local, y_opp_words_local))

            if i % 10 == 9:
                x_opp_words_local = x_opp_words_local + self.opp_words['x_gap']
                y_opp_words_local = self.opp_words['y'] - self.opp_words['y_gap']

            y_opp_words_local = y_opp_words_local + self.opp_words['y_gap']

        rect_flip = self.display_text(self.SurfObjs['flip'], self.flip['x'], self.flip['y'])

        rect_status = self.display_text(self.SurfObjs['status'], self.status['x'], self.status['y'])

        if 'flip' in graphics_to_update or 'flip_status' in graphics_to_update:
            rects_to_update.append(rect_flip)
        if 'tiles' in graphics_to_update:
            rects_to_update.append(rect_tiles)
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
            pygame.display.update(rects_to_update)
