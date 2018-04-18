from image_processing import *

class ImageProcessor:

	def __init__(self,strategies):
		self.strategies = [birdseye_correction, image_segmentation]

	def process_image(image_name):
		number = 5
		birdseye_correct(image, number)
		image_segmentation(f"warped{number}.png")