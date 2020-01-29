from flask import Flask, request, redirect, url_for, render_template
from flask import session as login_session
from databases import *
from model import *
import random

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

is_logged = False
recent = []
top_recipes = []
username = ""

@app.route('/')
def home():
	return render_template("home.html")
@app.route('/log_in' , methods = ['GET', 'POST'])
def log_in():
	global is_logged, recent,username
	wrong_username_m = ""
	wrong_password_m = ""
	

	if request.method == 'POST': #checking the request type.
		username = request.form["username"]#==> get the user's info out of the html form.
		password = request.form["password"]
		all_users_list = return_all_users()

		a = return_all_users()
		for i in a:
			print(i.username)
			print(i.password)

		for user in all_users_list: #==> check if the user's info is correct. If not, it returns a message to the user.
			if user.username == username and user.password == password:
				is_logged = True #once users log in they don't have to log in again at the same time they are using the website. 
				return render_template("profile.html", username = username)

		if is_logged == False and user.username == username and user.password != password:
			wrong_password_m = "The password seems to be wrong..."
			return render_template("Log_In.html", wrong_password_m = wrong_password_m,
				wrong_username_m = wrong_username_m)

		elif is_logged == False and user.username != username and user.password == password:
			wrong_username_m = "The username seems to be wrong..."
			return render_template("Log_In.html", wrong_password_m = wrong_password_m,
				wrong_username_m = wrong_username_m)

		elif is_logged == False and user.username != username and user.password != password:
			wrong_password_m = "The password seems to be wrong..."
			wrong_username_m = "The username seems to be wrong..."
			return render_template("Log_In.html", wrong_password_m = wrong_password_m,
				wrong_username_m = wrong_username_m)
	elif is_logged: #===>checking if the user already logged in once.
		return render_template("profile.html", recent = recent, username = username)

	return render_template("Log_In.html")

@app.route('/sign_up' ,  methods = ['GET', 'POST'])
def sign_up():
	username_message = ""
	password_message = ""

	if request.method == 'POST':
		new_username = request.form["new_username"] #==> get the user's info out of the html form.
		new_password = request.form["new_password"]
		all_users_list = return_all_users()

		for user in all_users_list: #===> check if the user already exits, or if the password/username are in use.
			if user.username == new_username and user.password == new_password:
				username_message = "This username is already in use!"
				password_message = "This password is already in use!"
				return render_template("Log_In.html", username_message = username_message, 
				password_message = password_message)

			elif user.username == new_username:
				username_message = "This username is already in use!"
				return render_template("Log_In.html", username_message = username_message, 
				password_message = password_message)

			elif user.password == new_password:
				password_message = "This password is already in use!"
				return render_template("Log_In.html", username_message = username_message, 
				password_message = password_message)

		add_user(new_username, new_password) #===> if the user doesn't exist, add it to the db.

		username_message = "You are now signed up. You can log in!"
		return render_template("Log_In.html", username_message = username_message, 
		password_message = password_message)

	return render_template("Log_In.html", username_message = username_message, 
		password_message = password_message)

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/recipe', methods = ['POST'])
def recipe():
	message = ""
	recipe_id = request.form["recipe_id"]
	recipe_object = return_recipe(recipe_id)
	return render_template("recipe.html", recipe_object = recipe_object, message = message)

@app.route('/recipes')
def recipes():
	global top_recipes
	all_recipes = return_all_recipes()
	for recipe in all_recipes:
		if recipe.average_rank != "No rank yet!" and recipe not in top_recipes:
			if float(recipe.average_rank) >= 4.5:
				top_recipes.append(recipe)
	return render_template("recipes.html" , top_recipes = top_recipes)

@app.route('/recipe_rate', methods = ['POST'])
def recipe_rate():
	global is_logged, recent
	message = ""
	recipe_id = request.form["recipe_object_id"]
	recipe_object = return_recipe(recipe_id)
	recent.append(recipe_object)

	if is_logged:
		user_rank = float(request.form["rating"])
		new_rank_sum = recipe_object.rank_sum + user_rank
		new_rank_count = recipe_object.rank_count + 1
		edit_rank(recipe_id, new_rank_sum, new_rank_count)


		all_recipes = return_all_recipes()
		for recipe in all_recipes:
			if recipe.average_rank != "No rank yet!" and recipe not in top_recipes:
				if float(recipe.average_rank) >= 4.5:
					top_recipes.append(recipe)

		return render_template("recipe.html", recipe_object = recipe_object, message = message)
	message = "Log in first!"
	return render_template("recipe.html", recipe_object = recipe_object, message = message)

@app.route('/all_recipes', methods = ['GET', 'POST'])
def all_recipes():
	recipes_list = return_all_recipes()
	search_m = ""
	if request.method == 'POST':
		search = request.form["search"]
		results = []
		for recipe in recipes_list:
			if recipe.r_name == search or search[0:3] in recipe.r_name:
				results.append(recipe)
		if len(results) == 0:
			search_m = "Sorry, nothing matched your search!"
		return render_template("all_recipes.html", recipes_list = results, search_m = search_m)
	return render_template("all_recipes.html", recipes_list = recipes_list, search_m = search_m)

@app.route('/share_your_recipe' , methods = ['GET' , 'POST'])
def share_your_recipe():
	if request.method == 'POST':
		rank_count = 0
		rank_sum = 0
		recipe_name = request.form["recipe_name"] 
		cook_name = request.form["cook_name"]
		ingredients = str(request.form["ingredients"])
		instructions = str(request.form["instructions"])
		pic = "../static/" + request.form["pic"]
		add_recipe(recipe_name, cook_name, ingredients, instructions, pic, rank_sum, rank_count)
		return render_template("after_sharing.html")
	return render_template("share_your_recipe.html")


if __name__ == '__main__':
	app.run(debug=True)