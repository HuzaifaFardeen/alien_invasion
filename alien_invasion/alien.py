import pygame
from pygame.sprite import Sprite 
class Alien(Sprite):
	'''class to represent single alien in a fleet'''
	def __init__(self, ai_game):
		'''initialize alien and set its starting position'''
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		#load image and get its rect
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		#start each new alien at top left of the screen
		self.rect.x = self.rect.width +10
		self.rect.y = self.rect.height+10
		#store alien's exact horizontal image
		self.x = float(self.rect.x)
	def check_edges(self):
		'''return true if alien at edge of screen'''
		screen_rect = self.screen.get_rect()
		return (self.rect.right >= screen_rect.right) or (self.rect.left<=0)
		
	def update(self):
		'''move alien to right'''
		self.x += self.settings.alien_speed * self.settings.fleet_direction
		self.rect.x = self.x	
		
