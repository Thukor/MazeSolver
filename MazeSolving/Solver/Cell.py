from collections import namedtuple
from pprint import pformat

class Cell:

	def __init__(self, row, column, wall_value):
		self.row = row
		self.column = column
		self.wall_value = wall_value
		self.is_start = False

	def __eq__(self, other):
		return (self.row, self.column, self.wall_value) == (other.row, other.column, other.wall_value)

	def __hash__(self):
		return hash((self.row, self.column, self.wall_value))

	def __str__(self):
		return pformat({
			"north wall:": self.has_north_wall,
			"east wall:": self.has_east_wall,
			"south wall:": self.has_south_wall,
			"west wall:": self.has_west_wall,
			"coordinate:": (self.row, self.column),
			"is_valid_start:": self.is_possible_start
			})

	def __repr__(self):
		return str(self)

	@property 
	def has_north_wall(self):
		return self.wall_value % 2 == 1

	@property 
	def has_east_wall(self):
		return self.wall_value in {4,5,6,7,12,14,15}

	@property 
	def has_south_wall(self):
		return self.wall_value in {8,9,10,11,12,14,5}

	@property 
	def has_west_wall(self):
		return self.wall_value in {2,3,6,10,7,14,15}

	@property
	def is_possible_start(self):
		return self.is_start

	@is_possible_start.setter 
	def is_possible_start(self, tf):
		self.is_start = tf



