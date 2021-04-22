from flask import Flask, render_template, redirect, abort, request
from forms.user import RegisterForm
from forms.loginform import LoginForm
from forms.recipesform import RecipesForm
from data import db_session
from data.users import User
from data.recipes import Recipes
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader


def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init('db/recipes.db')
    db_sess = db_session.create_session()
            
            
    @app.route("/")
    def index():
        len_data = len([x for x in db_sess.query(Recipes).all()])
        data = db_sess.query(Recipes).order_by(Recipes.coeff_popular)[::-1]
        val_1 = db_sess.query(Recipes).order_by(Recipes.coeff_popular)[::-1][0]
        return render_template("index.html", data=data, len_data=len_data, val_1=val_1)
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)
    
    
    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                age=form.age.data,
                birth=form.birth.data,
                email=form.email.data,
                city_from=form.city_from.data
            )
            user.set_password(form.password.data)
            
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)
    
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")
    
    
    @app.route('/add_recipes',  methods=['GET', 'POST'])
    @login_required
    def add_recipes():
        form = RecipesForm()
        if form.validate_on_submit():
            file_b = form.photo.data
            db_sess = db_session.create_session()
            rec = Recipes()
            rec.name_recipe = form.title.data
            rec.cooking_time = form.cooking_time.data
            rec.ingredients = form.ingredients.data
            rec.category = form.category.data
            rec.food = form.food.data
            rec.about = form.about.data
            name_file = (str(current_user.id) +
                         str(random.randint(1, 10000000)) + str(random.randint(1, 10000000)) +
                         str(random.randint(1, 10000000)) + '.png')
            name = r'static/img_rec/' + name_file
            with open(name, 'wb') as file:
                file.write(file_b.read())
                
            rec.name_photo = name_file
            current_user.rec.append(rec)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('recipes.html', title='Добавление рецепта', 
                               form=form)
    
    
    @app.route('/recipes_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def rec_delete(id):
        db_sess = db_session.create_session()
        if current_user.id != 1:
            rec = db_sess.query(Recipes).filter(Recipes.id == id,
                                              Recipes.user == current_user
                                              ).first()
        if current_user.id == 1:
            rec = db_sess.query(Recipes).filter(Recipes.id == id,
                                              ).first()
        if rec:
            db_sess.delete(rec)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')
    
    
    @app.route('/show/<int:id>', methods=['GET', 'POST'])
    def show(id):
        db_sess = db_session.create_session()
        rec = db_sess.query(Recipes).filter(Recipes.id == id,
                                                  ).first()
        user = db_sess.query(User).filter(Recipes.id == id,
                                          Recipes.personal_id == User.id,
                                                  ).first()
        if rec:
            rec.coeff_popular = rec.coeff_popular + 1
            db_sess.commit()
            return render_template('show.html', title='Полная информация о рецепте',
                                   cook=rec.food,
                                   time=rec.cooking_time,
                                   name=user.name,
                                   surname=user.surname,
                                   name_recipe=rec.name_recipe,
                                   ingredients=rec.ingredients)
        else:
            abort(404)
        return redirect('/')
    
    
    @app.route('/edit_recipes/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_rec(id):
        form = RecipesForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            if current_user.id != 1:
                rec = db_sess.query(Recipes).filter(Recipes.id == id,
                                                  Recipes.user == current_user
                                                  ).first()
            if current_user.id == 1:
                rec = db_sess.query(Recipes).filter(Recipes.id == id
                                                  ).first()
            if rec:
                form.title.data = rec.name_recipe
                form.cooking_time.data = rec.cooking_time
                form.ingredients.data = rec.ingredients
                form.category.data = rec.category
                form.about.data = rec.about
                form.food.data = rec.food
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            rec = db_sess.query(Recipes).filter(Recipes.id == id,
                                              Recipes.user == current_user
                                              ).first()
            if current_user.id == 1:
                rec = db_sess.query(Recipes).filter(Recipes.id == id
                                                  ).first()
            if rec:
                file_b = form.photo.data
                rec.name_recipe = form.title.data
                rec.cooking_time = form.cooking_time.data
                rec.ingredients = form.ingredients.data
                rec.category = form.category.data
                rec.food = form.food.data
                rec.about = form.about.data
                name_file = (str(current_user.id) +
                             str(random.randint(1, 10000000)) + str(random.randint(1, 10000000)) +
                             str(random.randint(1, 10000000)) + '.png')
                name = r'static/img_rec/' + name_file
                with open(name, 'wb') as file:
                    file.write(file_b.read())
                
                rec.name_photo = name_file
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('recipes.html',
                               title='Редактирование рецепта',
                               form=form
                               )
    
    
if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')