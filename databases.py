from model import Base, Users, Recipes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_recipe(r_name, cook_name, ingredients, instructions, pic, rank_sum, rank_count):
	recipe_object = Recipes(
		r_name = r_name,
		cook_name = cook_name,
 		ingredients = ingredients,
		instructions = instructions,
		pic = pic,
		rank_sum = rank_sum,
		rank_count = rank_count,
		average_rank = "No rank yet!")
	session.add(recipe_object)
	session.commit()


def edit_rank(id, new_rank_sum, new_rank_count):
	recipe_object = session.query(Recipes).filter_by(id = id).first()
	recipe_object.rank_sum = new_rank_sum
	recipe_object.rank_count = new_rank_count
	recipe_object.average_rank = str(round(new_rank_sum / new_rank_count, 1))
	session.commit()
	return

def del_recipe(id):
	session.query(Recipes).filter_by(id = id).delete()
	session.commit()

def return_all_recipes():
	recipes = session.query(Recipes).all()
	return recipes

def return_recipe(id):
	recipe = session.query(Recipes).filter_by(id = id).first()
	return recipe
###################################################################################################

def add_user(username, password):
	user_object = Users(
	username = username,
	password = password)
	session.add(user_object)
	session.commit()

def del_user(id):
	session.query(Users).filter_by(id = id).delete()
	session.commit()

def return_all_users():
	users = session.query(Users).all()
	return users

def return_user(id):
	user = session.query(Users).filter_by(id = id).first()
	return user

def edit_user(id, username, password):
	user_object = session.query(Users).filter_by(id = id).first()
	user_object.username = username
	user_object.password= password
	session.commit()
	return










