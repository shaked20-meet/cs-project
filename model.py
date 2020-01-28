from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key = True)
	username = Column(String)
	password = Column(String)

class Recipes(Base):
	__tablename__ = 'recipes'
	id = Column(Integer, primary_key = True)
	r_name = Column(String)
	cook_name = Column(String)
	ingredients = Column(String)
	instructions = Column(String)
	pic = Column(String)
	rank_sum = Column(Integer)
	rank_count = Column(Integer)
	average_rank = Column(String)
