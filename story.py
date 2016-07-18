import pygame, sys, random, glob

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.img_position = 0
		self.img_list = glob.glob("img/smurf*.png")
		self.image = pygame.image.load(self.img_list[self.img_position])
		self.rect = self.image.get_rect()
		self.rect.top = 235
		self.rect.left = 180
		self.jump = "stop"
		self.jump_number = 0

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
	screen = pygame.display.set_mode((600, 400))
	clock = pygame.time.Clock()
	fps = 60
	

	# add bg img
	background = pygame.image.load("img/swamp.png")
	back_rect = background.get_rect()
	max_x = back_rect.right - 600
	backsurf = pygame.Surface((600, 400))

	x = 0

	character = Player()
	gameOver = False

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
		if x > max_x:
			x = 0
		
		elif not gameOver:
			x += 1
			backsurf.blit(background, (0, 0), (x, 0, 600 + x, 400))
			screen.blit(backsurf, (0, 0))

			character.rect.top, character.jump, character.jump_number = jump_update(character.rect.top, character.jump, character.jump_number)
			screen.blit(character.image, character.rect)

			if character.img_position < 15:
				character.img_position += 1
			else:
				character.img_position = 0

			character.image = pygame.image.load(character.img_list[character.img_position])

		clock.tick(fps)
		pygame.display.update()

if __name__ == "__main__":
	main()