# all static files (sprites) must be in the same path as 'main.pyw' for proper working
# importing modules
import pygame
import random
import sys

# importing sub-modules
from random import randint

# initializing modules
pygame.init()
pygame.mixer.init()
pygame.font.init()

# game settings
# game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ProjectX"

FPS = 60
PLAYER_SPEED = 10
BULLET_SPEED = 30
ROCKET_SPEED = 10
METEOR_SPEED = 5
EARTH_HEALTH = 3

# rgb color tuples
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
SILVER = (150, 150, 150)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ALPHA = GREEN

# game variables
# settings
__version__ = "v1.0"
running = True
switch_screen = True
game_over_trigger = True
alpha_value = 128

# decoration
sun_pos_x = 200
moon_pos_x = 600
animation_counter = 0
score = 0

# weaponary variables
# bullets
bullet_ready = True
bullet_amount = 30
bullet_amount_maximum = bullet_amount

# rockets
rocket_ready = True
rocket_amount = 3

# setting up screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TITLE = pygame.display.set_caption(f"{SCREEN_TITLE} {__version__}")
MOUSE_VISIBILITY = pygame.mouse.set_visible(False)

# game lists
# explosion list
explosion = []
explosion.append(pygame.image.load("explosion0.png").convert())
explosion.append(pygame.image.load("explosion1.png").convert())
explosion.append(pygame.image.load("explosion2.png").convert())
explosion.append(pygame.image.load("explosion3.png").convert())
explosion.append(pygame.image.load("explosion4.png").convert())
explosion.append(pygame.image.load("explosion5.png").convert())
explosion.append(pygame.image.load("explosion6.png").convert())
explosion.append(pygame.image.load("explosion7.png").convert())

# game classes
# class player
class Player(pygame.sprite.Sprite):
	def __init__(self, pos_x=0, pos_y=0):
		super().__init__()
		self.image = pygame.image.load("player.png").convert()
		self.image.set_colorkey(ALPHA)
		self.rect = self.image.get_rect(center = [pos_x, pos_y])

	def update(self):
		self.rect.x = pygame.mouse.get_pos()[0] - 120
		self.rect.y = pygame.mouse.get_pos()[1] - 25

# class bullet
class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos_x=0, pos_y=0):
		super().__init__()
		self.image = pygame.image.load("bullet.png").convert()
		self.image.set_colorkey(ALPHA)
		self.rect = self.image.get_rect(center = [pos_x + 80, pos_y])

	def update(self):
		self.rect.x += BULLET_SPEED

		# destroying bullet mechanism 
		if self.rect.x >= SCREEN_WIDTH:
			self.kill()

# class rocket
class Rocket(pygame.sprite.Sprite):
	def __init__(self, pos_x=0, pos_y=0):
		super().__init__()
		self.image = pygame.image.load("rocket.png").convert()
		self.image.set_colorkey(ALPHA)
		self.rect = self.image.get_rect(center = [pos_x + 80, pos_y])

	def update(self):
		self.rect.x += ROCKET_SPEED

		# destroying bullet mechanism 
		if self.rect.x >= SCREEN_WIDTH:
			self.kill()

# in gaming mob is enemy
# class mob
class Meteor(pygame.sprite.Sprite):
	def __init__(self, pos_x=SCREEN_WIDTH, pos_y=random.randint(30, SCREEN_HEIGHT - 30)):
		super().__init__()
		self.image = pygame.image.load("meteor.png").convert()
		self.image.set_colorkey(ALPHA)
		self.rect = self.image.get_rect(center = [pos_x, pos_y])

	def update(self):
		# mob movement direction
		self.rect.x -= METEOR_SPEED

		# delete mob when is out of screen
		if self.rect.x <= -50:
			self.kill()

class Hudge_Meteor(pygame.sprite.Sprite):
	def __init__(self, pos_x=(SCREEN_WIDTH + SCREEN_WIDTH), pos_y=random.randint(30, SCREEN_HEIGHT - 30)):
		super().__init__()
		self.image = pygame.image.load("hudge_meteor.png").convert()
		self.image.set_colorkey(ALPHA)
		self.rect = self.image.get_rect(center = [pos_x, pos_y])

	def update(self):
		# mob movement direction
		self.rect.x -= METEOR_SPEED - 3

		# delete mob when is out of screen
		if self.rect.x <= -100:
			self.kill()

class Small_Meteor(pygame.sprite.Sprite):
	def __init__(self, pos_x=(SCREEN_WIDTH + SCREEN_WIDTH), pos_y=random.randint(30, SCREEN_HEIGHT - 30)):
		super().__init__()
		self.image = pygame.image.load("small_meteor.png").convert()
		self.image.set_colorkey(ALPHA)
		self.rect = self.image.get_rect(center = [pos_x, pos_y])

	def update(self):
		# mob movement direction
		self.rect.x -= METEOR_SPEED + 3

		# delete mob when is out of screen
		if self.rect.x <= -100:
			self.kill()

# game functions
# exit game function
def exit():
	pygame.quit()
	sys.exit()
	running = False

# indicators
# health indicator
def earth_health_indicator():
	# earth thumbnail
	earth_thumbnail = pygame.image.load("earth_thumbnail.png")
	earth_thumbnail.set_colorkey(ALPHA)

	# 100% health
	pygame.draw.rect(SCREEN, SILVER, pygame.Rect(65, 15, 100, 15))
	pygame.draw.rect(SCREEN, GREEN, pygame.Rect(65, 15, (EARTH_HEALTH * 33), 15))
	pygame.draw.rect(SCREEN, WHITE, pygame.Rect(65, 15, 100, 15), 3)

	# 75% health
	if EARTH_HEALTH <= 2:
		pygame.draw.rect(SCREEN, YELLOW, pygame.Rect(65, 15, (EARTH_HEALTH * 33), 15))
		pygame.draw.rect(SCREEN, WHITE, pygame.Rect(65, 15, 100, 15), 3)

	# 50% health
	if EARTH_HEALTH <= 1:
		pygame.draw.rect(SCREEN, RED, pygame.Rect(65, 15, (EARTH_HEALTH * 33), 15))
		pygame.draw.rect(SCREEN, WHITE, pygame.Rect(65, 15, 100, 15), 3)

	SCREEN.blit(earth_thumbnail, (150, 11))

def bullet_overheat():
	# 100% bullets
	pygame.draw.rect(SCREEN, SILVER, pygame.Rect(210, 15, 480, 15))
	pygame.draw.rect(SCREEN, GREEN, pygame.Rect(210, 15, (bullet_amount) * 16, 15))
	pygame.draw.rect(SCREEN, WHITE, pygame.Rect(210, 15, 480, 15), 3)

	# text
	my_font = pygame.font.SysFont("Comic Sans MS", 25)
	text_bullets = my_font.render("BULLETS", False, RED)
	SCREEN.blit(text_bullets, (410, 25))

	my_font = pygame.font.SysFont("Comic Sans MS", 25)
	text_bullets_0 = my_font.render("0", False, RED)
	text_bullets_30 = my_font.render("30", False, GREEN)

	SCREEN.blit(text_bullets_0, (190, 4))
	SCREEN.blit(text_bullets_30, (692, 4))

# rocket indicator
def rockets_indicator():
	# rocket thumbnail
	if rocket_amount == 3:
		rocket_thumbnail1 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail1.set_colorkey(ALPHA)

		rocket_thumbnail2 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail2.set_colorkey(ALPHA)

		rocket_thumbnail3 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail3.set_colorkey(ALPHA)

		SCREEN.blit(rocket_thumbnail1, (730, 10))
		SCREEN.blit(rocket_thumbnail2, (750, 10))
		SCREEN.blit(rocket_thumbnail3, (770, 10))

	elif rocket_amount == 2:
		rocket_thumbnail1 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail1.set_colorkey(ALPHA)

		rocket_thumbnail2 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail2.set_colorkey(ALPHA)

		rocket_thumbnail3 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail3.set_colorkey(ALPHA)
		rocket_thumbnail3.set_alpha(alpha_value)

		SCREEN.blit(rocket_thumbnail1, (730, 10))
		SCREEN.blit(rocket_thumbnail2, (750, 10))
		SCREEN.blit(rocket_thumbnail3, (770, 10))

	elif rocket_amount == 1:
		rocket_thumbnail1 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail1.set_colorkey(ALPHA)

		rocket_thumbnail2 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail2.set_colorkey(ALPHA)
		rocket_thumbnail2.set_alpha(alpha_value)

		rocket_thumbnail3 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail3.set_colorkey(ALPHA)
		rocket_thumbnail3.set_alpha(alpha_value)

		SCREEN.blit(rocket_thumbnail1, (730, 10))
		SCREEN.blit(rocket_thumbnail2, (750, 10))
		SCREEN.blit(rocket_thumbnail3, (770, 10))

	else:
		rocket_thumbnail1 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail1.set_colorkey(ALPHA)
		rocket_thumbnail1.set_alpha(alpha_value)

		rocket_thumbnail2 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail2.set_colorkey(ALPHA)
		rocket_thumbnail2.set_alpha(alpha_value)

		rocket_thumbnail3 = pygame.image.load("rocket_thumbnail.png")
		rocket_thumbnail3.set_colorkey(ALPHA)
		rocket_thumbnail3.set_alpha(alpha_value)

		SCREEN.blit(rocket_thumbnail1, (730, 10))
		SCREEN.blit(rocket_thumbnail2, (750, 10))
		SCREEN.blit(rocket_thumbnail3, (770, 10))

def menu():
	pass

# creating sprite groups
# player sprite group
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

bullet_group = pygame.sprite.Group()
bullet = Bullet(pos_x=player.rect.x, pos_y=player.rect.y)
bullet_group.add(bullet)

rocket_group = pygame.sprite.Group()
rocket = Bullet(pos_x=player.rect.x, pos_y=player.rect.y)
rocket_group.add(rocket)

meteor_group = pygame.sprite.Group()
meteor = Meteor()
meteor_group.add(meteor)

hudge_meteor_group = pygame.sprite.Group()
hudge_meteor = Hudge_Meteor()
hudge_meteor_group.add(hudge_meteor)

small_meteor_group = pygame.sprite.Group()
small_meteor = Small_Meteor()
small_meteor_group.add(small_meteor)

# loading decoration images
# earth image
earth = pygame.image.load("earth.png")
earth.set_colorkey(ALPHA)

# sun image
sun = pygame.image.load("sun.png")
sun.set_colorkey(ALPHA)

# moon image
moon = pygame.image.load("moon.png")
moon.set_colorkey(ALPHA)

# main game loop
while running:
	# decoration movement
	sun_pos_x += 0.5
	moon_pos_x -= 0.5

	# decoration repositioning
	if sun_pos_x >= SCREEN_WIDTH:
		sun_pos_x = (SCREEN_WIDTH - SCREEN_WIDTH - 500)

	if moon_pos_x <= (SCREEN_WIDTH - SCREEN_WIDTH - 500):
		moon_pos_x = SCREEN_WIDTH

	# if key pressed statements
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	# create new mob when is out of the screen
	if meteor.rect.x <= -50:
		meteor = Meteor(pos_y=random.randint(0, SCREEN_HEIGHT))
		meteor_group.add(meteor)

		# if meteor (mob) hit earth 3x GAME OVER
		EARTH_HEALTH -= 1
		if EARTH_HEALTH < 0:
			bullet_ready = False
			rocket_ready = False

			game_over_trigger = False
			player.kill()

	if hudge_meteor.rect.x <= -50:
		hudge_meteor = Small_Meteor(pos_y=random.randint(0, SCREEN_HEIGHT * 12))
		hudge_meteor_group.add(hudge_meteor)

		# if meteor (mob) hit earth 3x GAME OVER
		EARTH_HEALTH -= 3
		if EARTH_HEALTH < 0:
			bullet_ready = False
			rocket_ready = False

			game_over_trigger = False
			player.kill()

	if small_meteor.rect.x <= -50:
		small_meteor = Small_Meteor(pos_y=random.randint(0, SCREEN_HEIGHT))
		small_meteor_group.add(small_meteor)

		# if meteor (mob) hit earth 3x GAME OVER
		EARTH_HEALTH -= 1
		if EARTH_HEALTH < 0:
			bullet_ready = False
			rocket_ready = False

			game_over_trigger = False
			player.kill()

	# keyboard imput
	keys = pygame.key.get_pressed()

	# fullscreen and window mode switcher
	if keys[pygame.K_f] and switch_screen == True:
		SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
		switch_screen = False

	elif keys[pygame.K_f] and switch_screen == False:
		SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		switch_screen = True

	# triggering player shooting
	# on left mouse click fire bullets
	mouse_click = pygame.mouse.get_pressed()
	# condition for fireing bullets
	if mouse_click[0] and bullet_amount > 0 and bullet_ready == True:
		bullet_amount -= 1
		bullet = Bullet(pos_x=(player.rect.x), pos_y=(player.rect.y + 25))
		bullet_group.add(bullet)

	# bullet reloading mechanism
	elif bullet_amount <= bullet_amount:
		bullet_amount += 0.1
		if bullet_amount >= bullet_amount_maximum:
			bullet_amount = bullet_amount_maximum

	# on right mouse click fire rockets
	if mouse_click[2] and rocket_amount > 0 and rocket_ready == True:
		rocket_amount -= 1
		# drawing rockets on right mouse click (fire)
		rocket = Rocket(pos_x=(player.rect.x), pos_y=(player.rect.y + 25))
		rocket_group.add(rocket)

	# checking for collisions
	# player hit mob
	if pygame.sprite.groupcollide(player_group, meteor_group, True, False, pygame.sprite.collide_rect_ratio(.85)):
		# if mob hit player bullets and rockets not fireing
		bullet_ready = False
		rocket_ready = False

		# game over triger
		game_over_trigger = False

	if pygame.sprite.groupcollide(player_group, hudge_meteor_group, True, False, pygame.sprite.collide_rect_ratio(.85)):
		# if mob hit player bullets and rockets not fireing
		bullet_ready = False
		rocket_ready = False

		# game over triger
		game_over_trigger = False

	if pygame.sprite.groupcollide(player_group, small_meteor_group, True, False, pygame.sprite.collide_rect_ratio(.85)):
		# if mob hit player bullets and rockets not fireing
		bullet_ready = False
		rocket_ready = False

		# game over triger
		game_over_trigger = False

	# bullet hit metheor
	if pygame.sprite.groupcollide(bullet_group, meteor_group, True, True, pygame.sprite.collide_rect_ratio(1)):
		meteor = Meteor(pos_y=random.randint(30, SCREEN_HEIGHT - 30))
		meteor_group.add(meteor)

		score += 5

	# rocket hit metheor
	if pygame.sprite.groupcollide(rocket_group, meteor_group, False, True, pygame.sprite.collide_rect_ratio(1)):
		meteor = Meteor(pos_y=random.randint(30, SCREEN_HEIGHT - 30))
		meteor_group.add(meteor)

		score += 10

	# bullet hit hudge meteor
	if pygame.sprite.groupcollide(bullet_group, hudge_meteor_group, True, False, pygame.sprite.collide_rect_ratio(1)):
		pass

	# rocket hit hudge meteor
	if pygame.sprite.groupcollide(rocket_group, hudge_meteor_group, True, True, pygame.sprite.collide_rect_ratio(1)):
		hudge_meteor_group = pygame.sprite.Group()
		hudge_meteor = Hudge_Meteor(pos_x=random.randint(4500, 5500))
		hudge_meteor_group.add(hudge_meteor)

		score += 20

	# bullet hit small meteor
	if pygame.sprite.groupcollide(bullet_group, small_meteor_group, True, True, pygame.sprite.collide_rect_ratio(1)):
		pass

	# rocket hit small meteor
	if pygame.sprite.groupcollide(rocket_group, small_meteor_group, True, True, pygame.sprite.collide_rect_ratio(1)):
		small_meteor_group = pygame.sprite.Group()
		small_meteor = Small_Meteor(pos_x=random.randint(9500, 10500))
		small_meteor_group.add(small_meteor)

		score += 30

	# drawing sprites on the screen
	SCREEN.fill(BLACK)

	SCREEN.blit(earth, (0, 0))
	SCREEN.blit(sun, (sun_pos_x, 100))
	SCREEN.blit(moon, (moon_pos_x, 500))

	bullet_group.update()
	bullet_group.draw(SCREEN)

	rocket_group.update()
	rocket_group.draw(SCREEN)

	player_group.update()
	player_group.draw(SCREEN)

	meteor_group.update()
	meteor_group.draw(SCREEN)

	hudge_meteor_group.update()
	hudge_meteor_group.draw(SCREEN)

	small_meteor_group.update()
	small_meteor_group.draw(SCREEN)

	earth_health_indicator()
	bullet_overheat()
	rockets_indicator()

	# condition for displaying game over text over the screen
	if game_over_trigger == False:
		# game over text
		my_font = pygame.font.SysFont("Comic Sans MS", 90)
		game_over = my_font.render("GAME OVER!", False, RED)
		SCREEN.blit(game_over, ((SCREEN_WIDTH // 6), (SCREEN_HEIGHT // 2.5)))

		# game over score
		my_font = pygame.font.SysFont("Comic Sans MS", 30)
		game_over_score  = my_font.render(f"SCORE: {score}", False, GREEN)
		SCREEN.blit(game_over_score, ((SCREEN_WIDTH // 2.4), (SCREEN_HEIGHT // 1.75)))

	# fps counter
	pygame.display.flip()
	pygame.time.Clock().tick(FPS)