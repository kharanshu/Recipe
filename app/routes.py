from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, Recipe
from app.forms import RecipeForm, RegistrationForm, LoginForm

@app.route('/')
@app.route('/home')
def home():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('home.html', recipes=recipes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data ,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data,
                        description=form.description.data,
                        ingredients=form.ingredients.data,
                        instructions=form.instructions.data,
                        created_by=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('recipe_form.html', title='New Recipe', form=form)

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipe.title, recipe=recipe)

@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.created_by != current_user.id:
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.description.data = recipe.description
        form.ingredients.data = recipe.ingredients
        form.instructions.data = recipe.instructions
    return render_template('edit_recipe.html', title='Edit Recipe', form=form)

@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.created_by != current_user.id:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/user_recipes/<int:user_id>')
def user_recipes(user_id):
    user = User.query.get(user_id)
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return render_template('user_recipes.html', user=user, recipes=recipes)
