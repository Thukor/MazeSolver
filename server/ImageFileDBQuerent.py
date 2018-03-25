from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import sessionmaker
from setup_db import ImageFile, Base

class ImageFileDBQuerent:

	def __init__(self):
		engine = create_engine('sqlite:///image_files.db')
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		self.session = DBSession()

	def insert_file(self,filename):
		self.session.add(ImageFile(filename=filename))
		self.session.commit()

	def get_solution(self,solution_id):
		return self.session.query(ImageFile).filter(ImageFile.solution_id == solution_id).one().filename
		
	def get_solution_id_from_filename(self,filename):
		return self.session.query(ImageFile).filter(ImageFile.filename == filename).one().solution_id