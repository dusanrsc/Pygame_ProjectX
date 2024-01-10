# all static files (sprites) must be in the same path as main.pyw for proper working
# importing modules
import pygame
import random
import sys

# importing sub-modules
from random import randint

# initializing modules
pygame.init()
pygame.mixer.init()

# game settings
# game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Earth Defender"

FPS = 60
BULLET_SPEED = 30
MOB_SPEED = 8
EARTH_HEALTH = 3

# rgb color tuples
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ALPHA = GREEN

# game variables
__version__ = "v1.0"
running = True

# setting up screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TITLE = pygame.display.set_caption(f"{SCREEN_TITLE} {__version__}")
MOUSE_VISIBILITY = pygame.mouse.set_visible(False)

# game classes
# class player
class Player(pygame.sprite.Sprite):
	def __init__(self, pos_x=0, pos_y=0):
		super().__init__()
		self.image = pygame.image.load("player.png").convert()
		self.image.set_colorkey(ALPHA)
		self.rect = self.image.get_rect(center = [pos_x, pos_y])

	def update(self):
		self.rect.x = pygame.mouse.get_pos()[0]
		self.rect.y = pygame.mouse.get_pos()[1]

class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos_x=0, pos_y=0):
		super().__init__()
		self.image = pygame.image.load("bullet.png").convert_alpha()
		self.rect = self.image.get_rect(center = [pos_x, pos_y])

	def update(self):
		self.rect.x += BULLET_SPEED

		# destroying bullet mechanism 
		if self.rect.x >= SCREEN_WIDTH:
			self.kill()

# in gaming mob is enemy
class Mob(pygame.sprite.Sprite):
	def __init__(self, pos_x=SCREEN_WIDTH, pos_y=random.randint(10, SCREEN_HEIGHT - 10)):
		super().__init__()
		self.image = pygame.image.load("meteor.png").convert()
		self.image.set_colorkey(ALPHA)
		self.rect = self.image.get_rect(center = [pos_x, pos_y])

	def update(self):
		# mob movement direction
		self.rect.x -= MOB_SPEED

		# delete mob when is out of screen
		if self.rect.x <= -50:
			self.kill()

# game functions
# exit game function
def exit():
	pygame.quit()
	sys.exit()
	running = False

# health indicator
def earth_health_indicator():
	# earth thumbnail
	earth_thumbnail = pygame.image.load("earth_thumbnail.png")
	earth_thumbnail.set_colorkey(ALPHA)
	SCREEN.blit(earth_thumbnail, (30, 10))

	# 100% health
	pygame.draw.rect(SCREEN, GREEN, pygame.Rect(65, 25, (EARTH_HEALTH * 33), 15))
	pygame.draw.rect(SCREEN, WHITE, pygame.Rect(65, 25, 100, 15), 3)

	# 75% health
	if EARTH_HEALTH <= 2:
		pygame.draw.rect(SCREEN, YELLOW, pygame.Rect(65, 25, (EARTH_HEALTH * 33), 15))
		pygame.draw.rect(SCREEN, WHITE, pygame.Rect(65, 25, 100, 15), 3)

	# 50% health
	if EARTH_HEALTH <= 1:
		pygame.draw.rect(SCREEN, RED, pygame.Rect(65, 25, (EARTH_HEALTH * 33), 15))
		pygame.draw.rect(SCREEN, WHITE, pygame.Rect(65, 25, 100, 15), 3)

# creating sprite groups
# player sprite group
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

bullet_group = pygame.sprite.Group()
bullet = Bullet(pos_x=player.rect.x, pos_y=player.rect.y)
bullet_group.add(bullet)

mob_group = pygame.sprite.Group()
mob = Mob()
mob_group.add(mob)

# loading images
earth = pygame.image.load("earth.png")
earth.set_colorkey(ALPHA)

# main game loop
while running:
	# if key pressed statements
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	# create new mob when is out of the screen
	if mob.rect.x <= -50:
		mob = Mob(pos_y=random.randint(0, SCREEN_HEIGHT))
		mob_group.add(mob)

		# if asteroid (mob) hit earth 3x GAME OVER
		EARTH_HEALTH -= 1
		if EARTH_HEALTH < 0:
			exit()

	# triggering player shooting
	mouse_click = pygame.mouse.get_pressed()
	if mouse_click[0]:
		bullet = Bullet(pos_x=(player.rect.x), pos_y=(player.rect.y + 25))
		bullet_group.add(bullet)

	# checking for collisions
	# player hit mob
	if pygame.sprite.groupcollide(player_group, mob_group, True, False, pygame.sprite.collide_rect_ratio(.85)):
		print("GAME OVER!")

	# bullet hit mob
	if pygame.sprite.groupcollide(bullet_group, mob_group, True, True, pygame.sprite.collide_rect_ratio(1)):
		mob = Mob(pos_y=random.randint(0, SCREEN_HEIGHT))
		mob_group.add(mob)
		print("I ALREADY TOLD YA!")

	# drawing sprites on the screen
	SCREEN.fill(BLACK)
	SCREEN.blit(earth, (0, 0))

	bullet_group.update()
	bullet_group.draw(SCREEN)

	player_group.update()
	player_group.draw(SCREEN)

	mob_group.update()
	mob_group.draw(SCREEN)

	earth_health_indicator()

	# fps counter
	pygame.display.flip()
	pygame.time.Clock().tick(FPS)