from flask import Blueprint, render_template, session, current_app, request, redirect, url_for, flash, jsonify, abort
from flask_login import current_user
from .auth import login_required
from functools import wraps
from werkzeug.utils import secure_filename
from .models import Recipe, Tag, favorites, recipe_tags 
from .database import db
import os
import uuid
from sqlalchemy import or_, func, desc
import random

def save_address(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session['last_page'] = request.url
        #print(session['last_page'])
        return f(*args, **kwargs)
    return decorated_function

views = Blueprint('views', __name__)

#root
@views.route('/') 
def home():
    all_recipes = Recipe.query.all() 
    random_recipes = random.sample(all_recipes, min(len(all_recipes), 6)) 
    return render_template("home.html", recipes=random_recipes, session=session)

@views.route('/about') 
def about(): 
    return render_template("about.html", session=session)

@views.route('/contact') 
def contact(): 
    return render_template("contact.html", session=session)


@views.route('/profile')  
@login_required
def profile(): 
    return render_template("profile.html", session=session)

@views.route('/toggle_favorite', methods=['POST'])
@login_required
def toggle_favorite():
    recipe_id = request.form.get('recipe_id')
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify(success=False), 404
    assoc = db.session.query(favorites).filter_by(user_id=current_user.id, recipe_id=recipe.id).first()

    if assoc:
        current_user.favorites.remove(recipe)
        favorited = False
    else:
        current_user.favorites.append(recipe)
        favorited = True

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e)), 500

    return jsonify(success=True, favorited=favorited)

@views.route('/browse', methods=['GET', 'POST'])
def browse(): 
    if request.method == 'POST':
        if 'toggle_favorite' in request.form:
            recipe_id = request.form.get('toggle_favorite')
            recipe = Recipe.query.get(recipe_id)
            if recipe:
                if current_user.favorites.filter_by(id=recipe.id).first():
                    current_user.favorites.remove(recipe)
                else:
                    current_user.favorites.append(recipe)
                db.session.commit()
            page = request.form.get('page', 1)
            return redirect(url_for('views.browse', page=page))
            
        if 'search' in request.form:
            search_query = request.form.get('search', '').strip()
            if search_query:
                return redirect(url_for('views.browse', search=search_query, page=1))

    page = request.args.get('page', 1, type=int)
    per_page = 4
    search_query = request.args.get('search', '').strip()
    
    query = Recipe.query
    
    if search_query:
        search_terms = search_query.lower().split()
        
        conditions = []
        
        for term in search_terms:
            conditions.append(Recipe.title.ilike(f'%{term}%'))
        
        tag_conditions = []
        for term in search_terms:
            tag_conditions.append(Tag.name.ilike(f'%{term}%'))
        
        if tag_conditions:
            tag_query = Recipe.query.join(recipe_tags).join(Tag).filter(or_(*tag_conditions))
            query = query.filter(or_(or_(*conditions), Recipe.id.in_([r.id for r in tag_query])))
        else:
            query = query.filter(or_(*conditions))
        
        query = query.order_by(Recipe.title)
    
    paginated_recipes = query.paginate(page=page, per_page=per_page, error_out=False)
    
    recipes = paginated_recipes.items
    next_page = paginated_recipes.next_num if paginated_recipes.has_next else None
    prev_page = paginated_recipes.prev_num if paginated_recipes.has_prev else None

    favorites_ids = []
    if current_user.is_authenticated:
        favorites_ids = [recipe.id for recipe in current_user.favorites.all()]
    
    return render_template('browse.html', recipes=recipes, favorites_ids=favorites_ids,  next_page=next_page, prev_page=prev_page, search_query=search_query)


@views.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites_view(): 
    if request.method == 'POST':
        if 'toggle_favorite' in request.form:
            recipe_id = request.form.get('toggle_favorite')
            recipe = Recipe.query.get(recipe_id)
            if recipe:
                if current_user.favorites.filter_by(id=recipe.id).first():
                    current_user.favorites.remove(recipe)
                else:
                    current_user.favorites.append(recipe)
                db.session.commit()
            page = request.form.get('page', 1)
            return redirect(url_for('views.favorites_view', page=page))

    page = request.args.get('page', 1, type=int)
    per_page = 4

    paginated_recipes = current_user.favorites.paginate(page=page, per_page=per_page, error_out=False)
    recipes = paginated_recipes.items
    next_page = paginated_recipes.next_num if paginated_recipes.has_next else None
    prev_page = paginated_recipes.prev_num if paginated_recipes.has_prev else None

    favorites_ids = [recipe.id for recipe in current_user.favorites.all()]
    
    return render_template('favorites.html', recipes=recipes, favorites_ids=favorites_ids, next_page=next_page, prev_page=prev_page)


@views.route('/my-recipes', methods=['GET', 'POST'])
@login_required
def my_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = 4

    paginated_recipes = Recipe.query.filter_by(user_id=current_user.id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    recipes = paginated_recipes.items
    next_page = paginated_recipes.next_num if paginated_recipes.has_next else None
    prev_page = paginated_recipes.prev_num if paginated_recipes.has_prev else None
    
    return render_template('my_recipes.html', recipes=recipes, next_page=next_page, prev_page=prev_page)


@views.route('/recipe/<recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        abort(404)
    
    favorites_ids = []
    if current_user.is_authenticated:
        favorites_ids = [favorite.id for favorite in current_user.favorites]
    
    return render_template('recipe_detail.html', recipe=recipe, favorites_ids=favorites_ids)


@views.route('/create-recipe', methods=['GET', 'POST']) 
@login_required
def create_recipe():
    if request.method == 'POST':
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        current_app.config['UPLOAD_FOLDER'] = upload_folder
        os.makedirs(upload_folder, exist_ok=True)


        title = request.form.get('title')
        tags_input = request.form.get('tags') or ""
        cooking_time = request.form.get('cooking_time')
        difficulty = request.form.get('difficulty')
        instructions = request.form.get('instructions')
        
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
            image_filename = 'uploads/' + image_filename
        else:
            image_filename = 'images/default_recipe_image.jpg'


        new_recipe = Recipe(
            title=title,
            cooking_time=cooking_time,
            difficulty=int(difficulty),
            instructions=instructions,
            image=image_filename,
            rating=0,
            user=current_user
        )

        tag_names = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(id=str(uuid.uuid4()), name=name)
                db.session.add(tag)
            new_recipe.tags.append(tag)

        db.session.add(new_recipe)
        db.session.commit()
        flash("Recipe created successfully!", category="success")
        return redirect(url_for('views.my_recipes'))
    
    return render_template('create_recipe.html')



@views.route('/recipe/<recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    
    if not recipe or recipe.user_id != current_user.id:
        return jsonify(success=False, message="Recipe not found or not authorized"), 404
    
    try:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify(success=True), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 500


@views.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    
    if not recipe or recipe.user_id != current_user.id:
        flash("Recipe not found or you don't have permission to edit it.", category="error")
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        current_app.config['UPLOAD_FOLDER'] = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

        title = request.form.get('title')
        tags_input = request.form.get('tags') or ""
        cooking_time = request.form.get('cooking_time')
        difficulty = request.form.get('difficulty')
        instructions = request.form.get('instructions')
        
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
            image_filename = 'uploads/' + image_filename
            recipe.image = image_filename
        
        recipe.title = title
        recipe.cooking_time = cooking_time
        recipe.difficulty = int(difficulty)
        recipe.instructions = instructions
        
        recipe.tags.clear()
        tag_names = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(id=str(uuid.uuid4()), name=name)
                db.session.add(tag)
            recipe.tags.append(tag)

        db.session.commit()
        flash("Recipe updated successfully!", category="success")
        return redirect(url_for('views.recipe_detail', recipe_id=recipe.id))
    
    tags = ','.join([tag.name for tag in recipe.tags])
    return render_template('edit_recipe.html', recipe=recipe, tags=tags)


