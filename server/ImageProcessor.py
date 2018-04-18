from image_processing import *

class ImageProcessor:

	def __init__(self,strategies):
		self.strategies = [birdseye_correction, image_segmentation]

	def process_image(image_name, number):
		birdseye_correct(image, number)
		image_segmentation("warped" + str(number) + ".png")