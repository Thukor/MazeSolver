from image_processing import *

"""
Processor Class for images
"""


class ImageProcessor:

	#initialize strategies
	def __init__(self,strategies):
		self.strategies = [birdseye_correction, image_segmentation]
	
	#We interpret each set of processing functions as strategies.
	def process_image(image_name, number):
		birdseye_correction(image_name, number)
		image_segmentation("warped.png", number)
