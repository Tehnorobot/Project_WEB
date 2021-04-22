from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class RecipesForm(FlaskForm):
    title = StringField('Название рецепта/блюда', validators=[DataRequired()])
    cooking_time = StringField('Время приготовления', validators=[DataRequired()])
    ingredients = TextAreaField('Список ингредиентов(формат: Мука, соль)', validators=[DataRequired()])
    category = StringField("Категория блюда(пример: десерт)")
    food = TextAreaField ("Процесс приготовления")
    about = TextAreaField ("Ваше описание блюда")
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Применить')