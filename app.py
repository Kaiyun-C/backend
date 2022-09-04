'''
Date: 28/08/2022
Author: Kaiyun Chen
'''

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import chart_studio
import plotly.graph_objects as go
import chart_studio.plotly as py
import plotly.express as px
# import pymysql
# pymysql.install_as_MySQLdb()
chart_studio.tools.set_credentials_file(
    username='kch0083', api_key='4oYjeM5PdCS815xuxyUS')

app = Flask(__name__)
CORS(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:adminadmin@database-2.coh1lexhr8xj.ap-northeast-1.rds.amazonaws.com' \
                                 ':3306/sys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def drawing_plot():
    table_df = pd.read_sql_table(
        "dia_year_sex",
        con=db.engine,
        columns=['id',
                 'years',
                 'males',
                 'females',
                 'persons'
                 ],
    )
    years = table_df['years']
    males = table_df['males']
    females = table_df['females']

    m_trend = go.Scatter(
        x=years,
        y=males,
        name='Males',
        mode='lines',
        line=dict(color='#0099e6'),

    )

    f_trend = go.Scatter(
        x=years,
        y=females,
        name='Females',
        mode='lines',
        line=dict(color='#f14444'),

    )

    final_data = [m_trend, f_trend]
    fig = go.Figure(final_data).update_xaxes(title_text='Year').update_yaxes(
        title_text='Age-standardised per cent').update_layout(
        title='Prevalence of type 2 diabetes, by sex, 2000–2020',
        font=dict(size=25)).update_layout(
        hoverlabel=dict(
            font_size=25,
            font_family="Rockwell"
        ))

    py.plot(fig, filename='base_line', auto_open=False, show_link=False)

    complication_df = pd.read_sql_table(
        "complications_sex",
        con=db.engine,
        columns=['id',
                 'Number_of_Complications',
                 'Males',
                 'Females',
                 'Persons'
                 ],
    )
    num_comp = complication_df['Number_of_Complications']
    percentage = complication_df['Persons']
    blue_color = ['#e6f2ff', '#80bfff', '#1a8cff',
                  '#3366ff', '#005ce6', '#0040ff']
    fig2 = go.Figure(data=[go.Pie(labels=num_comp, values=percentage,
                                  hole=.6,
                                  pull=[0, 0.1, 0.1, 0.1, 0.15, 0.2],
                                  marker_colors=blue_color,
                                  hoverinfo='skip'
                                  )])
    fig2.update_layout(
        title_text="Number of Complications percentage",
        annotations=[dict(text='Age <br> standardised <br> percentage',
                          font_size=25, showarrow=False)],
        font=dict(size=25)
    ).update_layout(legend_title_text='Number of Complications')
    py.plot(fig2, filename='pie_c', auto_open=False, show_link=False)


drawing_plot()


@app.route("/add", methods=["POST"], strict_slashes=False)
def add_articles():
    height = float(request.json['height'])
    weight = float(request.json['weight'])

    bmi = weight/((height/100)**2)

    # db.session.add(bmi)
    # db.session.commit()

    return jsonify({"bmi": bmi})


@app.route("/", methods=["GET"], strict_slashes=False)
def index():

    return jsonify({"HELLO": "WORLD"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
