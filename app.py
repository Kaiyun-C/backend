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
import random
import json
import pymysql
pymysql.install_as_MySQLdb()
chart_studio.tools.set_credentials_file(username='kch0083', api_key='4oYjeM5PdCS815xuxyUS')

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
        line=dict(color='#0099e6')
    )

    f_trend = go.Scatter(
        x=years,
        y=females,
        name='Females',
        mode='lines',
        line=dict(color='#99ddff')
    )

    final_data = [m_trend, f_trend]
    fig = go.Figure(final_data).update_xaxes(title_text='Year').update_yaxes(
        title_text='Age-standardised per cent').update_layout(
        title='Prevalence of type 2 diabetes, by sex, 2000–2020',
        font=dict(size=25))

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
    blue_color = ['#e6f2ff', '#80bfff', '#1a8cff', '#3366ff', '#005ce6', '#0040ff']
    fig2 = go.Figure(data=[go.Pie(labels=num_comp, values=percentage,
                                  hole=.6,
                                  pull=[0, 0.1, 0.1, 0.1, 0.15, 0.2],
                                  marker_colors=blue_color
                                  )])
    fig2.update_layout(
        title_text="Number of Complications percentage",
        annotations=[dict(text='Age standardised percentage', font_size=16, showarrow=False)],
        font=dict(size=25)
    )
    py.plot(fig2, filename='pie_c', auto_open=False, show_link=False)


drawing_plot()

# FOOD RECIPE
food_df = pd.read_sql_table(
    "clanned_calories",
    "mysql://admin:adminadmin@database-2.coh1lexhr8xj.ap-northeast-1.rds.amazonaws.com:3306/data1",
)
head_list = list(food_df.columns) # ['Food', 'Bi_category', 'Tag', 'Unit', 'Grams', 'Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs', 'GI', 'GI_level']
food_dict = []
for row in food_df.values:
    # {'Food': "Cows' milk", 'Bi_category': 'Dairy_products_1', 'Tag': 1, 'Unit': '1 cup', 'Grams': 250, 'Calories': 169.06, 'Protein': 8.2, 'Fat': 10.25, 'Sat.Fat': 9.22, 'Fiber': 0, 'Carbs': 12.3, 'GI': 27.6, 'GI_level': 'low'}
    row_dict = dict(zip(head_list, row))
    food_dict.append(row_dict)
# Tag
Tag_dict = {0: '', 1: '', 2: 'Boiled', 3: 'Steamed', 4: 'Baked', 5: 'Fried with less oil'}

# dictionary list of Low GI, Low Fat, Low Carb, Halal
food_dict_cal = []
food_dict_GI = []
food_dict_cal_GI = []
food_dict_halal = []
food_dict_cal_halal = []
food_dict_GI_halal = []
food_dict_cal_GI_halal = []
food_dict_carb = []
food_dict_cal_carb = []
food_dict_GI_carb = []
food_dict_cal_GI_carb = []
food_dict_halal_carb = []
food_dict_cal_halal_carb = []
food_dict_GI_halal_carb = []
food_dict_cal_GI_halal_carb = []

for each in food_dict:
    if each['Bi_category'] != 'Meat' and each['Calories'] <= 150:
        food_dict_cal.append(each)
    elif each['Bi_category'] == 'Meat' and each['Calories'] < 290:
        food_dict_cal.append(each)
    elif each['Bi_category'] == 'Nuts':
        food_dict_cal.append(each)
for each in food_dict:
    if each['GI_level'] == 'low':
        food_dict_GI.append(each)
for each in food_dict_cal:
    if each['GI_level'] == 'low':
        food_dict_cal_GI.append(each)
# for halal
for each in food_dict:
    if each['Food'] not in ['Pork roast', 'Pork']:
        food_dict_halal.append(each)
for each in food_dict_cal:
    if each['Food'] not in ['Pork roast', 'Pork']:
        food_dict_cal_halal.append(each)
for each in food_dict_GI:
    if each['Food'] not in ['Pork roast', 'Pork']:
        food_dict_GI_halal.append(each)
for each in food_dict_cal_GI:
    if each['Food'] not in ['Pork roast', 'Pork']:
        food_dict_cal_GI_halal.append(each)
# for low carbs
for each in food_dict:
    if each['Carbs'] <= 50:
        food_dict_carb.append(each)
for each in food_dict_cal:
    if each['Carbs'] <= 50:
        food_dict_cal_carb.append(each)
for each in food_dict_GI:
    if each['Carbs'] <= 50:
        food_dict_GI_carb.append(each)
for each in food_dict_cal_GI:
    if each['Carbs'] <= 50:
        food_dict_cal_GI_carb.append(each)
for each in food_dict_halal:
    if each['Carbs'] <= 50:
        food_dict_halal_carb.append(each)
for each in food_dict_cal_halal:
    if each['Carbs'] <= 50:
        food_dict_cal_halal_carb.append(each)
for each in food_dict_GI_halal:
    if each['Carbs'] <= 50:
        food_dict_GI_halal_carb.append(each)
for each in food_dict_cal_GI_halal:
    if each['Carbs'] <= 50:
        food_dict_cal_GI_halal_carb.append(each)


class Recipe:
    '''
    veg 和 high protein的 meal组成方式 与别的不同
    所以对于 Low GI, Low Fat, Low Carb, Halal 的排列组合归纳成了不同的 dictionary，作为参数 one_dict
    对于是否是 veg、是否是 high protein作为 tag：'veg', 'high_protein'
    '''
    def __init__(self, tag, one_dict):
        self.tag = tag
        self.one_dict = one_dict

    # randomly choose 1 Staple_food
    def staple_food(self, one_dict):
        Staple_food_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Staple_food':
                Staple_food_list.append(each)
        one_Staple_food = random.sample(Staple_food_list, 1)[0]
        return one_Staple_food

    # randomly choose 1 Dairy_product
    def dairy_product(self, one_dict):
        Dairy_products_list = []
        for each in self.one_dict:
            if each['Bi_category'] in ['Dairy_products_1', 'Dairy_products_2']:
                Dairy_products_list.append(each)
        one_Dairy_product = random.sample(Dairy_products_list, 1)[0]
        return one_Dairy_product

    # randomly choose 1 Fruit_1
    def fruit(self, one_dict):
        Fruit_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Fruit_1':
                Fruit_list.append(each)
        one_Fruit = random.sample(Fruit_list, 1)[0]
        return one_Fruit

    # randomly choose 1 Fruit_2
    def juice(self, one_dict):
        juice_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Fruit_2':
                juice_list.append(each)
        one_juice = random.sample(juice_list, 1)[0]
        return one_juice

    # randomly choose 1 Meat
    def meat(self, one_dict):
        Meat_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Meat':
                Meat_list.append(each)
        one_Meat = random.sample(Meat_list, 1)[0]
        return one_Meat

    # randomly choose 1 Meat for Halal
    def halal(self, one_dict):
        Meat_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Meat' and each['Food'] not in ['Pork roast', 'Pork']:
                Meat_list.append(each)
        one_Meat = random.sample(Meat_list, 1)[0]
        return one_Meat

    # randomly choose 1 seafood
    def seafood(self, one_dict):
        seafood_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'seafood' and each['Tag'] == 4:
                seafood_list.append(each)
        one_seafood = random.sample(seafood_list, 1)[0]
        return one_seafood

    # randomly choose 5 Vegetables for salad
    def vegetables_lunch(self, one_dict):
        Vegetables_list_1 = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Vegetables' and each['Tag'] == 1:
                Vegetables_list_1.append(each)
        five_Vegetables = random.sample(Vegetables_list_1, 5)
        return five_Vegetables

    # randomly choose 1 Vegetables from Tag 0
    def vegetables_dinner(self, one_dict):
        Vegetables_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Vegetables' and each['Tag'] == 0:
                Vegetables_list.append(each)
        one_Vegetable = random.sample(Vegetables_list, 1)[0]
        return one_Vegetable

    # randomly choose 1 Nuts
    def nuts(self, one_dict):
        Nuts_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Nuts':
                Nuts_list.append(each)
        one_Nut = random.sample(Nuts_list, 1)[0]
        return one_Nut

    def show_plan(self, tag, one_dict):
        Staple_food_breakfast = self.staple_food(self.one_dict)
        Dairy_product = self.dairy_product(self.one_dict)
        Fruit_breakfast = self.fruit(self.one_dict)
        Meat_lunch = self.meat(self.one_dict)
        Seafood_lunch = self.seafood(self.one_dict)
        Juice = self.juice(self.one_dict)
        Vegetables_dinner_one = self.vegetables_dinner(self.one_dict)
        Nuts = self.nuts(self.one_dict)

        Vegetables_lunch = self.vegetables_lunch(self.one_dict)
        five_Vegetables_list = [each['Food'] for each in Vegetables_lunch]
        five_Vegetables_cal = [each['Calories'] for each in Vegetables_lunch]
        five_Vegetables_pro = [each['Protein'] for each in Vegetables_lunch]
        five_Vegetables_carb = [each['Carbs'] for each in Vegetables_lunch]
        if self.tag != 'veg':
            ve_cal_lunch = sum(five_Vegetables_cal) / 2
            ve_pro_lunch = sum(five_Vegetables_pro) / 2
            ve_carb_lunch = sum(five_Vegetables_carb) / 2
            five_Vegetables_str = ','.join(five_Vegetables_list)
            Vegetables_lunch_str = five_Vegetables_str + ' (250-300g in total)'
        else:
            ve_cal_lunch = sum(five_Vegetables_cal) * 0.65
            ve_pro_lunch = sum(five_Vegetables_pro) * 0.65
            ve_carb_lunch = sum(five_Vegetables_carb) * 0.65
            five_Vegetables_str = ','.join(five_Vegetables_list)
            Vegetables_lunch_str = five_Vegetables_str + ' (300-350g in total)'

        four_Vegetables_dinner = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Vegetables' and each['Tag'] in [2, 3] and each['Food'] not in five_Vegetables_list:
                four_Vegetables_dinner.append(each)
        four_Vegetables = random.sample(four_Vegetables_dinner, 4)
        four_Vegetables_list = [each['Food'] for each in four_Vegetables]
        four_Vegetables_cal = [each['Calories'] for each in four_Vegetables]
        four_Vegetables_pro = [each['Protein'] for each in four_Vegetables]
        four_Vegetables_carb = [each['Carbs'] for each in four_Vegetables]
        if self.tag != 'veg':
            ve_cal_dinner_1 = sum(four_Vegetables_cal) / 2
            ve_pro_dinner_1 = sum(four_Vegetables_pro) / 2
            ve_carb_dinner_1 = sum(four_Vegetables_carb) / 2
            four_Vegetables_str = ','.join(four_Vegetables_list)
            four_Vegetables_dinner_str = four_Vegetables_str + ' (Boiled, steamed or baked, 200-250g in total)'
        else:
            ve_cal_dinner_1 = sum(four_Vegetables_cal) * 0.8
            ve_pro_dinner_1 = sum(four_Vegetables_pro) * 0.8
            ve_carb_dinner_1 = sum(four_Vegetables_carb) * 0.8
            four_Vegetables_str = ','.join(four_Vegetables_list)
            four_Vegetables_dinner_str = four_Vegetables_str + ' (Boiled, steamed or baked, 300-350g in total)'

        Staple_food_lunch = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Staple_food' and each['Food'] != Staple_food_breakfast['Food']:
                Staple_food_lunch.append(each)
        one_Staple_lunch = random.sample(Staple_food_lunch, 1)[0]

        Meat_dinner = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Meat' and each['Food'] != Meat_lunch['Food']:
                Meat_dinner.append(each)
        one_Meat_dinner = random.sample(Meat_dinner, 1)[0]


        Seafood_dinner = []
        for each in self.one_dict:
            if each['Bi_category'] == 'seafood' and each['Tag'] == 4 and each['Food'] != Seafood_lunch['Food']:
                Seafood_dinner.append(each)
        one_seafood_dinner = random.sample(Seafood_dinner, 1)[0]

        Fruit_lunch_list = []
        for each in self.one_dict:
            if each['Bi_category'] == 'Fruit_1' and each['Food'] != Fruit_breakfast['Food']:
                Fruit_lunch_list.append(each)
        one_Fruit_lunch = random.sample(Fruit_lunch_list, 1)[0]
        one_Fruit_str_lunch = one_Fruit_lunch['Unit'] + ' ' + one_Fruit_lunch['Food'] + ' ' + str(
            one_Fruit_lunch['Grams'])

        # recipe
        Breakfast_plan = Staple_food_breakfast['Food'] + ' ' + str(Staple_food_breakfast['Grams']) + 'g; ' \
                         + '1 egg; ' \
                         + Dairy_product['Food'] + ' ' + Dairy_product['Unit'] + '; ' \
                         + Fruit_breakfast['Unit'] + ' ' + Fruit_breakfast['Food'] + ' ' + str(
            Fruit_breakfast['Grams']) + 'g'
        if tag == 'veg':
            Lunch_plan = one_Staple_lunch['Food'] + ' ' + str(one_Staple_lunch['Grams']) + 'g; ' \
                         + '1 egg; ' \
                         + 'Salad: ' + Vegetables_lunch_str + '; ' \
                         + one_Fruit_str_lunch + 'g; ' \
                         + Juice['Unit'] + ' ' + Juice['Food']
            Dinner_plan = '1 egg; ' \
                          + Vegetables_dinner_one['Food'] + ' (100g in total); ' \
                          + four_Vegetables_dinner_str + '; ' \
                          + Nuts['Food'] + ' 25g'

            # calculate calories
            kcal_bre = int(
                Staple_food_breakfast['Calories'] + 72 + Dairy_product['Calories'] + Fruit_breakfast['Calories'])
            kcal_lun = int(one_Staple_lunch['Calories'] + 72 + ve_cal_lunch + Juice['Calories'])
            kcal_din = int(72 + Vegetables_dinner_one['Calories'] + ve_cal_dinner_1 + Nuts['Calories'] / 2)
            kcal_1day = kcal_bre + kcal_lun + kcal_din

            # calculate Protein
            pro_bre = int(Staple_food_breakfast['Protein'] + 6 + Dairy_product['Protein'] + Fruit_breakfast['Protein'])
            pro_lun = int(one_Staple_lunch['Protein'] + 6 + ve_pro_lunch + Juice['Protein'])
            pro_din = int(6 + Vegetables_dinner_one['Protein'] + ve_pro_dinner_1 + Nuts['Protein'] / 2)
            pro_1day = pro_bre + pro_lun + pro_din

            # calculate Carbs
            carb_bre = int(Staple_food_breakfast['Carbs'] + 0 + Dairy_product['Carbs'] + Fruit_breakfast['Carbs'])
            carb_lun = int(one_Staple_lunch['Carbs'] + 0 + ve_carb_lunch + Juice['Carbs'])
            carb_din = int(0 + Vegetables_dinner_one['Carbs'] + ve_carb_dinner_1 + Nuts['Carbs'] / 2)
            carb_1day = carb_bre + carb_lun + carb_din
        else:
            if tag != 'high_protein':
                Lunch_plan = one_Staple_lunch['Food']+ ' '+str(one_Staple_lunch['Grams']) +'g; '\
                            + Meat_lunch['Food'] + ' ' + Meat_lunch['Unit']  + ' ' + Tag_dict[Meat_lunch['Tag']]\
                            + ' or ' + Seafood_lunch['Food'] + ' ' + Seafood_lunch['Unit'] + ' (Boiled, steamed or baked); '\
                            + 'Salad: ' + Vegetables_lunch_str +'; '\
                            + Juice['Unit'] + ' ' + Juice['Food']
                Dinner_plan = one_Meat_dinner['Food'] + ' ' + one_Meat_dinner['Unit']  + ' ' + Tag_dict[one_Meat_dinner['Tag']]\
                            + ' or ' + one_seafood_dinner['Unit'] + ' ' + one_seafood_dinner['Food'] + ' (Boiled, steamed or baked); '\
                            + Vegetables_dinner_one['Food'] + ' (100g in total); '\
                            + four_Vegetables_dinner_str + '; '\
                            + Nuts['Food'] + ' 25g'
                # calculate calories
                kcal_bre = int(Staple_food_breakfast['Calories']+72+Dairy_product['Calories']+Fruit_breakfast['Calories'])
                kcal_lun = int(one_Staple_lunch['Calories']+(Meat_lunch['Calories']+Seafood_lunch['Calories'])/2+ve_cal_lunch+Juice['Calories'])
                kcal_din = int((one_Meat_dinner['Calories']+one_seafood_dinner['Calories'])/2+Vegetables_dinner_one['Calories']+ve_cal_dinner_1+Nuts['Calories']/2)
                kcal_1day = kcal_bre+kcal_lun+kcal_din

                # calculate Protein
                pro_bre = int(Staple_food_breakfast['Protein'] + 6 + Dairy_product['Protein'] + Fruit_breakfast['Protein'])
                pro_lun = int(one_Staple_lunch['Protein'] + (Meat_lunch['Protein'] + Seafood_lunch['Protein']) / 2 + ve_pro_lunch + Juice['Protein'])
                pro_din = int((one_Meat_dinner['Protein'] + one_seafood_dinner['Protein']) / 2 + Vegetables_dinner_one['Calories'] + ve_pro_dinner_1 + Nuts['Protein'] / 2)
                pro_1day = pro_bre + pro_lun + pro_din

                # calculate Carbs
                carb_bre = int(Staple_food_breakfast['Carbs'] + 0 + Dairy_product['Carbs'] + Fruit_breakfast['Carbs'])
                carb_lun = int(one_Staple_lunch['Carbs'] + (Meat_lunch['Carbs'] + Seafood_lunch['Carbs']) / 2 + ve_carb_lunch + Juice['Carbs'])
                carb_din = int((one_Meat_dinner['Carbs'] + one_seafood_dinner['Carbs']) / 2 + Vegetables_dinner_one['Carbs'] + ve_carb_dinner_1 + Nuts['Carbs'] / 2)
                carb_1day = carb_bre + carb_lun + carb_din
            else:
                Lunch_plan = one_Staple_lunch['Food'] + ' ' + str(one_Staple_lunch['Grams']) + 'g; ' \
                             + Meat_lunch['Food'] + ' ' + Meat_lunch['Unit'] + ' ' + Tag_dict[Meat_lunch['Tag']] \
                             + ' and ' + Seafood_lunch['Food'] + ' ' + Seafood_lunch[
                                 'Unit'] + ' (Boiled, steamed or baked); ' \
                             + 'Salad: ' + Vegetables_lunch_str + '; ' \
                             + Juice['Unit'] + ' ' + Juice['Food']
                Dinner_plan = one_Meat_dinner['Food'] + ' ' + one_Meat_dinner['Unit'] + ' ' + Tag_dict[
                    one_Meat_dinner['Tag']] \
                              + ' and ' + one_seafood_dinner['Unit'] + ' ' + one_seafood_dinner[
                                  'Food'] + ' (Boiled, steamed or baked); ' \
                              + Vegetables_dinner_one['Food'] + ' (100g in total); ' \
                              + four_Vegetables_dinner_str + '; ' \
                              + Nuts['Food'] + ' 25g'
                # calculate calories
                kcal_bre = int(Staple_food_breakfast['Calories'] + 72 + Dairy_product['Calories'] + Fruit_breakfast[
                    'Calories'])
                kcal_lun = int(one_Staple_lunch['Calories'] +
                            Meat_lunch['Calories'] + Seafood_lunch['Calories']+ ve_cal_lunch + Juice[
                                   'Calories'])
                kcal_din = int(
                    one_Meat_dinner['Calories'] + one_seafood_dinner['Calories'] + Vegetables_dinner_one[
                        'Calories'] + ve_cal_dinner_1 + Nuts['Calories'] / 2)
                kcal_1day = kcal_bre + kcal_lun + kcal_din

                # calculate Protein
                pro_bre = int(
                    Staple_food_breakfast['Protein'] + 6 + Dairy_product['Protein'] + Fruit_breakfast['Protein'])
                pro_lun = int(one_Staple_lunch['Protein'] +
                            Meat_lunch['Protein'] + Seafood_lunch['Protein'] + ve_pro_lunch + Juice['Protein'])
                pro_din = int(
                    one_Meat_dinner['Protein'] + one_seafood_dinner['Protein'] + Vegetables_dinner_one[
                        'Calories'] + ve_pro_dinner_1 + Nuts['Protein'] / 2)
                pro_1day = pro_bre + pro_lun + pro_din

                # calculate Carbs
                carb_bre = int(
                    Staple_food_breakfast['Carbs'] + 0 + Dairy_product['Carbs'] + Fruit_breakfast['Carbs'])
                carb_lun = int(
                    one_Staple_lunch['Carbs'] + Meat_lunch['Carbs'] + Seafood_lunch['Carbs'] + ve_carb_lunch +
                    Juice['Carbs'])
                carb_din = int(one_Meat_dinner['Carbs'] + one_seafood_dinner['Carbs'] + Vegetables_dinner_one[
                    'Carbs'] + ve_carb_dinner_1 + Nuts['Carbs'] / 2)
                carb_1day = carb_bre + carb_lun + carb_din


        meal_plan = {'meal_plan': {'Breakfast': {'meal_plan': Breakfast_plan, 'kcal': kcal_bre, 'Protein': pro_bre, 'Carbs': carb_bre},
                                   'Lunch': {'meal_plan': Lunch_plan, 'kcal': kcal_lun, 'Protein': pro_lun, 'Carbs': carb_lun},
                                   'Dinner': {'meal_plan': Dinner_plan, 'kcal': kcal_din, 'Protein': pro_din, 'Carbs': carb_din}}, 'kcal': kcal_1day, 'Protein': pro_1day, 'Carbs': carb_1day}

        return meal_plan

    def fifty_plan(self, tag, one_dict):
        key_list = []
        for i in range(0,50):
            key_item = self.show_plan(self.tag, self.one_dict)
            key_list.append(key_item)
        return key_list



@app.route("/add", methods=["POST"], strict_slashes=False)
def add_articles():
    height = float(request.json['height'])
    weight = float(request.json['weight'])

    bmi = weight/((height/100)**2)

    # db.session.add(bmi)
    # db.session.commit()

    return jsonify({"bmi":bmi})

# @app.route("/recipe",methods=["GET","POST"])
# def any():
#     tag= (request.json["tags"])
#     可多选 [Low GI, Veg, Low Fat, High Protein, Low Carb, Halal] (inner join)
#     perfer = (request.json["food"])
#     单选 [Chicken, Beef, Fish, Pork, Seafood]
#     
#     search= request.json["keyword"]
@app.route("/recipe",methods=["POST"])
def all_tag_food_recipe():
    dict_name_list = ['', 'low_cal', 'low_GI', 'low_cal_GI', 'halal', 'low_cal_halal', 'low_GI_halal', 'low_cal_GI_halal', 'low_carb', 'low_cal_carb', 'low_GI_carb', 'low_cal_GI_carb', 'halal_low_carb', 'low_cal_halal_carb', 'low_GI_halal_carb', 'low_cal_GI_halal_carb']
    dict_list = [food_dict, food_dict_cal, food_dict_GI, food_dict_cal_GI, food_dict_halal, food_dict_cal_halal, food_dict_GI_halal, food_dict_cal_GI_halal, food_dict_carb, food_dict_cal_carb, food_dict_GI_carb, food_dict_cal_GI_carb, food_dict_halal_carb, food_dict_cal_halal_carb, food_dict_GI_halal_carb, food_dict_cal_GI_halal_carb]
    tag_list = ['normal', 'veg', 'high_protein']
    tag_recipe_pair = {}
    for i in range(0, len(dict_name_list)):
        for tag in tag_list:
            tag_name_pair = [tag, dict_name_list[i]]
            tag_name = "_".join(tag_name_pair)
            pair = Recipe(tag,dict_list[i])
            tag_recipe_pair[tag_name] = pair.fifty_plan(tag, dict_list[i])
            # tag_recipe_pair_json = json.dumps(tag_recipe_pair, ensure_ascii=False)
    return jsonify(tag_recipe_pair)

@app.route("/", methods=["GET"], strict_slashes=False)
def index():

    return jsonify({"HELLO": "WORLD"})

if __name__ == "__main__":
    app.run(debug=True)


