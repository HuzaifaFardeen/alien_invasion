import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
	'''a class to msnsge ship'''
	def __init__(self, ai_game):
		'''initialize the ship and set its starting position'''
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		self.settings = ai_game.settings
		#load ship image and get its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		#start each ship at bottom centre of screen
		self.rect.midbottom = self.screen_rect.midbottom
		#for store float for ship's horizontal position
		self.x = float(self.rect.x)
		
		#movement flag; start witha ship thst is not moving
		self.moving_right = False
		self.moving_left = False
		
	def update(self):
		'''update position based on flag'''
		#update x value not rect
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.x += self.settings.ship_speed
		elif self.moving_left and self.rect.left>0 :
			self.x -=self.settings.ship_speed
		#update rect value  	
		self.rect.x = self.x
	def blitme(self):
		'''draw ship at its current location'''
		self.screen.blit(self.image , self.rect)
	def center_ship(self):
		'''cntre ship on screen'''
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
