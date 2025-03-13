class Settings:
	'''to store all settings of game'''
	def __init__(self):
		#screen settings
		self.bg_color = (230,230,230)
		self.screen_width = 1200
		self.screen_height = 600
		self.ship_speed = 5 #ship speed
		self.ship_limit = 3
		#bullet settings
		self.bullet_speed = 50
		self.bullet_height= 3
		self.bullet_width = 15 #15 
		self.bullet_color = (60,60,60)
		self.bullet_allowed = 10
		
		#alien settings
		self.alien_speed = 10
		self.fleet_drop_speed = 10
		#fleet diection 1 = left, -1 = right
		self.fleet_direction = 1
		#how quickly game speeds up
		self.speedup_scale = 1.2
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		'''initialize settings that change througtout the game'''
		self.ship_speed = 1.5
		self.bullet_speed = 2.5
		self.alien_speed = 1
		self.fleet_direction = 1
		#alien points
		self.alien_points = 50
		
	def increase_speed(self):
		self.ship_speed *=   self.speedup_scale
		self.alien_speed *=  self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
