import os
import os.path
import json
import datetime
import subprocess
import pandas as pd
from flask_pymongo import PyMongo
from collections import defaultdict
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import helpers_classes
import helpers_constants
import helpers_functions

# mongod --dbpath ~/path/to/your/app/data

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


app = Flask(__name__)
app.secret_key = 'mysecret'
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db_users = PyMongo(app, uri="mongodb://localhost:27017/users")
db_script = PyMongo(app, uri="mongodb://localhost:27017/scripture_commentary")
db_forms = PyMongo(app, uri="mongodb://localhost:27017/forms")
db_bank = PyMongo(app, uri="mongodb://localhost:27017/banking")
db_books = PyMongo(app, uri="mongodb://localhost:27017/books")


@login_manager.user_loader
def load_user(username):
    u = db_users.db.users.find_one({'name': username})
    if not u:
        return None
    return helpers_classes.User(u['name'], u['access'])


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = helpers_classes.LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('scripture_commentary'))
    if request.method == 'POST' and form.validate_on_submit():
        user = db_users.db.users.find_one({'name': form.username.data})
        if user:
            if form.password.data == user['password']:
            # if check_password_hash(form.password.data, login_user['password']):

                user_obj = helpers_classes.User(user['name'], user['access'])
                login_user(user_obj)
                return redirect(url_for('scripture_commentary'))

        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    form = helpers_classes.RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        users = db_users.db.users
        existing_user = users.find_one({'name': form.username.data})

        if existing_user is None:
            # hashpass = generate_password_hash(form.password.data, method='sha256')  # add this in place of the password below
            users.insert({'name': form.username.data, 'password': form.password.data, 'access': form.access.data})

            flash('Registration was successful!')
            return redirect(url_for('register'))

        flash('That username already exists!')
    return render_template('register.html', form=form, page_name='Register Child')


@app.route("/scripture_commentary", methods=['POST', 'GET'])
@login_required
def scripture_commentary():
    form = helpers_classes.ScriptureDailyForm()
    if request.method == 'POST':  # and form.validate_on_submit():
        tab = db_script.db[form.choose_kid.data]
        for comment in form.comment.data.split('\r'):
            data = helpers_functions.scripture_data_json(form, comment)
            ret = tab.insert_one(data)
            print('data inserted: {}'.format(ret))
        return redirect(url_for('scripture_commentary'))
    return render_template('scripture_commentary.html', form=form, page_name='Scripture Commentary')


@app.route("/weekly_forms_create", methods=['POST', 'GET'])
@login_required
def weekly_forms_create():
    today = datetime.date.today()
    date_shift = 6 - today.weekday()  # Monday is 0
    date = str(today + datetime.timedelta(date_shift))
    output = {k: v for k, v in list(db_forms.db.Weekly.find())[-1].items() if k != '_id'}

    form = helpers_classes.WeeklyForm()
    if request.method == 'POST':
        data_weekly = helpers_functions.weekly_data_json(form)
        ret_weekly = db_forms.db['Weekly'].insert_one(data_weekly)
        print('Weekly data inserted: {}'.format(ret_weekly))

        scripture_dict = {
            'assignment': form.scripture_ass.data,
            'reference': form.scripture_ref.data,
            'scripture': form.scripture.data
        }
        kids_dict = {
            'Calvin': {
                'book': form.cal_book.data,
                'goal': form.cal_goal.data,
                'jobs': ['vacuum stairs #1', 'vacuum stairs #2', "vacuum parent's\nroom, closet, and\nhallway", 'vacuum stairs #1', 'vacuum stairs #2', "vacuum parent's\nroom, closet, and\nhallway"]
            },
            'Samuel': {
                'book': form.sam_book.data,
                'goal': form.sam_goal.data,
                'jobs': ['toilet', 'garbage, mirror,\npaper towels,\nlight switches\ndoor knobs', 'sink, handsoap\nhand towel', 'vacuum room', 'fold laundry', 'other bathrooms']
            },
            'Kay': {
                'book': form.kay_book.data,
                'goal': form.kay_goal.data,
                'jobs': ['toilet', 'garbage, mirror,\npaper towels,\nlight switches\ndoor knobs', 'sink, handsoap\nhand towel', 'vacuum room', 'fold laundry', 'other bathrooms']
            },
            'Seth': {
                'book': form.seth_book.data,
                'goal': form.seth_goal.data,
                'jobs': ['toilet', 'garbage, mirror,\npaper towels,\nlight switches\ndoor knobs', 'sink, handsoap\nhand towel', 'vacuum room', 'fold laundry', 'other bathrooms']
            }
        }

        helpers_functions.weekly_form_pdf_create(
            [str(form.weekof.data + datetime.timedelta(days)) for days in range(0, 7)],
            scripture_dict,
            kids_dict
        )
        # helpers_functions.weekly_jobs_latex_create([form.mon_job.data, form.tue_job.data, form.wed_job.data, form.thu_job.data, form.fri_job.data, form.sat_job.data])

        # todo: jobs and scripture list and goals sheets
        # todo: make an interface that is like the time sheet and that can be manipulated
        # todo: dockerize everything.



        data_scriptures = helpers_functions.scripture_list_json(form)
        ret_scriptures = db_forms.db['Scriptures'].insert_one(data_scriptures)
        print('Scriptures data inserted: {}'.format(ret_scriptures))
        return redirect(url_for('weekly_forms_create'))
    return render_template('weekly_forms_create.html', form=form, date=date, form_data=output, page_name='Weekly Forms')


@app.route("/download_forms", methods=['GET'])
@login_required
def download_forms():
    for file in ['weekly_time_sheet.pdf', 'weekly_jobs_sheet.pdf']:
        if os.path.exists(helpers_constants.filenamer(file)):
            os.rename(helpers_constants.filenamer(file), helpers_constants.filenamer('static/' + file))

    time_stamp = str(datetime.datetime.fromtimestamp(os.path.getmtime(helpers_constants.filenamer('static/weekly_time_sheet.pdf'))).strftime('%Y-%m-%d %H:%M:%S'))
    return render_template(
        'download_forms.html',
        page_name='Download Forms',
        weekly_forms_pdf=time_stamp,
    )


@app.route("/banking_manage", methods=['POST', 'GET'])
@login_required
def banking_manage():
    form = helpers_classes.CreditDebit()
    if request.method == 'POST':  # and form.validate_on_submit():
        data = helpers_functions.credit_debit_data(form)
        tab = db_bank.db[form.choose_kid.data]
        ret = tab.insert_one(data)
        print('data inserted: {}'.format(ret))
        return redirect(url_for('banking_manage'))
    return render_template('banking_manage.html', form=form, page_name='Banking Accounts Manage')


@app.route("/banking_history")
@login_required
def banking_history():
    return render_template('banking_history.html', page_name='Banking History')


@app.route('/query_bank', methods=['POST', 'GET'])
def query_bank():
    js = json.loads(request.data.decode('utf-8'))

    sum = 0
    itemized = []
    for entry in list(db_bank.db[js['name']].find()):
        if entry['type'] == 'deposit':
            sum += entry['amount']
        else:
            sum += -entry['amount']

        itemized.append(
            {
                'type': entry['type'],
                'amount': '{0:.2f}'.format(entry['amount']),
                'description': entry['description'],
                'date': entry['date'],
                'cumulative': '{0:.2f}'.format(sum)
            }
        )
    output = {'itemized': itemized, 'total': '{0:.2f}'.format(sum)}
    return jsonify(output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
