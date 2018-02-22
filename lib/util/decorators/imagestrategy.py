STRATEGIES = []

def imagestrategy(processing_function):
	STRATEGIES.append(processing_function)
	def process_image(image):
		return processing_function(image)

