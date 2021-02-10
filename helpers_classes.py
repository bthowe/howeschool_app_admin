from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from flask_login import UserMixin
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, RadioField, DateField, TimeField, FloatField
from wtforms.widgets import TextArea

import helpers_constants

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=15)], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    # remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    # access = SelectField('Access Level', choices=[(0, 'guest'), (1, 'user'), (2, 'admin')], coerce=int)
    access = SelectField('Access Level', choices=[(1, 'user'), (2, 'admin')], coerce=int)
    username = StringField('First Name', validators=[InputRequired(), Length(min=3, max=15)], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class VocabForm(FlaskForm):
    practice_type = RadioField('What do you want to do?', choices=[('practice', 'Practice'), ('quiz', 'Quiz')], default='practice')
    prompt_type = RadioField('Prompt Type:', choices=[('word', 'Word'), ('def', 'Definition/Sentence')], default='word')
    lesson_num = IntegerField('Lesson Number:', validators=[InputRequired()])

class WeeklyForm(FlaskForm):
    weekof = DateField('For the week beginning on', validators=[InputRequired()], id='date')
    scripture_ref = StringField('Reference', validators=[InputRequired()], id='scripture_ref')
    scripture = StringField('Text', validators=[InputRequired()], widget=TextArea(), id='scripture')
    discussion_ref = StringField('Reference', validators=[InputRequired()], id='discussion_ref')
    discussion_question = StringField('Question', validators=[InputRequired()], widget=TextArea(), id='discussion_question')
    mon_job = StringField('Monday', validators=[InputRequired()], id='mon_job')
    tue_job = StringField('Tuesday', validators=[InputRequired()], id='tue_job')
    wed_job = StringField('Wednesday', validators=[InputRequired()], id='wed_job')
    thu_job = StringField('Thursday', validators=[InputRequired()], id='thu_job')
    fri_job = StringField('Friday', validators=[InputRequired()], id='fri_job')
    sat_job = StringField('Saturday', validators=[InputRequired()], id='sat_job')
    cal_goal1 = StringField('Calvin', validators=[InputRequired()], id='calvin_goal1')
    sam_goal1 = StringField('Samuel', validators=[InputRequired()], id='samuel_goal1')
    kay_goal1 = StringField('Kay', validators=[InputRequired()], id='kay_goal1')
    seth_goal1 = StringField('Seth', validators=[InputRequired()], id='seth_goal1')
    cal_book = StringField('Calvin', validators=[InputRequired()], id='calvin_book')
    sam_book = StringField('Samuel', validators=[InputRequired()], id='samuel_book')
    kay_book = StringField('Kay', validators=[InputRequired()], id='kay_book')
    seth_book = StringField('Seth', validators=[InputRequired()], id='seth_book')


class MathDailyForm(FlaskForm):
    choose_kid = SelectField('Name', choices=[('choose', 'Choose...'), ('calvin', 'Calvin'), ('samuel', 'Samuel'), ('kay', 'Kay')], validators=[InputRequired()], id='choose_kid')
    choose_book = SelectField('Name', choices=[('choose', 'Choose...'), ('Math_5_4', 'Math 5/4'), ('Math_6_5', 'Math 6/5'), ('Math_7_6', 'Math 7/6'), ('Math_8_7', 'Math 8/7'), ('Algebra_1_2', 'Algebra 1/2'), ('Algebra_1', 'Algebra 1'), ('Algebra_2', 'Algebra 2'), ('Advanced_math', 'Advanced Math'), ('Calculus', 'Calculus')], validators=[InputRequired()], id='choose_book')
    test = BooleanField('Test')
    start_chapter = IntegerField('Start Chapter', validators=[InputRequired()], id='start_chapter')
    start_problem = StringField('First Problem', validators=[InputRequired()], id='start_problem')
    end_chapter = IntegerField('End Chapter', validators=[InputRequired()], id='end_chapter')
    end_problem = StringField('Last Problem', validators=[InputRequired()], id='end_problem')
    date = DateField('Date', validators=[InputRequired()], id='date')
    start_time = TimeField('Start Time', validators=[InputRequired()], id='start_time', render_kw={"placeholder": "hh:mm"})
    end_time = TimeField('Stop Time', validators=[InputRequired()], id='end_time', render_kw={"placeholder": "hh:mm"})

class ScriptureDailyForm(FlaskForm):
    choose_kid = SelectField('Name', choices=[('choose', 'Choose...'), ('Calvin', 'Calvin'), ('Samuel', 'Samuel'), ('Kay', 'Kay')], validators=[InputRequired()], id='choose_kid', render_kw={'onchange': 'focus_to_date()'})
    date = DateField('Date', validators=[InputRequired()], id='date')
    start_book = StringField('Start Book', validators=[InputRequired()], id='start_book')
    start_chapter = IntegerField('Start Chapter', validators=[InputRequired()], id='start_chapter')
    start_verse = IntegerField('Start Verse', validators=[InputRequired()], id='start_verse')
    end_book = StringField('End Book', validators=[InputRequired()], id='end_book')
    end_chapter = IntegerField('End Chapter', validators=[InputRequired()], id='end_chapter')
    end_verse = IntegerField('End Verse', validators=[InputRequired()], id='end_verse')
    comment = StringField('Comment', validators=[InputRequired()], widget=TextArea(), id='comment')

class NewBookInformation(FlaskForm):
    title = StringField('Title', validators=[InputRequired()], id='title')  #, render_kw={'placeholder': 'Title'})
    author = StringField('Author', validators=[InputRequired()], id='author', render_kw={'placeholder': 'Last, First'})
    # title = StringField('Title', validators=[InputRequired()], widget=TextArea(), id='title')
    # author = StringField('Author', validators=[InputRequired()], widget=TextArea(), id='author', render_kw={'placeholder': 'Last, First'})

class CreditDebit(FlaskForm):
    choose_kid = SelectField('Name', choices=[('choose', 'Choose...'), ('Calvin', 'Calvin'), ('Samuel', 'Samuel'), ('Kay', 'Kay')], validators=[InputRequired()], id='choose_kid')
    credit_debit = SelectField('Transaction Type', choices=[('choose', 'Choose...'), ('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], validators=[InputRequired()], id='credit_debit')
    amount = FloatField('Amount', validators=[InputRequired()], id='amount')
    description = StringField('Description', validators=[InputRequired()], widget=TextArea(), id='description')

class User(UserMixin):
    def __init__(self, username, access=helpers_constants.ACCESS['user']):
        self.username = username
        self.access = access

    # def is_authenticated(self):
    #     return True

    def is_active(self):
        # Here you should write whatever the code is that checks the database if your user is active
        # return self.active
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def allowed(self, access_level):
        print(self.access)
        print(access_level)
        return self.access >= access_level

