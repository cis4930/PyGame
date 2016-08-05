'''     interface.py
     =============================

     classes:
        Action_Board_Class
        Action_Class
        Word_Class

     other methods:
        Set_Font_Size
        main     -     -     -     sample game 1  doesn't use action stuff
        main_two -     -     -     sample game 2  uses action stuff
'''


# imports
#--------------------------------------------
from __future__ import print_function

import copy, pygame, random, string, sys, glob, time
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

'''   Xing, if you find different colors matches the look better, here's where you can alter things easily
         colors - string value of the color:( red, green, blue )
         then as easy as changing string value for bg_color, matched_color, unmatched_color, and action_color
'''
# some shared initial values
#--------------------------------------------
pygame.init()       # initialize pygame
# format of colors = { 'color_name': ( R, G, B ) }
colors = { 'black': ( 0, 0, 0 ), 'blue': ( 0, 0, 200 ), 'green': ( 0, 200, 0 ), 'gray': ( 30, 30, 30 ), 'orange': ( 255, 165, 0 ), 'red': ( 200, 0, 0 ), 'white': ( 255, 255, 255 ), 'yellow': ( 255, 255, 0 ) }
word_coords = [ 50, 50 ]
bg_color = colors.get( 'black' )
matched_color = colors.get( 'blue' )
unmatched_color = colors.get( 'green' )
action_color = colors.get( 'orange' )
reward_points_multiplier = 25
reward_timer_multiplier = 1
reward_points = 0
reward_timer = 0
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# some font functionality
#--------------------------------------------
font_size_dict = { 25:[ 15, 26 ], 30:[ 18, 31 ], 38:[ 23, 39 ], 42:[ 25, 43] }
font = pygame.font.Font( 'media/fonts/FreeMonoBold.ttf', 42 )         # initialize font
font_width = font_size_dict[ 42 ][ 0 ]
font_height = font_size_dict[ 42 ][ 1 ]
def Set_Font_Size( size ):
     global font
     global font_width
     global font_height
     if size in font_size_dict.keys():
        print( "changing font size")
        font = pygame.font.Font( 'media/fonts/FreeMonoBold.ttf', size )         # initialize font
        font_width = font_size_dict[ size ][ 0 ]
        font_height = font_size_dict[ size ][ 1 ]
     else:
        pass

# load in dictionaries
''' Xing, note all_words is a property of interface.py
     rewards, timer, score within my test game refernces this, if you need ideas '''
#--------------------------------------------
f = open( 'dictionary.txt', 'r' )
r = f.read()
all_words = string.split( r, sep='\n' )
random.shuffle( all_words )
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''
        Xing,
         This class is majority of your interaction.
'''
# Action_Board_Class
#---------------------
#  Action_Board_Class( action_string_list )
#     due to font size, action_string_list is expected to have fewer than 7 items
#  Draw_Surface() is used privately
#  update( letter ) letter in string format ( key pressed by player )
#     returns None until a word is completed
#     returns name of action when word is completed as string
#--------------------------------------------
class Action_Board_Class:
     # Action_Board_Class __init__()
     #-----------------------------------------
     def __init__( self, action_string_list ):
        self.bg_surface_size = ( 800, 200 )
        self.bg_surface_obj = pygame.Surface( self.bg_surface_size )
        self.bg_surface_obj = self.bg_surface_obj.convert()
        self.action_string_list = []
        self.actions_dict = {}
        # set font size based on number of actions for comfortable fit
        # note, all font size in game testing below will be affected, but not outside of module
        if len( action_string_list ) <= 4:
         Set_Font_Size( 42 )
        elif len( action_string_list ) == 5:
         Set_Font_Size( 38 )
        elif len( action_string_list ) == 6:
         Set_Font_Size( 30 )
        elif len( action_string_list ) == 7:
         Set_Font_Size( 25 )
        else:
         return None    # too many actions
        # create action objects for each action in list
        for action in action_string_list:
         self.actions_dict[ action ] = Action_Class( action )
        self.action_string_list = list( self.actions_dict.keys() )
        self.Draw_Surface()
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

     # Action_Board_Class Draw_Surface()
     #-----------------------------------------
     def Draw_Surface( self ):
        self.bg_surface_obj.fill( bg_color )
        i = 1
        for action_object in self.actions_dict.values():
         temp_rect_obj = action_object.bg_surface_obj.get_rect()
         temp_rect_obj.left = 100
         temp_rect_obj.top = i
         i += temp_rect_obj.height
         self.bg_surface_obj.blit( action_object.bg_surface_obj, temp_rect_obj )
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

     # Action_Board_Class update()
     #-----------------------------------------
     def update( self, letter ):
        result_string = None
        for action_string in self.action_string_list:
         result = self.actions_dict[ action_string ].update( letter )
         self.Draw_Surface()
         if result == False:
            result_string = action_string
        if len( self.action_string_list ) == 0:
         self.action_string_list = list( self.actions_dict.keys() )
        return result_string
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Action_Class
#--------------------------------------------
class Action_Class:
     # Action_Class __init__()
     #-----------------------------------------
     def __init__( self, action_string ):
        self.word_incomplete = True
        # create action_id surface with appended ':'
        self.action_string = action_string
        self.action_word_value = string.upper( action_string ) + ": "
        self.action_word_surface = font.render( self.action_word_value, 1, action_color, bg_color )
        self.action_word_rect = self.action_word_surface.get_rect()
        # generate initial game_word
        self.New_Game_Word()
        self.Draw_Surface()
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

     # Action_Class Draw_Surface()
     #-----------------------------------------
     def Draw_Surface( self ):
        self.bg_surface_size = ( self.action_word_rect.width + self.game_word_rect.width, font_height )
        self.bg_surface_obj = pygame.Surface( self.bg_surface_size )
        self.bg_surface_obj = self.bg_surface_obj.convert()
        self.bg_surface_obj.fill( bg_color )
        self.bg_surface_obj.blit( self.action_word_surface, self.action_word_rect )
        self.bg_surface_obj.blit( self.game_word_obj.bg_surface_obj, self.game_word_rect )
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

     # Action_Class New_Game_Word()
     #-----------------------------------------
     def New_Game_Word( self ):
        self.game_word_obj = Word_Class( all_words.pop() )
        self.game_word_rect = self.game_word_obj.bg_surface_obj.get_rect()
        self.game_word_rect.left = self.action_word_rect.width
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

     # Action_Class Update()
     #-----------------------------------------
     def update( self, letter ):
        result = self.game_word_obj.update( letter )
        self.Draw_Surface()
        if result == False:
         self.New_Game_Word()
         self.Draw_Surface()
        return result
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Word_Class
#--------------------------------------------
class Word_Class:
     # Word_Class __init__()
     #-----------------------------------------
     def __init__ ( self, word_string ):
        self.bg_surface_size = ( len(word_string) * font_width, font_height )
        self.bg_surface_obj = pygame.Surface( self.bg_surface_size )
        self.bg_surface_obj = self.bg_surface_obj.convert()
        self.bg_surface_obj.fill( bg_color )
        self.match_index = 0
        self.string_value = string.upper( word_string )
        self.letter_surface_list = []
        # generate list of letter surface objects for ease of modifying
        for letter in self.string_value:
         self.letter_surface_list.append( font.render( letter, 1, unmatched_color, bg_color ) )
        self.temp_rect_obj = self.letter_surface_list[ 0 ].get_rect()
        # place letter surface objects onto bg_surface_obj
        for i in xrange( len( self.string_value ) ):
         self.temp_rect_obj.left = ( i * font_width )
         self.bg_surface_obj.blit( self.letter_surface_list[ i ], self.temp_rect_obj )
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

     # Word_Class update()
     #  returns false if complete, else true
     #-----------------------------------------
     def update( self, letter ):
        # if typed_letter matches word_letter at index
        if string.upper( letter ) == self.string_value[ self.match_index ]:
         self.letter_surface_list[ self.match_index ] = font.render( string.upper( letter ), 1, matched_color, bg_color )
         self.temp_rect_obj.left = ( self.match_index * font_width )
         self.bg_surface_obj.blit( self.letter_surface_list[ self.match_index ], self.temp_rect_obj )
         self.match_index = ( self.match_index + 1 )
        else:
         for i in xrange( 0, self.match_index ):
            self.letter_surface_list[ i ] = font.render( self.string_value[ i ] , 1, unmatched_color, bg_color )
            self.temp_rect_obj.left = ( i * font_width )
            self.bg_surface_obj.blit( self.letter_surface_list[ i ], self.temp_rect_obj )
         self.match_index = 0
        # check for word completion, return result
        if self.match_index == len( self.string_value ):
         return False
        else:
         return True
     #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


'''  The Xing Zone '''
""" Player class for character in game
"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.numberOfSprites = 8;
        self.img_position = 0       # first image in list of images (for animation)
        self.img_list = glob.glob("media/sprites/run*.png")     # create image list of all animation frames
        self.image = pygame.image.load(self.img_list[self.img_position])    # set image based on image position
        self.rect = self.image.get_rect()
        self.rect.top = 235         # positioning of player on screen
        self.rect.left = 20
        self.jump = "stop"
        self.jump_number = 0
    def setCrawl(self):
        self.numberOfSprites = 1;
        self.img_position = 0       # first image in list of images (for animation)
        self.img_list = glob.glob("media/sprites/crawl.png")     # create image list of all animation frames
        self.image = pygame.image.load(self.img_list[self.img_position])    # set image based on image position
        self.rect = self.image.get_rect()
        self.rect.top = 235+32         # positioning of player on screen
        self.rect.left = 20
    def setSpin(self):
        self.numberOfSprites = 19;
        self.img_position = 0       # first image in list of images (for animation)
        self.img_list = glob.glob("media/sprites/spin*.png")     # create image list of all animation frames
        self.image = pygame.image.load(self.img_list[self.img_position])    # set image based on image position
        self.rect = self.image.get_rect()
        self.rect.top = 235         # positioning of player on screen
        self.rect.left = 20
    def setRun(self):
        self.numberOfSprites = 8;
        self.img_position = 0       # first image in list of images (for animation)
        self.img_list = glob.glob("media/sprites/run*.png")     # create image list of all animation frames
        self.image = pygame.image.load(self.img_list[self.img_position])    # set image based on image position
        self.rect = self.image.get_rect()
        self.rect.top = 235         # positioning of player on screen
        self.rect.left = 20
""" Used to more easily detect collision between character and other objects
"""
class PlayerRect(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((64, 110))
        self.rect = self.image.get_rect()

""" Checkpoint class
"""
class Shell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/sprites/enemy02.png")      # set desired image
        self.rect = self.image.get_rect()
        self.rect.top = 250+32             # positioning of checkpoint on screen
        self.rect.left = 800
        self.soundObj = pygame.mixer.Sound("media/sounds/shell.wav")
        self.codename = "Shell"

    # update checkpoint location on the screen so that it appears to move closer to character
    def update(self):
        self.rect.left -= 4
class Slum(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/sprites/enemy03.png")      # set desired image
        self.rect = self.image.get_rect()
        self.rect.top = 200             # positioning of checkpoint on screen
        self.rect.left = 800
        self.soundObj = pygame.mixer.Sound("media/sounds/slum.wav")
        self.codename = "Slum"
    # update checkpoint location on the screen so that it appears to move closer to character
    def update(self):
        self.rect.left -= 4
class Elephant(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/sprites/enemy04.png")      # set desired image
        self.rect = self.image.get_rect()
        self.rect.top = 250+32             # positioning of checkpoint on screen
        self.rect.left = 800
        self.soundObj = pygame.mixer.Sound("media/sounds/elephant.wav")
        self.codename = "Elephant"
    # update checkpoint location on the screen so that it appears to move closer to character
    def update(self):
        self.rect.left -= 4
class Octopus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/sprites/enemy05.png")      # set desired image
        self.rect = self.image.get_rect()
        self.rect.top = 250+32             # positioning of checkpoint on screen
        self.rect.left = 800
        self.soundObj = pygame.mixer.Sound("media/sounds/octopus.wav")
        self.codename = "Octopus"
    # update checkpoint location on the screen so that it appears to move closer to character
    def update(self):
        self.rect.left -= 4
class Flower(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/sprites/enemy06.png")      # set desired image
        self.rect = self.image.get_rect()
        self.rect.top = 250+32             # positioning of checkpoint on screen
        self.rect.left = 800
        self.soundObj = pygame.mixer.Sound("media/sounds/flower.wav")
        self.codename = "Flower"
    # update checkpoint location on the screen so that it appears to move closer to character
    def update(self):
        self.rect.left -= 4
class George(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/sprites/george.png")      # set desired image
        self.rect = self.image.get_rect()
        self.rect.top = 250+32             # positioning of checkpoint on screen
        self.rect.left = 800
        self.soundObj = pygame.mixer.Sound("media/sounds/george.wav")
        self.codename = "George"
    # update checkpoint location on the screen so that it appears to move closer to character
    def update(self):
        self.rect.left -= 4
class GigaGeorge(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("media/sprites/giga-george.png")      # set desired image
        self.rect = self.image.get_rect()
        self.rect.top = 50             # positioning of checkpoint on screen
        self.rect.left = 800
        self.soundObj = pygame.mixer.Sound("media/sounds/giga-george.wav")
        self.codename = "GigaGeorge"
    # update checkpoint location on the screen so that it appears to move closer to character
    def update(self):
        self.rect.left -= 2

def jump_update(y, jump, number):
    jump_speed = 5
    if number == 1:
        if jump == "up" and y < 50:
            jump = "down"
    elif number == 2:
        if jump == "up" and y < -10:
            jump = "down"
    if jump == "down" and y >= 160:
        jump = "stop"
        y = 235
        number = 0
    if jump == "up":
        y = y - jump_speed
    elif jump == "down":
        y = y + jump_speed
    return(y, jump, number)
# This is a sample game using the new classes and new look.
#--------------------------------------------
def main_two():

    #Smurf stuff

    clock = pygame.time.Clock()
    fps = 60
    background_smurf = pygame.image.load("media/backgrounds/swamp.png")
    back_rect = background_smurf.get_rect()

    max_x = back_rect.right - 600                       # bounds for background scrolling to create
    

    x = 0

    scrolling_smurf = 0
    character = Player()
    character_rect = PlayerRect()

    checkpoint_group = pygame.sprite.Group()
    checkpoint_spawn_delay = 5
    checkpoint_spawn_start = time.time()
    #checkpoint_spawn_delay_increment = 0

    RED = (255, 0, 0)

    checkpoint_reached_font = pygame.font.Font("media/fonts/FreeMonoBold.ttf", 35)
    checkpoint_reached_surf = checkpoint_reached_font.render("You died!", True, RED)


     # dict of actions       ''' Xing, check out functions as values, may be helpful '''
    game_actions = {
        'jump': "Player jumps over something unknown!",
        'crawl': "Player crawls under danger!",
        'spin': "Flippin' spin with kick",
        'invisibility': "You are one with the shadows"
        }

     # some initial game values
    playing_game = True
    time_remains = True
    word_incomplete = True
    start = True
    game_over = False

     # initilize game screen
    screen_size = ( 800, 600 )    # ( width, height ) - game screen size
    screen = pygame.display.set_mode( screen_size )
    pygame.display.set_caption( "main_two() interface board testing" )

     # game background
    background = pygame.Surface( screen.get_size() )
    background = background.convert()

    smurf_state = "RUNNING"
    crawl_start = False
    spin_start = False
    action_starts = time.time()
    pygame.mixer.init()
    #setting sound
    npc = None
     # running game
    while playing_game:
        if x > max_x:
            x = 0
        x += 1              # increment x value for background scrolling
        
        background.blit(background_smurf, (0, 0), (x, 0, 600 + x, 800))
        screen.blit(background, (0, 0))
        if smurf_state == "RUNNING" or smurf_state == "JUMPING" or smurf_state == "CRAWLING" or smurf_state == "SPINNING" or smurf_state == "INVISIBLE":
            if smurf_state != "INVISIBLE":
                screen.blit(character.image, character.rect)

            # if not at last position in image list, increment to next frame
            if character.img_position < character.numberOfSprites-1:
                character.img_position += 1
            # else, reset image position to 0
            else:
                character.img_position = 0

            character.rect.top, character.jump, character.jump_number = jump_update(character.rect.top, character.jump, character.jump_number)
            character.image = pygame.image.load(character.img_list[character.img_position])

            for check in checkpoint_group:
                if check.rect.right < 0:
                    checkpoint_group.remove(check)

            # checkpoint spawing delay logic (still needs some work)
            if time.time() - checkpoint_spawn_start >= 2:
                if npc:
                    if npc.codename == "GigaGeorge":
                        if time.time() - checkpoint_spawn_start >= 6:
                            npc.soundObj.stop()

                    else:
                        npc.soundObj.stop()
            if time.time() - checkpoint_spawn_start >= checkpoint_spawn_delay:
                enemy = random.randint(0,6)
                #enemy = 1
                if enemy == 0:
                    checkpoint_spawn_delay = 5
                    npc = Shell()    
                elif enemy == 1:
                    checkpoint_spawn_delay = 5
                    npc = Slum()
                elif enemy == 2:
                    checkpoint_spawn_delay = 5
                    npc = Elephant()
                elif enemy == 3:
                    checkpoint_spawn_delay = 5
                    npc = Octopus()
                elif enemy == 4:
                    checkpoint_spawn_delay = 5
                    npc = Flower()
                elif enemy == 5:
                    checkpoint_spawn_delay = 5
                    npc = George()
                elif enemy == 6:
                    checkpoint_spawn_delay = 10
                    npc = GigaGeorge()
                    #pygame.mixer.music.load("img/angry-george.mp3")
                    #pygame.mixer.music.play()
                checkpoint_group.add(npc)
                npc.soundObj.play()
                    
                checkpoint_spawn_start = time.time()
            #if checkpoint_spawn_delay > 0:
            #    checkpoint_spawn_delay -= 1
            #else:
            #    checkpoint_group.add(Checkpoint())
                #checkpoint_spawn_delay = checkpoint_spawn_delay_increment / 5
                #if checkpoint_spawn_delay < 60:
                #    checkpoint_spawn_delay = 60
            checkpoint_group.update()
            checkpoint_group.draw(screen)

            # detect collision between player and checkpoint
            character_rect.rect.center = character.rect.center
            if smurf_state != "INVISIBLE":
                if pygame.sprite.spritecollideany(character_rect, checkpoint_group):
                    if smurf_state != "SPINNING":
                        screen.blit(checkpoint_reached_surf, (200,400))
                        for check in checkpoint_group:
                			checkpoint_group.remove(check)
                        seconds = 0 #die
                    else:
                        checkpoint_group.remove(npc)
        if smurf_state == "CRAWLING":
            if not crawl_start:
                character.setCrawl();
                crawl_start = True
            if time.time()-action_starts >= 1.5:
                smurf_state = "RUNNING"
                character.setRun()
                crawl_start = False
        if smurf_state == "SPINNING":
            if not spin_start:
                character.setSpin();
                spin_start = True
            if time.time()-action_starts >= 1.5:
                smurf_state = "RUNNING"
                character.setRun()
                spin_start = False
        if smurf_state == "INVISIBLE":
            if time.time()-action_starts >= 1.5:
                smurf_state = "RUNNING"
                character.setRun()
        # if time runs out, game over and display score and choice of replay
        ''' Xing, this can act as failing to complete word before running into obstical '''
        if not time_remains:
            game_over_message1 = "Congratulations!"
            game_over_message_surface1 = font.render( game_over_message1, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
            game_over_message_rect1 = game_over_message_surface1.get_rect()
            game_over_message_rect1.centerx = background.get_rect().centerx
            game_over_message_rect1.top = 149
            game_over_message2 = "You scored " + str( score ) + " points."
            game_over_message_surface2 = font.render( game_over_message2, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
            game_over_message_rect2 = game_over_message_surface2.get_rect()
            game_over_message_rect2.centerx = background.get_rect().centerx
            game_over_message_rect2.top = 224
            game_over_message3 = "Play again?"
            game_over_message_surface3 = font.render( game_over_message3, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
            game_over_message_rect3 = game_over_message_surface3.get_rect()
            game_over_message_rect3.centerx = background.get_rect().centerx
            game_over_message_rect3.top = 299
            background.fill( colors.get( 'black' ) )
            background.blit( game_over_message_surface1, game_over_message_rect1 )
            background.blit( game_over_message_surface2, game_over_message_rect2 )
            background.blit( game_over_message_surface3, game_over_message_rect3 )
            screen.blit( background, ( 0, 0 ) )
            pygame.display.flip()
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if pygame.key.name( event.key ) == 'n':
                            sys.exit()
                        if pygame.key.name( event.key ) == 'y':
                            start = True
                            time_remains = True
                            word_incomplete = True
                            game_over = False
                            checkpoint_spawn_start = time.time()
        # first game loop iteration initialization
        
        if start:
            # score
            score = 0      # starting score
            score_surface = font.render( str( score ), 1, colors.get( 'red' ), colors.get( 'yellow' ) )
            # timer
            start_time = time.time()
            seconds = 60   # starting timer in seconds
            timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
            timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
            timer_rect = timer_surface.get_rect()
            timer_rect.centerx = background.get_rect().centerx
            timer_rect.top = 35
            pygame.time.set_timer( pygame.USEREVENT + 1, 1000 )
            start = False
            # initialize interface_board
            action_object = Action_Board_Class( list( game_actions.keys() ) )
            temp_rect_obj = action_object.bg_surface_obj.get_rect()
            temp_rect_obj.top = 400

            #start music
            pygame.mixer.music.load("media/sounds/rainforest.mp3")
            pygame.mixer.music.play(-1, 0.0)

        # completed word, distribute rewards and update game
        if not word_incomplete:
            score = score + reward_points
            score_surface = font.render( str( score ), 1, colors.get( 'red' ), colors.get( 'yellow' ) )
            seconds = seconds + reward_timer
            timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
            timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
            word_incomplete = True
            ''' Xing, this is where the action occurs after completing the word '''
            if result_string:
                action_starts = time.time()
            if result_string == "jump":
                smurf_state = "JUMPING"
            if result_string == "crawl":
                smurf_state = "CRAWLING"
            if result_string == "spin":
                smurf_state = "SPINNING"
                soundObj = pygame.mixer.Sound("media/sounds/spin.wav")
                soundObj.play()
            if result_string == "invisibility":
                smurf_state = "INVISIBLE"
            print( game_actions[ result_string ] )
        if smurf_state == "JUMPING":
            if character.jump_number < 2:
                character.jump = "up"
                character.jump_number += 1
                smurf_state = "RUNNING"
        # refresh game background
        #background.fill( colors.get( 'black' ) )
        screen.blit( score_surface, ( 35, 35 ) )
        screen.blit( timer_surface, timer_rect )
        #screen.blit( background, ( 0, 0 ) )
        pygame.display.flip()
        
        # if all_words is empty, exit game -+- word_count[349464] so unlikely
        if len( all_words ) == 0:
            print( "Out of words!" )
            sys.exit()
        # keep going, all_words is not empty

        else:
        # rewards, timer, and score
            reward_points = reward_points_multiplier * len( all_words[ -1 ] )
            reward_timer = reward_timer_multiplier * len( all_words[ -1 ] )
            # animation -+-+-+-
            #background.blit( action_object.bg_surface_obj, temp_rect_obj )
            #screen.blit( background, ( 0, 0 ) )
            #pygame.display.flip()
         # while player is typing
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
        
                if event.type == pygame.KEYDOWN:
                    # clear background
                    #background.fill( colors.get( 'black' ) )
                    #screen.blit( background, ( 0, 0 ) )
                    pygame.display.flip()
                    # check typed letter against word
                    result_string = action_object.update( pygame.key.name( event.key ) )
                    if result_string is not None:
                        word_incomplete = False
                    # update word visually
                    screen.blit( score_surface, ( 35, 35 ) )
                    screen.blit( timer_surface, timer_rect )
                    background.blit( action_object.bg_surface_obj, temp_rect_obj )
                    #screen.blit( background, ( 0, 0 ) )
                    pygame.display.flip()
                            
                if event.type == pygame.USEREVENT + 1:
                    seconds = seconds - 1
                    if seconds > 0:
                        #background.fill( colors.get( 'black' ) )

                        screen.blit( background, ( 0, 0 ) )
                        pygame.display.flip()
                        timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
                        timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
                        pygame.time.set_timer( pygame.USEREVENT + 1, 1000 )
                        screen.blit( timer_surface, timer_rect )
                        screen.blit( score_surface, ( 35, 35 ) )
                        background.blit( action_object.bg_surface_obj, temp_rect_obj )
                        #screen.blit( background, ( 0, 0 ) )
                        #pygame.display.flip()
                    else:
                        pygame.mixer.music.stop()
                        time_remains = False
                        game_over = True
        #time


        clock.tick(fps)
        pygame.display.update()
        
        
        
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


# testing through __name__ == "__main__"
#--------------------------------------------
if __name__ == "__main__":
     main_two()
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+