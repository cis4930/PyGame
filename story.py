import pygame, sys, random, glob

""" Player class for character in game
"""
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.img_position = 0		# first image in list of images (for animation)
		self.img_list = glob.glob("img/smurf*.png")		# create image list of all animation frames
		self.image = pygame.image.load(self.img_list[self.img_position])	# set image based on image position
		self.rect = self.image.get_rect()
		self.rect.top = 235			# positioning of player on screen
		self.rect.left = 180
		self.jump = "stop"
		self.jump_number = 0

"""	Used to more easily detect collision between character and other objects
"""
class PlayerRect(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((64, 110))
		self.rect = self.image.get_rect()

"""	Checkpoint class
"""
class Checkpoint(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/flag.png")		# set desired image
		self.rect = self.image.get_rect()
		self.rect.top = 250				# positioning of checkpoint on screen
		self.rect.left = 480

	# update checkpoint location on the screen so that it appears to move closer to character
	def update(self):
		self.rect.left -= 8

def jump_update(y, jump, number):
	jump_speed = 10
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

def main():
	pygame.init()
	screen = pygame.display.set_mode((600, 700))		# main window size
	clock = pygame.time.Clock()
	fps = 45			# frames per second
	

	background = pygame.image.load("img/swamp.png")		# load desired background image
	back_rect = background.get_rect()
	max_x = back_rect.right - 600						# bounds for background scrolling to create
	backsurf = pygame.Surface((600, 400))				#  somewhat seamless infinite loop

	x = 0			# initial x position for scrolling background

	gameOver = False

	character = Player()
	character_rect = PlayerRect()

	checkpoint = Checkpoint()
	checkpoint_group = pygame.sprite.Group()
	checkpoint_spawn_delay = 60
	checkpoint_spawn_delay_increment = 0

	BLUE = (0, 0, 255)

	checkpoint_reached_font = pygame.font.Font("FreeMonoBold.ttf", 28)
	checkpoint_reached_surf = checkpoint_reached_font.render("Checkpoint Reached!", True, BLUE)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if character.jump != "up" or character.jump != "down":
					if event.key == pygame.K_SPACE:
						if character.jump_number < 2:
							character.jump = "up"
							character.jump_number += 1
		
		# if maxium boundary is reached, reset x postion to beginning of background image
		if x > max_x:
			x = 0
		
		elif not gameOver:
			x += 1 				# increment x value for background scrolling
			backsurf.blit(background, (0, 0), (x, 0, 600 + x, 400))
			screen.blit(backsurf, (0, 0))

			screen.blit(character.image, character.rect)

			# if not at last position in image list, increment to next frame
			if character.img_position < 15:
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
			if checkpoint_spawn_delay > 0:
				checkpoint_spawn_delay -= 1
			else:
				checkpoint_group.add(Checkpoint())
				checkpoint_spawn_delay = checkpoint_spawn_delay_increment / 5
				if checkpoint_spawn_delay < 60:
					checkpoint_spawn_delay = 60
			checkpoint_group.update()
			checkpoint_group.draw(screen)

			# detect collision between player and checkpoint
			character_rect.rect.center = character.rect.center
			if pygame.sprite.spritecollideany(character_rect, checkpoint_group):
				screen.blit(checkpoint_reached_surf, (30,100))

		clock.tick(fps)
		pygame.display.update()
		checkpoint_spawn_delay_increment += 1

if __name__ == "__main__":
	main()