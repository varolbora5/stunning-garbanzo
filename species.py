class Vegetob:
	def __init__(self) -> None:
		self.density = 0

	def elaborate(self):
		self.grow()

	def get_density(self):
		return self.density

	def grow(self):
		if self.density < 100:
			self.density += 1
