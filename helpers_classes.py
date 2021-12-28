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
    scripture_ass = StringField('Reading Assignment', validators=[InputRequired()], id='scripture_ass')

    # discussion_ref = StringField('Reference', validators=[InputRequired()], id='discussion_ref')
    # discussion_question = StringField('Question', validators=[InputRequired()], widget=TextArea(), id='discussion_question')

    mon_job_cal = StringField('Monday', validators=[InputRequired()], id='mon_job_cal')
    tue_job_cal = StringField('Tuesday', validators=[InputRequired()], id='tue_job_cal')
    wed_job_cal = StringField('Wednesday', validators=[InputRequired()], id='wed_job_cal')
    thu_job_cal = StringField('Thursday', validators=[InputRequired()], id='thu_job_cal')
    fri_job_cal = StringField('Friday', validators=[InputRequired()], id='fri_job_cal')
    sat_job_cal = StringField('Saturday', validators=[InputRequired()], id='sat_job_cal')
    mon_job_sam = StringField('Monday', validators=[InputRequired()], id='mon_job_sam')
    tue_job_sam = StringField('Tuesday', validators=[InputRequired()], id='tue_job_sam')
    wed_job_sam = StringField('Wednesday', validators=[InputRequired()], id='wed_job_sam')
    thu_job_sam = StringField('Thursday', validators=[InputRequired()], id='thu_job_sam')
    fri_job_sam = StringField('Friday', validators=[InputRequired()], id='fri_job_sam')
    sat_job_sam = StringField('Saturday', validators=[InputRequired()], id='sat_job_sam')
    mon_job_kay = StringField('Monday', validators=[InputRequired()], id='mon_job_kay')
    tue_job_kay = StringField('Tuesday', validators=[InputRequired()], id='tue_job_kay')
    wed_job_kay = StringField('Wednesday', validators=[InputRequired()], id='wed_job_kay')
    thu_job_kay = StringField('Thursday', validators=[InputRequired()], id='thu_job_kay')
    fri_job_kay = StringField('Friday', validators=[InputRequired()], id='fri_job_kay')
    sat_job_kay = StringField('Saturday', validators=[InputRequired()], id='sat_job_kay')
    mon_job_seth = StringField('Monday', validators=[InputRequired()], id='mon_job_seth')
    tue_job_seth = StringField('Tuesday', validators=[InputRequired()], id='tue_job_seth')
    wed_job_seth = StringField('Wednesday', validators=[InputRequired()], id='wed_job_seth')
    thu_job_seth = StringField('Thursday', validators=[InputRequired()], id='thu_job_seth')
    fri_job_seth = StringField('Friday', validators=[InputRequired()], id='fri_job_seth')
    sat_job_seth = StringField('Saturday', validators=[InputRequired()], id='sat_job_seth')

    cal_goal = StringField('Calvin', validators=[InputRequired()], id='calvin_goal1')
    sam_goal = StringField('Samuel', validators=[InputRequired()], id='samuel_goal1')
    kay_goal = StringField('Kay', validators=[InputRequired()], id='kay_goal1')
    seth_goal = StringField('Seth', validators=[InputRequired()], id='seth_goal1')

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

