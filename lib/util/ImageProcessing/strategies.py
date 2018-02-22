from ..decorators.imagestrategy import *

@imagestrategy
def identity(image):
	return image

class ImageProcessor:
	@staticmethod 
	def process_image(image, strategy):
		return strategy(image)