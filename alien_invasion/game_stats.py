class GameStats:
	''' track stats of game'''
	def __init__(self, ai_game):
		'''initialize stats'''
		self.settings = ai_game.settings
		self.reset_stats()
		self.high_score = 0
	def reset_stats(self):
		'''initialize stats that will change during game'''
		self.ships_left = self.settings.ship_limit
		#stores initial score
		self.score = 0
		self.level = 1
