from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from flask_login import UserMixin
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, RadioField, DateField, TimeField, FloatField
from wtforms.widgets import TextArea

import helpers_constants

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=15)], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


class RegisterForm(FlaskForm):
    access = SelectField('Access Level', choices=[(1, 'user'), (2, 'admin')], coerce=int)
    username = StringField('First Name', validators=[InputRequired(), Length(min=3, max=15)], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


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


class ScriptureDailyForm(FlaskForm):
    choose_kid = SelectField('Name', choices=[('choose', 'Choose...'), ('Calvin', 'Calvin'), ('Samuel', 'Samuel'), ('Kay', 'Kay'), ('Seth', 'Seth')], validators=[InputRequired()], id='choose_kid', render_kw={'onchange': 'focus_to_date()'})
    date = DateField('Date', validators=[InputRequired()], id='date')
    start_book = StringField('Start Book', validators=[InputRequired()], id='start_book', render_kw={'onchange': 'update_end_book()'})
    start_chapter = IntegerField('Start Chapter', validators=[InputRequired()], id='start_chapter', render_kw={'onchange': 'update_end_chapter()'})
    start_verse = IntegerField('Start Verse', validators=[InputRequired()], id='start_verse')
    end_book = StringField('End Book', validators=[InputRequired()], id='end_book')
    end_chapter = IntegerField('End Chapter', validators=[InputRequired()], id='end_chapter')
    end_verse = IntegerField('End Verse', validators=[InputRequired()], id='end_verse')
    comment = StringField('Comment', validators=[InputRequired()], widget=TextArea(), id='comment')


class CreditDebit(FlaskForm):
    choose_kid = SelectField('Name', choices=[('choose', 'Choose...'), ('Calvin', 'Calvin'), ('Samuel', 'Samuel'), ('Kay', 'Kay'), ('Seth', 'Seth')], validators=[InputRequired()], id='choose_kid')
    credit_debit = SelectField('Transaction Type', choices=[('choose', 'Choose...'), ('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], validators=[InputRequired()], id='credit_debit')
    amount = FloatField('Amount', validators=[InputRequired()], id='amount')
    description = StringField('Description', validators=[InputRequired()], widget=TextArea(), id='description')


class User(UserMixin):
    def __init__(self, username, access=helpers_constants.ACCESS['user']):
        self.username = username
        self.access = access

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def allowed(self, access_level):
        print(self.access)
        print(access_level)
        return self.access >= access_level

