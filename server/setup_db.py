from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#Define Table
class ImageFile(Base):
	__tablename__ = 'imagefiles'

	solution_id = Column(Integer, autoincrement=True, primary_key=True)
	filename = Column(String(255))

engine = create_engine('sqlite:///image_files.db')
Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)