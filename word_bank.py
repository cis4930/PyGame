'''		word_bank.py
	=============================

	classes:
		Word_Class

	other methods:

'''

# imports
#--------------------------------------------
from __future__ import print_function

import pygame, random, string, sys
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# some shared initial values
#--------------------------------------------
pygame.init()		# initialize pygame
# format of colors = { 'color_name': ( R, G, B ) }
colors = { 'black': ( 0, 0, 0 ), 'blue': ( 0, 0, 200 ), 'green': ( 0, 200, 0 ), 'orange': ( 255, 165, 0 ), 'red': ( 200, 0, 0 ), 'white': ( 255, 255, 255 ), 'yellow': ( 255, 255, 0 ) }
word_coords = [ 50, 50 ]
font = pygame.font.Font( './FreeMonoBold.ttf', 42 )			# initialize font
bg_color = colors.get( 'black' )
matched_color = colors.get( 'blue' )
unmatched_color = colors.get( 'green' )
reward_points_multiplier = 25
reward_timer_multiplier = 1
reward_points = 0
reward_timer = 0
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# load in dictionaries
#--------------------------------------------
f = open( 'dictionary.txt', 'r' )
r = f.read()
all_words = string.split( r, sep='\n' )
random.shuffle( all_words )
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Word_Class
#--------------------------------------------
class Word_Class:
	# Word_Class __init__()
	#-----------------------------------------
	def __init__ ( self, word_string ):
		self.bg_surface_size = ( len(word_string) * 25, 43 )
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
			self.temp_rect_obj.left = ( i * 25 )
			self.bg_surface_obj.blit( self.letter_surface_list[ i ], self.temp_rect_obj )
	#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

	# Word_Class update()
	#	returns false if complete, else true
	#-----------------------------------------
	def update( self, letter ):
		# if typed_letter matches word_letter at index
		if string.upper( letter ) == self.string_value[ self.match_index ]:
			self.letter_surface_list[ self.match_index ] = font.render( letter, 1, matched_color, bg_color )
			self.temp_rect_obj.left = ( self.match_index * 25 )
			self.bg_surface_obj.blit( self.letter_surface_list[ self.match_index ], self.temp_rect_obj )
			self.match_index = ( self.match_index + 1 )
		else:
			for i in xrange( 0, self.match_index ):
				self.letter_surface_list[ i ] = font.render( self.string_value[ i ] , 1, unmatched_color, bg_color )
				self.temp_rect_obj.left = ( i * 25 )
				self.bg_surface_obj.blit( self.letter_surface_list[ i ], self.temp_rect_obj )
			self.match_index = 0
		# check for word completion, return result
		if self.match_index == len( self.string_value ):
			return False
		else:
			return True
	#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# main()
#				simulates launcher.py
#--------------------------------------------
def main():
	# some initial values
	screen_size = ( 800, 600 ) 		# ( height, width )
	playing_game = True
	time_remains = True
	word_incomplete = True
	start = True
	game_over = False

	# initilize pygame screen
	screen = pygame.display.set_mode( screen_size )
	pygame.display.set_caption( "word_bank testing" )

	background = pygame.Surface( screen.get_size() )
	background = background.convert()

	while playing_game:
		if not time_remains:			# game over, display score and choice of replay
			game_over_message1 = "Congratulations!"
			game_over_message2 = "You scored " + str( score ) + " points."
			game_over_message3 = "Play again?"
			game_over_message_surface1 = font.render( game_over_message1, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
			game_over_message_rect1 = game_over_message_surface1.get_rect()
			game_over_message_rect1.centerx = background.get_rect().centerx
			game_over_message_rect1.top = 149
			game_over_message_surface2 = font.render( game_over_message2, 1, colors.get( 'red' ), colors.get( 'yellow' ) )
			game_over_message_rect2 = game_over_message_surface2.get_rect()
			game_over_message_rect2.centerx = background.get_rect().centerx
			game_over_message_rect2.top = 224
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

		if start:				# some starting values
			score = 0
			seconds = 10
			timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
			timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
			timer_rect = timer_surface.get_rect()
			timer_rect.centerx = background.get_rect().centerx
			timer_rect.top = 35
			score_surface = font.render( str( score ), 1, colors.get( 'red' ), colors.get( 'yellow' ) )
			pygame.time.set_timer( pygame.USEREVENT + 1, 1000 )
			start = False

		if not word_incomplete:		# completed word, distribute rewards and update game
			score = score + reward_points
			score_surface = font.render( str( score ), 1, colors.get( 'red' ), colors.get( 'yellow' ) )
			seconds = seconds + reward_timer
			timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
			timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
			word_incomplete = True

		# refresh background
		background.fill( colors.get( 'black' ) )
		background.blit( score_surface, ( 35, 35 ) )
		background.blit( timer_surface, timer_rect )
		screen.blit( background, ( 0, 0 ) )
		pygame.display.flip()

		if len( all_words ) == 0:			# if all_words is empty, exit game [349464]
			print( "Out of words!" )
			sys.exit()
		else:										# keep going, all_words is fine
		# rewards, timer, and score -------
			reward_points = reward_points_multiplier * len( all_words[ -1 ] )
			reward_timer = reward_timer_multiplier * len( all_words[ -1 ] )
		# randomly place word
			game_word = Word_Class( all_words.pop() )
			temp_rect_obj = game_word.bg_surface_obj.get_rect()
			temp_rect_obj.left = random.randint( 100, (750 - temp_rect_obj.width) )
			temp_rect_obj.top = random.randint( 200, 500 )
		# animation -+-+-+-
			background.blit( game_word.bg_surface_obj, temp_rect_obj )
			screen.blit( background, ( 0, 0 ) )
			pygame.display.flip()
			# while player is typing
			while word_incomplete and time_remains:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					if event.type == pygame.KEYDOWN:
						# clear background
						background.fill( colors.get( 'black' ) )
						screen.blit( background, ( 0, 0 ) )
						pygame.display.flip()
						# check typed letter against word
						word_incomplete = game_word.update( string.upper( pygame.key.name( event.key ) ) )
						# update word visually
						background.blit( score_surface, ( 35, 35 ) )
						background.blit( timer_surface, timer_rect )
						background.blit( game_word.bg_surface_obj, temp_rect_obj )
						screen.blit( background, ( 0, 0 ) )
						pygame.display.flip()
					if event.type == pygame.USEREVENT + 1:
						seconds = seconds - 1
						if seconds > 0:
							background.fill( colors.get( 'black' ) )
							screen.blit( background, ( 0, 0 ) )
							pygame.display.flip()
							timer_str = str( seconds / 60 ) + ':' + str( seconds % 60 )
							timer_surface = font.render( timer_str, 1, colors.get( 'black' ), colors.get( 'orange' ) )
							pygame.time.set_timer( pygame.USEREVENT + 1, 1000 )
							background.blit( timer_surface, timer_rect )
							background.blit( score_surface, ( 35, 35 ) )
							background.blit( game_word.bg_surface_obj, temp_rect_obj )
							screen.blit( background, ( 0, 0 ) )
							pygame.display.flip()
						else:
							time_remains = False
							game_over = True
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


# simulate launcher.py through main()
#--------------------------------------------
if __name__ == "__main__":
	main()
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+