from image_processing import *

class ImageProcessor:

	def __init__(self,strategies):
		self.strategies = [birdseye_correction, image_segmentation]

	def process_image(image_name, number):
		birdseye_correction(image_name, number)
		image_segmentation("warped.png", number)