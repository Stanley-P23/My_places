from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, DateField, BooleanField, Label
from wtforms.validators import DataRequired, Length, Email
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed





# WTForm for creating a blog post

class AddPlaceForm(FlaskForm):

    name = StringField("1. Name the spot", validators=[DataRequired()])
    description = CKEditorField("2. Describe it", validators=[DataRequired()])
    distance = SelectField("3. How far is it from your place?", choices=[("close", "close"), ("so so", "so so"), ("far",
                                                                                                               "far")], default='close')
    type = SelectField("4. Is it indoor or outdoor?",
                           choices=[("indoor", "indoor"), ("outdoor", "outdoor")], default='indoor')
    photo = FileField("5. Upload a photo",
                      validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])


    food = BooleanField('Served food')
    my_food = BooleanField('Food in a backpack')
    table = BooleanField("There's a table")
    socket = BooleanField('Electric socket')
    work_study = BooleanField('Suitable for work/study')
    cultural = BooleanField('Culture place')
    outdoor_activity = BooleanField('Best for outdoor activity')



    submit = SubmitField("Remember")

class CreateExercisesSeriesForm(FlaskForm):

    session_no = StringField("Numer zajęć", validators=[DataRequired(), Length(1, 2)])
    title = StringField("Tytuł", validators=[DataRequired(), Length(5, 50)])
    submit = SubmitField("Stwórz serię zadań")

class CreateDateForm(FlaskForm):

    date = DateField("Termin", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Zatwierdź termin")


class CreateExerciseForm(FlaskForm):



    body = CKEditorField("Treść zadania", validators=[DataRequired()])
    value1 = CKEditorField("Odpowiedź A", validators=[DataRequired()])
    value2 = CKEditorField("Odpowiedź B", validators=[DataRequired()])
    value3 = CKEditorField("Odpowiedź C", validators=[DataRequired()])
    value4 = CKEditorField("Odpowiedź D", validators=[DataRequired()])
    correct = SelectField(u'Poprawna odpowiedź', choices=['A', 'B', 'C', 'D'])
    submit = SubmitField("Prześlij")



class CreateAnswerForm(FlaskForm):

                answer1 = SelectField('Odpowiedź', choices=['A', 'B', 'C', 'D'])
                answer2 = SelectField('Odpowiedź', choices=['A', 'B', 'C', 'D'])
                answer3 = SelectField('Odpowiedź', choices=['A', 'B', 'C', 'D'])
                answer4 = SelectField('Odpowiedź', choices=['A', 'B', 'C', 'D'])
                answer5 = SelectField('Odpowiedź', choices=['A', 'B', 'C', 'D'])
                answer6 = SelectField('Odpowiedź', choices=['A', 'B', 'C', 'D'])
                submit = SubmitField("Prześlij odpowiedzi")



# TODO: Create a RegisterForm to register new users


# TODO: Create a LoginForm to login existing users


# TODO: Create a CommentForm so users can leave comments below posts

class CreateCommentForm(FlaskForm):

    body = CKEditorField("Your comment:", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Add a comment")

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8), ])

    submit = SubmitField(label="LOG ME IN!")

class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8), ])
    confirm = PasswordField('Repeat password', validators=[DataRequired(), Length(8), ])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField(label="Register Me!")