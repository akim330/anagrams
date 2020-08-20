# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVYBLUE = (60, 60, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BGCOLOR = WHITE
TEXTCOLOR = BLACK

class Graphics:
    def __init__(self):
        #  ________
        # | LAYOUT |
        #  --------

        # 'Current'
        ''''
        font_current = 'freesansbold.ttf'
        size_current = 32
        color_current = BLACK
        x_current = 10
        y_current = 20
        '''

        self.current = {'font': 'freesansbold.ttf',
                        'size': 32,
                        'color': BLACK,
                        'x': 10,
                        'y': 20}

        # Ready Flip
        """
        font_flip = 'freesansbold.ttf'
        size_flip = 20
        color_flip = BLACK
        x_flip = 20
        y_flip = 60
        """

        self.flip = {'font': 'freesansbold.ttf',
                     'size': 20,
                     'color': BLACK,
                     'x': 20,
                     'y': 60}

        # Tiles
        """
        font_tile = 'freesansbold.ttf'
        size_tile = 32
        color_tile = BLACK
        x_tile_0 = 150
        y_tile_0 = 38
        x_gap_tile = 30
        y_gap_tile = 50
        """

        self.tile = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x_0': 150,
                     'y_0': 38,
                     'x_gap': 30,
                     'y_gap': 50}

        # 'Your Words'
        '''
        font_your = 'freesansbold.ttf'
        size_your = 32
        color_your = BLACK
        x_your = 10
        y_your = 100
        y_gap_your = 50
        '''

        self.your = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x': 10,
                     'y': 100,
                     'y_gap': 50}

        # Your Words

        '''
        font_words = 'freesansbold.ttf'
        size_words = 32
        color_words = BLACK
        x_words = 10
        y_words = y_your + y_gap_your
        x_gap_words = 150
        y_gap_words = 50
        '''

        self.self_words = {'font': 'freesansbold.ttf',
                     'size': 32,
                     'color': BLACK,
                     'x': 10,
                     'y': self.your['y'] + self.your['y_gap'],
                     'x_gap': 150,
                     'y_gap': 50}

        # 'Opponent's Words'
        '''
        font_opp = 'freesansbold.ttf'
        size_opp = 32
        color_opp = BLACK
        x_opp = 300
        y_opp = 100
        y_gap_opp = 50
        '''
        self.opp = {'font': 'freesansbold.ttf',
                    'size': 32,
                    'color': BLACK,
                    'x': 300,
                    'y': 100,
                    'y_gap': 50}


        # Opponent's Words
        '''
        font_opp_words = 'freesansbold.ttf'
        size_opp_words = 32
        color_opp_words = BLACK
        x_opp_words = 300
        y_opp_words = y_opp + y_gap_opp
        x_gap_opp_words = 150
        y_gap_opp_words = 50
        '''

        self.opp_words = {'font': 'freesansbold.ttf',
                          'size': 32,
                          'color': BLACK,
                          'x': 300,
                          'y': self.opp['y'] + self.opp['y_gap'],
                          'x_gap': 150,
                          'y_gap': 50}

        self.color_taken = BLUE

        # Guess
        '''
        font_guess = 'freesansbold.ttf'
        size_guess = 32
        color_guess = BLACK
        x_guess = 10
        y_guess = 500
        '''

        self.guess = {'font': 'freesansbold.ttf',
                      'size': 32,
                      'color': BLACK,
                      'x': 10,
                      'y': 500}

        # Status
        """
        font_status = 'freesansbold.ttf'
        size_status = 24
        color_status = BLACK
        x_status = 10
        y_status = 550
        """

        self.status = {'font': 'freesansbold.ttf',
                       'size': 24,
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

    def display_text_tiles(self, SurfaceObj, x, y):
        textRectObj = SurfaceObj.get_rect()
        textRectObj.center = (x, y)
        DISPLAYSURF.blit(SurfaceObj, textRectObj)

    def printstatus(self, game, player, graphics_to_update, guess, status):

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

        if 'flip' in graphics_to_update or 'flip_request' in graphics_to_update:
            self.SurfObjs['flip'] = self.fontObjs['flip'].render(game.flip_status, True, self.flip['color'])

        if 'tiles' in graphics_to_update:
            self.SurfObjs['tiles_list'] = []

            size_tiles, y_gap_tile, x_gap_tile = self.__numtiles_to_fontsize(len(game.current))
            self.fontObjs['tile'] = pygame.font.Font(self.self_words['font'], size_tiles)

            for tile in game.current:
                self.SurfObjs['tiles_list'].append(self.fontObjs['tile'].render(tile, True, self.tile['color']))

        if 'self_words' in graphics_to_update:
            self.SurfObjs['self_words_list'] = []

            size_words, y_gap_words = self.__numwords_to_fontsize(len(self_words_list))
            self.fontObjs['self_words'] = pygame.font.Font(self.self_words['font'], size_words)

            if who_took == 'self':
                for i, word in enumerate(self_words_list):
                    if i == game.new_word_i:
                        self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.color_taken))
                    else:
                        self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.self_words['color']))
            else:
                for word in game.self_words_list:
                    self.SurfObjs['self_words_list'].append(self.fontObjs['self_words'].render(word, True, self.self_words['color']))

        if 'opp_words' in graphics_to_update:
            self.SurfObjs['opp_words_list'] = []

            size_opp_words, y_gap_opp_words = self.__numwords_to_fontsize(len(opp_words_list))
            self.fontObjs['opp_words'] = pygame.font.Font(self.opp_words['font'], size_opp_words)

            if who_took == 'opp':
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
            self.statusSurfObj = self.fontObjs['status'].render(status, True, self.status['color'])

        # Reset graphics_to_update
        graphics_to_update = []

        # Display all the surface objects created above

        y_tile = self.tile['y_0']
        x_tile = self.tile['x_0']

        self.display_text(self.SurfObjs['current'], self.current['x'], self.current['y'])


        for i, tile in enumerate(self.SurfObjs['tiles_list']):
            x_tile = x_tile + self.tile['x_gap']

            self.display_text_tiles(tile, x_tile, y_tile)

            if i % 20 == 19:
                y_tile = y_tile + y_gap_tile
                x_tile = self.tile['x_0']

        self.display_text(self.SurfObjs['your'], self.your['x'], self.your['y'])


        x_words_local = self.words['x']
        y_words_local = self.words['y']

        for i, word in enumerate(self.SurfObjs['self_words_list']):

            self.display_text(word, x_words_local, y_words_local)

            if i % 10 == 9:
                x_words_local = x_words_local + self.words['x_gap']
                y_words_local = self.words['y'] - self.words['y_gap']

            y_words_local = y_words_local + self.words['y_gap']

        self.display_text(self.SurfObjs['guess'], self.guess['x'], self.guess['y'])


        self.display_text(self.SurfObjs['opp'], self.opp['x'], self.opp['y'])


        x_opp_words_local = self.opp_words['x']
        y_opp_words_local = self.opp_words['y']

        for i, word in enumerate(self.SurfObjs['opp_words_list']):

            self.display_text(word, x_opp_words_local, y_opp_words_local)


            if i % 10 == 9:
                x_opp_words_local = x_opp_words_local + self.opp_words['x_gap']
                y_opp_words_local = self.opp_words['y'] - self.opp_words['y_gap']

            y_opp_words_local = y_opp_words_local + self.opp_words['y_gap']

        self.display_text(self.SurfObjs['flip'], self.flip['x'], self.flip['y'])

        self.display_text(self.SurfObjs['status'], self.status['x'], self.status['y'])
