import os
import string
import yagmail
import datetime
import itertools
import subprocess
import numpy as np
import pandas as pd
from functools import wraps
from collections import defaultdict
from flask import url_for, redirect
from flask_login import current_user
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Line, Drawing
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak, NextPageTemplate, \
    PageTemplate, Frame

import helpers_constants


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.allowed(access_level):
                return redirect(url_for('main_menu', message="You do not have access to that page. Sorry!"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def weekly_data_json(form):
    data = {
        "week_start_date": str(form.weekof.data),

        "scripture_ass": form.scripture_ass.data,
        "scripture_ref": form.scripture_ref.data,
        "scripture": form.scripture.data,

        "mon_job_cal": form.mon_job_cal.data,
        "tue_job_cal": form.tue_job_cal.data,
        "wed_job_cal": form.wed_job_cal.data,
        "thu_job_cal": form.thu_job_cal.data,
        "fri_job_cal": form.fri_job_cal.data,
        "sat_job_cal": form.sat_job_cal.data,
        "mon_job_sam": form.mon_job_sam.data,
        "tue_job_sam": form.tue_job_sam.data,
        "wed_job_sam": form.wed_job_sam.data,
        "thu_job_sam": form.thu_job_sam.data,
        "fri_job_sam": form.fri_job_sam.data,
        "sat_job_sam": form.sat_job_sam.data,
        "mon_job_kay": form.mon_job_kay.data,
        "tue_job_kay": form.tue_job_kay.data,
        "wed_job_kay": form.wed_job_kay.data,
        "thu_job_kay": form.thu_job_kay.data,
        "fri_job_kay": form.fri_job_kay.data,
        "sat_job_kay": form.sat_job_kay.data,
        "mon_job_seth": form.mon_job_seth.data,
        "tue_job_seth": form.tue_job_seth.data,
        "wed_job_seth": form.wed_job_seth.data,
        "thu_job_seth": form.thu_job_seth.data,
        "fri_job_seth": form.fri_job_seth.data,
        "sat_job_seth": form.sat_job_seth.data,
        "mon_job_mags": form.mon_job_mags.data,
        "tue_job_mags": form.tue_job_mags.data,
        "wed_job_mags": form.wed_job_mags.data,
        "thu_job_mags": form.thu_job_mags.data,
        "fri_job_mags": form.fri_job_mags.data,
        "sat_job_mags": form.sat_job_mags.data,
        "mon_job_mar": form.mon_job_mar.data,
        "tue_job_mar": form.tue_job_mar.data,
        "wed_job_mar": form.wed_job_mar.data,
        "thu_job_mar": form.thu_job_mar.data,
        "fri_job_mar": form.fri_job_mar.data,
        "sat_job_mar": form.sat_job_mar.data,

        "calvin_goal1": form.cal_goal.data,
        "samuel_goal1": form.sam_goal.data,
        "kay_goal1": form.kay_goal.data,
        "seth_goal1": form.seth_goal.data,
        "mags_goal1": form.mags_goal.data,
        "martin_goal1": form.mar_goal.data,

        "calvin_book": form.cal_book.data,
        "samuel_book": form.sam_book.data,
        "kay_book": form.kay_book.data,
        "seth_book": form.seth_book.data,
        "mags_book": form.mags_book.data,
        "mar_book": form.mar_book.data,
    }
    return data

def scripture_data_json(form, comment):
    data = {
        "name": form.choose_kid.data,
        "date": str(form.date.data),
        "start_book": form.start_book.data,
        "start_chapter": form.start_chapter.data,
        "start_verse": form.start_verse.data,
        "end_book": form.end_book.data,
        "end_chapter": form.end_chapter.data,
        "end_verse": form.end_verse.data,
        "comment": comment.replace('\n', '')
    }
    return data

def math_num_data_json(form):
    if form.test.data:
        chapter = 'test ' + str(form.chapter.data)
    else:
        chapter = form.chapter.data
    data = {
        "book": form.choose_book.data,
        "chapter": chapter,
        "num_lesson_probs": form.num_lesson_probs.data,
        "num_mixed_probs": form.num_mixed_probs.data
    }
    return data

def credit_debit_data(form):
    data = {
        "kid": form.choose_kid.data,
        "type": form.credit_debit.data,
        "amount": form.amount.data,
        "description": form.description.data,
        "date": str(datetime.date.today())
    }
    return data

def new_book_information(form):
    data = {
        "author": form.author.data.title(),
        "title": form.title.data.title(),
        "date": datetime.date.today().strftime('%Y-%m-%d')
    }
    return data


def _header_create(name, scripture_dict, kid_dict):
    header_text = f'<font size=20> {name} </font>' \
                  '<br />' \
                  '<br />' \
                  f'"{scripture_dict["scripture"]}" ({scripture_dict["reference"]})' \
                  '<br />' \
                  '<br />' \
                  f'<i>Scripture Reading Assignment</i>: {scripture_dict["assignment"]}' \
                  '<br />' \
                  '<br />' \
                  f'<i>Goal</i>: {kid_dict["goal"]}' \
                  '<br />' \
                  '<br />' \
                  '<br />' \

    p_style = ParagraphStyle(name='Normal', fontName='Times', fontSize=12)
    paragraph = Paragraph(header_text, style=p_style)
    return paragraph

def _table_body(name, dates, kid_dict):
    print(name, dates, kid_dict)
    days_of_week = ['', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    if name == ['Calvin', 'Samuel']:
        return [
            [f'{days[0]}\n{days[1]}' for days in zip(days_of_week, [''] + dates)],
            [f'Math ({kid_dict["book"]}) \n (1.5-2 hrs.)', 'X', '', '', '', '', '', ''],
            ['Reading: Scriptures \n (10 min.)', '', '', '', '', '', '', ''],
            ['Reading: Classics \n (20 min.)', 'X', '', '', '', '', '', ''],
            ['Reading: Science \n (30 min.)', 'X', '', '', '', '', '', ''],
            ['Reading: Other \n (60 min.)', 'X', '', '', '', '', '', ''],
            ['Letters: Vocab \n (15 min.)', 'X', '', '', '', '', '', ''],
            ['Letters: Writing \n (15 min.)', 'X', '', '', '', '', '', ''],
            ['Music \n (15-30 min.)', '', '', '', '', '', '', ''],
            ['Job: Pickup \n (5 min.)', 'X', '', '', '', '', '', ''],
            ['Job:\n ', 'X'] + kid_dict['jobs'],
        ]
    elif name in ['Kay', 'Seth']:
        return [
            [f'{days[0]}\n{days[1]}' for days in zip(days_of_week, [''] + dates)],
            [f'Math ({kid_dict["book"]}) \n (1.5-2 hrs.)', 'X', '', '', '', '', '', ''],
            ['Reading: Scriptures \n (10 min.)', '', '', '', '', '', '', ''],
            ['Reading: Other \n (110 min.)', 'X', '', '', '', '', '', ''],
            ['Letters: Vocab \n (15 min.)', 'X', '', '', '', '', '', ''],
            ['Letters: Writing \n (15 min.)', 'X', '', '', '', '', '', ''],
            ['Music \n (15-30 min.)', '', '', '', '', '', '', ''],
            ['Job: Pickup \n (5 min.)', 'X', '', '', '', '', '', ''],
            ['Job:\n ', 'X'] + kid_dict['jobs'],
        ]
    elif name in ['Maggie', 'Martin']:
        return [
            [f'{days[0]}\n{days[1]}' for days in zip(days_of_week, [''] + dates)],
            [f'Math ({kid_dict["book"]}) \n (1.5-2 hrs.)', 'X', '', '', '', '', '', ''],
            ['Reading: Scriptures \n (10 min.)', '', '', '', '', '', '', ''],
            ['Reading: Other \n (110 min.)', 'X', '', '', '', '', '', ''],
            ['Letters: Writing \n (15 min.)', 'X', '', '', '', '', '', ''],
            ['Music \n (15-60 min.)', '', '', '', '', '', '', ''],
            ['Job: Pickup \n (5 min.)', 'X', '', '', '', '', '', ''],
            ['Job:\n ', 'X'] + kid_dict['jobs'],
        ]

def _table_create(name, dates, kid_dict):
    print(_table_body(name, dates, kid_dict))
    table = Table(
        _table_body(name, dates, kid_dict),
    )
    style = TableStyle(
        [
            # top margin
            ('BACKGROUND', (1, 0), (-1, 0), colors.lightgrey),
            ('LEFTPADDING', (1, 0), (-1, 0), 12),
            ('RIGHTPADDING', (1, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (1, 0), (-1, 0), 12),
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
            ('GRID', (1, 0), (-1, 0), 1, colors.black),

            # left margin
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('VALIGN', (0, 1), (0, -1), 'TOP'),
            ('GRID', (0, 1), (0, -1), 1, colors.black),

            # body
            ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (1, 1), (-1, -1), 'TOP'),
            ('GRID', (1, 1), (-1, -1), 1, colors.black),

            # all
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),

            # Sunday
            ('FONTSIZE', (1, 1), (1, -1), 20),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ]
    )
    table.setStyle(style)

    return table

def _timesheet_create(name, dates, scripture_dict, kid_dict):
    header = _header_create(name, scripture_dict, kid_dict)
    table = _table_create(name, dates, kid_dict)
    return [header, table]

def _boiler_header_create(name, date):
    boiler_header = Table(
        [
            [f'{name}', f'{date}'],
            ['', '']
        ],
        colWidths=250
    )
    style = TableStyle(
        [
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black, None, None, None, 4, 0.5),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black, None, None, None, 4, 0.5),
            # line commands are like
            # op, start, stop, weight, colour, cap, dashes, join, linecount, linespacing

            ('BOTTOMPADDING', (0, -1), (-1, -1), 40),
        ]
    )
    boiler_header.setStyle(style)
    return boiler_header

def _math_table_create(math_book):
    math_table = Table(
        [
            [f'Math Assignment ({math_book})', ''],
            ['Start Chapter:', 'First Problem:'],
            ['End Chapter:', 'Last Problem:'],
            ['Start Time:', 'End Time:'],
            ['Problems Missed:', ''],
        ],
        colWidths=250
    )
    style = TableStyle(
        [
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 4), (1, 4)),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 1), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]
    )
    math_table.setStyle(style)
    return math_table

def _scripture_table_create(i):
    scripture_table = Table(
        [
            ['Scriptures Questions, Principles, and Commentary', '', ''],
            ['Start Book:', 'Start Chapter:', 'Start Verse:'],
            ['End Book:', 'End Chapter:', 'End Verse:'],
            ['Comments:', '', ''],
        ],
        colWidths=167
    )
    # todo: this is ugly
    if i == 0:
        style = TableStyle(
            [
                ('SPAN', (0, 0), (-1, 0)),
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('GRID', (0, 1), (-1, 2), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),

                ('TOPPADDING', (0, 3), (-1, -1), 14),
                ('SPAN', (0, 3), (-1, -1)),
            ]
        )
    else:
        style = TableStyle(
            [
                ('TOPPADDING', (0, 0), (-1, 0), 100),
                ('SPAN', (0, 0), (-1, 0)),
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('GRID', (0, 1), (-1, 2), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),

                ('TOPPADDING', (0, 3), (-1, -1), 14),
                ('SPAN', (0, 3), (-1, -1)),
            ]
        )
    scripture_table.setStyle(style)
    return scripture_table

def boiler_sheet_pdf_create(name, date, math_book, i):
    boiler_header = _boiler_header_create(name, date)
    if i == 0:
        return [boiler_header, _scripture_table_create(i)]
    return [boiler_header, _math_table_create(math_book), _scripture_table_create(i)]

def weekly_form_pdf_create(date_lst, scripture_dict, kids_dict):
    pdf = SimpleDocTemplate('weekly_time_sheet.pdf', pagesize=landscape(letter), leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)

    p_frame = Frame(
        0.5 * inch, 0.5 * inch, 7.5 * inch, 10 * inch,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        id='portrait_frame'
    )
    l_frame = Frame(
        0.5 * inch, 0.5 * inch, 10 * inch, 7.5 * inch,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        id='landscape_frame'
    )

    portrait_template = PageTemplate(id='portrait', frames=[p_frame], pagesize=letter)
    landscape_template = PageTemplate(id='landscape', frames=[l_frame], pagesize=landscape(letter))
    pdf.addPageTemplates([landscape_template, portrait_template])

    elems = []
    for kid in kids_dict.keys():
        form_elem = _timesheet_create(kid, date_lst, scripture_dict, kids_dict[kid])
        elems += form_elem

        for i, date in enumerate(date_lst):
            elems.append(NextPageTemplate('portrait'))
            elems.append(PageBreak())
            elems += boiler_sheet_pdf_create(kid, date, kids_dict[kid]['book'], i)

        elems.append(NextPageTemplate('landscape'))
        elems.append(PageBreak())
    elems.pop()
    pdf.build(elems)

def weekly_summary_create(scripture_dict, kids_dict):
    pdf = SimpleDocTemplate('weekly_summary.pdf', pagesize=letter, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)

    scripture_body = '<i><font size=16>Scriptures</font></i>'\
                  '<br />' \
                  '<br />'\
                  f'<i>Scripture</i>: "{scripture_dict["scripture"]}" ({scripture_dict["reference"]})' \
                  '<br />' \
                  '<br />'
    p_style = ParagraphStyle(name='Normal', fontName='Times', fontSize=10)
    scripture_paragraph = Paragraph(scripture_body, style=p_style)

    scripture_ass_body = '<br />' \
                  f'<i>Reading Assignment</i>: {scripture_dict["assignment"]}' \
                  '<br />' \
                  '<br />'
    scripture_ass_paragraph = Paragraph(scripture_ass_body, style=p_style)

    goals_header = '<br />' \
                  f'<i>Goals</i>' \
                  '<br />' \
                  '<br />'
    p_style = ParagraphStyle(name='Normal', fontName='Times', fontSize=16)
    goals_paragraph = Paragraph(goals_header, style=p_style)

    goals_body = [[name, dict['goal']] for name, dict in kids_dict.items()]
    goals_table = Table(goals_body)
    t_style = TableStyle(
        [
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('ALIGN', (1, 0), (-1, 0), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]
    )
    goals_table.setStyle(t_style)

    buffer = '<br />' \
             '<br />'
    buffer_paragraph = Paragraph(buffer, style=p_style)

    jobs_body = '<br />' \
                  '<i>Jobs</i>' \
                  '<br />' \
                  '<br />'
    p_style = ParagraphStyle(name='Normal', fontName='Times', fontSize=16)
    jobs_paragraph = Paragraph(jobs_body, style=p_style)

    jobs_body = [['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']] + [[name] + dict['jobs'] for name, dict in kids_dict.items()]
    jobs_table = Table(jobs_body)
    t_style = TableStyle(
        [
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
            ('BACKGROUND', (1, 0), (-1, 0), colors.lightgrey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
            ('GRID', (1, 0), (-1, 0), 1, colors.black),
            ('GRID', (0, 1), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]
    )
    jobs_table.setStyle(t_style)

    line = Drawing(100, 1)
    line.add(Line(0, 0, 530, 0))

    elems = [scripture_paragraph, scripture_ass_paragraph, line, goals_paragraph, goals_table, buffer_paragraph, line, jobs_paragraph, jobs_table]

    pdf.build(elems)

def _problem_list_create(first, last, less_num):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    if str(first).isalpha():
        if str(last).isalpha():
            return [letter for letter in alphabet if (letter >= str(first) and letter <= str(last))]
        else:
            return [letter for letter in alphabet if (letter >= str(first) and letter <= less_num)] + list(map(str, range(1, int(last) + 1)))
    else:
        return list(map(str, range(int(first), int(last) + 1)))


def _alternatives_create(length, num):
    alternatives = []
    for card_i in range(length):
        alternatives_i = []
        for j in range(3):
            random_lesson = np.random.choice(helpers_constants.lesson_lst)
            num_cards_in_random_lesson = len(os.listdir('static/{0}'.format(random_lesson)))
            random_card = np.random.choice(range(0, num_cards_in_random_lesson, 2))
            alternatives_i.append('../static/{0}/rc_vocab_{0}_{1}.png'.format(random_lesson, random_card + num))
        alternatives.append(alternatives_i)
    return alternatives


def scripture_list_json(form):
    data = {
        "week_start_date": str(form.weekof.data),
        "scripture_ref": form.scripture_ref.data,
        "scripture": form.scripture.data,
    }
    return data


def scripture_table_create(data, year='current'):
    data['week_start_date'] = pd.to_datetime(data['week_start_date'])
    if year == 'current':
        year = max(data['week_start_date'].dt.year)
    elif year == 'all':
        year = '2019'
    data. \
        query('week_start_date >= "{year}-01-01"'.format(year=year)).\
        sort_values('week_start_date').\
        assign(week_start_date=data['week_start_date'].astype(str)).\
        groupby('scripture'). \
        first(). \
        reset_index() \
        [['scripture', 'scripture_ref', 'week_start_date']]. \
        pipe(scriptures_latex_create)


def db_writer(db_math_aggregate, user, df):
    db_math_aggregate[user].drop()
    ret = db_math_aggregate[user].insert_many(df)
    print(ret)


def miss_lst_create(record, lst, test=False):
    dict_out = defaultdict(list)

    if test:
        add_list = [{'chapter': 'test {}'.format(problem['chapter']), 'problem': problem['problem']} for problem in record[lst]]
        rem_list = [{'chapter': 'test {}'.format(problem['chapter']), 'problem': problem['problem']} for problem in record['rem_miss_list']]
    else:
        add_list = [{'chapter': problem['chapter'], 'problem': problem['problem']} for problem in record[lst]]
        rem_list = [{'chapter': problem['chapter'], 'problem': problem['problem']} for problem in record['rem_miss_list']]

    # todo: this method for removing from miss list is maybe flawed
    for prob in add_list:
        dict_out[prob['chapter']].append(prob['problem'])
    for prob in rem_list:
        dict_out[prob['chapter']].remove(prob['problem'])
    k_to_del = [k for k, v in dict_out.items() if not dict_out[k]]
    for k in k_to_del:
        del dict_out[k]
    return dict(dict_out)


def _test_atomize(record):
    df_out = pd.DataFrame()

    df_out['problem'] = range(1, 21)
    df_out['name'] = record['kid']
    df_out['book'] = record['book']
    df_out['chapter'] = record['end_chapter']
    df_out['date'] = record['date']
    df_out['origin'] = np.nan

    miss_lst = record['miss_lst'].get(str(record['end_chapter']))
    if not miss_lst:
        miss_lst = []
    df_out['correct'] = df_out.apply(lambda x: 0 if str(x['problem']) in miss_lst else 1, axis=1)

    hard_lst = record['hard_lst'].get(str(record['end_chapter']))
    if not hard_lst:
        hard_lst = []
    df_out['hard'] = df_out.apply(lambda x: 1 if str(x['problem']) in hard_lst else 0, axis=1)

    df_out['meta__insert_time'] = str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M'))

    return df_out[['book', 'chapter', 'correct', 'hard', 'date', 'origin', 'problem', 'name', 'meta__insert_time']]


def _chapter_atomize(db_origin, db_number, chapter, record):
    df_origins = pd.DataFrame(list(db_origin.find({'chapter': chapter})))
    df_number = pd.DataFrame(list(db_number.find({'chapter': chapter})))

    df_practice = pd.DataFrame()
    practice_problems_index = list(string.ascii_lowercase).index(df_number['num_lesson_probs'].iloc[0]) + 1
    df_practice['problem'] = list(string.ascii_lowercase)[:practice_problems_index]
    df_practice['origin'] = np.nan

    df_review = pd.DataFrame()
    df_review['origin'] = df_origins['origin_list'][0]
    df_review['problem'] = df_review.index + 1

    df = df_practice.append(df_review).reset_index(drop=True)

    miss_lst = record['miss_lst'].get(str(chapter))  # how to return None instead of throwing an error when key doesn't exist.
    hard_lst = record['hard_lst'].get(str(chapter))

    if miss_lst:
        df['correct'] = df.apply(lambda x: 0 if str(x['problem']) in miss_lst else 1, axis=1)
    else:
        df['correct'] = 1
    if hard_lst:
        df['hard'] = df.apply(lambda x: 1 if str(x['problem']) in hard_lst else 0, axis=1)
    else:
        df['hard'] = 0

    df['book'] = record['book']
    df['chapter'] = chapter
    df['date'] = record['date']
    df['name'] = record['kid']
    df['meta__insert_time'] = str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M'))

    if chapter == record['start_chapter']:
        index = df[df['problem'].astype(str) == record['start_problem']].index[0]
        df = df.loc[index:]
    if chapter == record['end_chapter']:
        index = df[df['problem'].astype(str) == record['end_problem']].index[0]
        df = df.loc[:index]
    return df.reset_index(drop=True)


def _ass_atomize(db_origin, db_number, record):
    df = pd.DataFrame()
    for chapter in range(record['start_chapter'], record['end_chapter'] + 1):
        df = df.append(_chapter_atomize(db_origin, db_number, chapter, record))
    return df[['book', 'chapter', 'correct', 'hard', 'date', 'origin', 'problem', 'name', 'meta__insert_time']]


def _elapsed_time(record):
    start_time = datetime.datetime.strptime('{0} {1}'.format(record['date'], record['start_time']), '%Y-%m-%d %H:%M')
    if start_time.hour < 6:
        start_time = start_time + datetime.timedelta(hours=12)
    end_time = datetime.datetime.strptime('{0} {1}'.format(record['date'], record['end_time']), '%Y-%m-%d %H:%M')
    if end_time.hour < 6:
        end_time = end_time + datetime.timedelta(hours=12)

    return [{'date': record['date'], 'kid': record['kid'], 'duration': int((end_time - start_time).seconds / 60)}]


def _math_todo_create(name, db_aggregate, begin_date):
    df_hard = pd.DataFrame(list(db_aggregate.db[name].find())). \
        query('date >= "{}"'.format(begin_date)). \
        query('hard == 1'.format(begin_date)) \
        [['book', 'chapter', 'problem']]
    df_hard['book'] = df_hard['book'].map(helpers_constants.book_dict)
    return df_hard.to_dict('records')
