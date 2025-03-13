import sys , pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard 
from button import Button
class AlienInvasion:
	'''class to manage and control game assets and behaviour'''
	def __init__(self):
		'''initialize the game and create game resources'''
		pygame.init()
		self.clock = pygame.time.Clock()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption('Alien Invasion')
		# the game starts in an in active state
		self.game_active = False
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()
		#make the play button
		self.play_button = Button(self,'play')
		
	def run_game(self):
		'''start main game loop'''
		while True:
			pygame.mouse.set_visible(not self.game_active)
			self._check_events()
			if self.game_active:
				self._update_bullets()
				self._update_aliens()
				self.ship.update()
			self._update_screen()
			
	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)				
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
	def _check_play_button(self,mouse_pos):
		'''start new game when player clicks play'''
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.game_active:
			self.stats.reset_stats()
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			self.bullets.empty()
			self.aliens.empty()
			self._create_fleet()
			self.ship.center_ship()	
			self.settings.initialize_dynamic_settings()
			self.game_active = True
	def _check_keydown_events(self,event):
		if event.key == pygame.K_RIGHT:
			#move ship to right
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			#move ship to right
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()				
	def _check_keyup_events(self,event)	:
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False	
					#move ship to left
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
	def _update_bullets(self):
		'''updatw bullet position and remove old ones'''
		#update bullet position
		self.bullets.update()
		#get rid of bullets that disappear
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <=0:
				self.bullets.remove(bullet)
			#print(len(self.bullets))
		self._check_bullet_alien_collisions()
	def _check_bullet_alien_collisions(self):
		collisions = pygame.sprite.groupcollide(self.bullets,
		                                        self.aliens, True, True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)                                       
			self.sb.prep_score()
			                                    
			self.sb.check_high_score()                                                                           
		if not self.aliens:
			#destroy existing bullets and create new fleet
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			self.stats.level +=1
			self.sb.prep_level()
	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullet_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
	def _create_alien(self,x_position, y_position):
		'''create an alien and place it in a row'''
		new_alien = Alien(self)
		new_alien.x = x_position
		new_alien.rect.x = x_position
		new_alien.rect.y = y_position
		self.aliens.add(new_alien)
	def _create_fleet(self):
		'''create a fleet of alien'''
		alien = Alien(self)
		alien_width , alien_height = alien.rect.size
		current_x , current_y = alien_width, alien_height
		while current_y <(self.settings.screen_height - 3*alien_height):
			while current_x <(self.settings.screen_width - 2*alien_width):
				self._create_alien(current_x, current_y)
				current_x += 2 *alien_width
			#finished a row, reset x value and increment y value
			current_y += 2*alien_height
			current_x = alien_width
	def _update_aliens(self):
		''' update position of aliens'''
		self._check_fleet_edges()
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			print('ship hit')
			self._ship_hit()
			self._alien_hit_bottom()
	def _ship_hit(self):
		'''respond to alien ship collisions'''
		if self.stats.ships_left > 0:
			#decrement ships left
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			#get rid of remaining belltets and aliens
			self.bullets.empty()
			self.aliens.empty()
			#create new fleet and centre ship
			self._create_fleet()
			self.ship.center_ship()
			#pause
			sleep(0.5) #this will happen before screen is updated so the 
					   #player will see the ship is hit and then the changes in above lines of code will be visible
		else:
			self.game_active = False
	def _alien_hit_bottom(self):
		'''check if alien hit boottom of screen'''
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= self.settings.screen_height:
				self._ship_hit()
				break
	def _check_fleet_edges(self):
		''' '''
		for alien in self.aliens.sprites() :
			if alien.check_edges():
				self._change_fleet_direction()
				break
	def _change_fleet_direction(self):
		for alien in self.aliens.sprites():		
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *=-1									
	def _update_screen(self):
		#redraw screen after every  loop
		self.screen.fill(self.settings.bg_color)
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.ship.blitme()
		self.aliens.draw(self.screen)
		#draw score info
		self.sb.show_score()
		#draw play button if game is inactive
		if not self.game_active:
			self.play_button.draw_button()
		#make recently drawn screen visible
		pygame.display.flip()
		self.clock.tick(60)
	
if __name__ == '__main__' :
	#make game instance and run the game
	ai = AlienInvasion()
	ai.run_game()
