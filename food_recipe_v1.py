from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pymysql
import random
import json
pymysql.install_as_MySQLdb()


app = Flask(__name__)
CORS(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:adminadmin@database-2.coh1lexhr8xj.ap-northeast-1.rds.amazonaws.com' \
                                 ':3306/sys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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

# dictionary list of low calories/low GI/both low
food_dict_cal = []
food_dict_GI = []
food_dict_cal_GI = []
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

# randomly choose 1 Staple_food
def staple_food(one_dict):
    Staple_food_list = []
    for each in one_dict:
        if each['Bi_category'] == 'Staple_food':
            Staple_food_list.append(each)
    one_Staple_food = random.sample(Staple_food_list, 1)[0]
    return one_Staple_food

# randomly choose 1 Dairy_product
def dairy_product(one_dict):
    Dairy_products_list = []
    for each in one_dict:
        if each['Bi_category'] in ['Dairy_products_1','Dairy_products_2']:
            Dairy_products_list.append(each)
    one_Dairy_product = random.sample(Dairy_products_list, 1)[0]
    return one_Dairy_product

# randomly choose 1 Fruit_1
def fruit(one_dict):
    Fruit_list = []
    for each in one_dict:
        if each['Bi_category'] == 'Fruit_1':
            Fruit_list.append(each)
    one_Fruit = random.sample(Fruit_list, 1)[0]
    return one_Fruit

# randomly choose 1 Fruit_2
def juice(one_dict):
    juice_list = []
    for each in one_dict:
        if each['Bi_category'] == 'Fruit_2':
            juice_list.append(each)
    one_juice = random.sample(juice_list, 1)[0]
    return one_juice

# randomly choose 1 Meat
def meat(one_dict):
    Meat_list = []
    for each in one_dict:
        if each['Bi_category'] == 'Meat':
            Meat_list.append(each)
    one_Meat = random.sample(Meat_list, 1)[0]
    return one_Meat

# randomly choose 1 seafood
def seafood(one_dict):
    seafood_list = []
    for each in one_dict:
        if each['Bi_category'] == 'seafood' and each['Tag'] == 4:
            seafood_list.append(each)
    one_seafood = random.sample(seafood_list, 1)[0]
    return one_seafood

# randomly choose 5 Vegetables for salad
def vegetables_lunch(one_dict):
    Vegetables_list_1 = []
    for each in one_dict:
        if each['Bi_category'] == 'Vegetables' and each['Tag'] == 1:
            Vegetables_list_1.append(each)
    five_Vegetables = random.sample(Vegetables_list_1, 5)
    return five_Vegetables

# randomly choose 1 Vegetables from Tag 0
def vegetables_dinner(one_dict):
    Vegetables_list = []
    for each in one_dict:
        if each['Bi_category'] == 'Vegetables' and each['Tag'] == 0 :
            Vegetables_list.append(each)
    one_Vegetable = random.sample(Vegetables_list, 1)[0]
    return one_Vegetable

# randomly choose 1 Nuts
def nuts(one_dict):
    Nuts_list = []
    for each in one_dict:
        if each['Bi_category'] == 'Nuts':
            Nuts_list.append(each)
    one_Nut = random.sample(Nuts_list, 1)[0]
    return one_Nut

def show_plan(one_dict):
    Staple_food_breakfast = staple_food(one_dict)
    Dairy_product = dairy_product(one_dict)
    Fruit_breakfast = fruit(one_dict)
    Meat_lunch = meat(one_dict)
    Seafood_lunch = seafood(one_dict)
    Juice = juice(one_dict)
    Vegetables_dinner_one = vegetables_dinner(one_dict)
    Nuts = nuts(one_dict)

    Vegetables_lunch = vegetables_lunch(one_dict)
    five_Vegetables_list = [each['Food'] for each in Vegetables_lunch]
    five_Vegetables_cal = [each['Calories'] for each in Vegetables_lunch]
    ve_cal_lunch = sum(five_Vegetables_cal) / 2
    five_Vegetables_str = ','.join(five_Vegetables_list)
    Vegetables_lunch_str = five_Vegetables_str + ' (250-300g in total)'

    four_Vegetables_dinner = []
    for each in one_dict:
        if each['Bi_category'] == 'Vegetables' and each['Tag'] in [2, 3] and each['Food'] not in five_Vegetables_list:
            four_Vegetables_dinner.append(each)
    four_Vegetables = random.sample(four_Vegetables_dinner, 4)
    four_Vegetables_list = [each['Food'] for each in four_Vegetables]
    four_Vegetables_cal = [each['Calories'] for each in four_Vegetables]
    ve_cal_dinner_1 = sum(four_Vegetables_cal) / 2
    four_Vegetables_str = ','.join(four_Vegetables_list)
    four_Vegetables_dinner_str = four_Vegetables_str + ' (Boiled, steamed or baked, 200-250g in total)'

    Staple_food_lunch = []
    for each in one_dict:
        if each['Bi_category'] == 'Staple_food' and each['Food'] != Staple_food_breakfast['Food']:
            Staple_food_lunch.append(each)
    one_Staple_lunch = random.sample(Staple_food_lunch, 1)[0]

    Meat_dinner = []
    for each in one_dict:
        if each['Bi_category'] == 'Meat' and each['Food'] != Meat_lunch['Food']:
            Meat_dinner.append(each)
    one_Meat_dinner = random.sample(Meat_dinner, 1)[0]

    Seafood_dinner = []
    for each in one_dict:
        if each['Bi_category'] == 'seafood' and each['Tag'] == 4 and each['Food'] != Seafood_lunch['Food']:
            Seafood_dinner.append(each)
    one_seafood_dinner = random.sample(Seafood_dinner, 1)[0]

    # recipe
    Breakfast_plan = Staple_food_breakfast['Food']+ ' '+str(Staple_food_breakfast['Grams']) +'g; '\
                    + '1 egg; '\
                    + Dairy_product['Food'] + ' ' + Dairy_product['Unit'] +'; '\
                    + Fruit_breakfast['Unit'] + ' ' + Fruit_breakfast['Food'] + ' ' + str(Fruit_breakfast['Grams']) + 'g'
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

    meal_plan = {'meal_plan': {'Breakfast': {'meal_plan': Breakfast_plan, 'kcal': kcal_bre},
                               'Lunch': {'meal_plan': Lunch_plan, 'kcal': kcal_lun},
                               'Dinner': {'meal_plan': Dinner_plan, 'kcal': kcal_din}}, 'kcal': kcal_1day}
    meal_plan_json = json.dumps(meal_plan, ensure_ascii=False)
    return meal_plan_json
def show_vegetarian_plan(one_dict):
    Staple_food_breakfast = staple_food(one_dict)
    Dairy_product = dairy_product(one_dict)
    Fruit_breakfast = fruit(one_dict)
    Juice = juice(one_dict)
    Vegetables_dinner_one = vegetables_dinner(one_dict)
    Nuts = nuts(one_dict)

    Vegetables_lunch = vegetables_lunch(one_dict)
    five_Vegetables_list = [each['Food'] for each in Vegetables_lunch]
    five_Vegetables_cal = [each['Calories'] for each in Vegetables_lunch]
    ve_cal_lunch = sum(five_Vegetables_cal) * 0.65
    five_Vegetables_str = ','.join(five_Vegetables_list)
    Vegetables_lunch_str = five_Vegetables_str + ' (300-350g in total)'

    four_Vegetables_dinner = []
    for each in one_dict:
        if each['Bi_category'] == 'Vegetables' and each['Tag'] in [2, 3] and each['Food'] not in five_Vegetables_list:
            four_Vegetables_dinner.append(each)
    four_Vegetables = random.sample(four_Vegetables_dinner, 4)
    four_Vegetables_list = [each['Food'] for each in four_Vegetables]
    four_Vegetables_cal = [each['Calories'] for each in four_Vegetables]
    ve_cal_dinner_1 = sum(four_Vegetables_cal) * 0.8
    four_Vegetables_str = ','.join(four_Vegetables_list)
    four_Vegetables_dinner_str = four_Vegetables_str + ' (Boiled, steamed or baked, 300-350g in total)'

    Staple_food_lunch = []
    for each in one_dict:
        if each['Bi_category'] == 'Staple_food' and each['Food'] != Staple_food_breakfast['Food']:
            Staple_food_lunch.append(each)
    one_Staple_lunch = random.sample(Staple_food_lunch, 1)[0]

    Fruit_lunch_list = []
    for each in one_dict:
        if each['Bi_category'] == 'Fruit_1' and each['Food'] != Fruit_breakfast['Food']:
            Fruit_lunch_list.append(each)
    one_Fruit_lunch = random.sample(Fruit_lunch_list, 1)[0]
    one_Fruit_str_lunch = one_Fruit_lunch['Unit'] + ' ' + one_Fruit_lunch['Food'] + ' ' + str(one_Fruit_lunch['Grams'])

    Breakfast_plan = Staple_food_breakfast['Food']+ ' '+str(Staple_food_breakfast['Grams']) +'g; '\
                    + '1 egg; '\
                    + Dairy_product['Food'] + ' ' + Dairy_product['Unit'] +'; '\
                    + Fruit_breakfast['Unit'] + ' ' + Fruit_breakfast['Food'] + ' ' + str(Fruit_breakfast['Grams']) + 'g'
    Lunch_plan = one_Staple_lunch['Food']+ ' '+str(one_Staple_lunch['Grams']) +'g; '\
                + '1 egg; '\
                + 'Salad: ' + Vegetables_lunch_str +'; ' \
                + one_Fruit_str_lunch + 'g; ' \
                + Juice['Unit'] + ' ' + Juice['Food']
    Dinner_plan = '1 egg; '\
                + Vegetables_dinner_one['Food'] + ' (100g in total); '\
                + four_Vegetables_dinner_str + '; '\
                + Nuts['Food'] + ' 25g'
    #可选零食？

    # calculate calories
    kcal_bre = int(Staple_food_breakfast['Calories'] + 72 + Dairy_product['Calories'] + Fruit_breakfast['Calories'])
    kcal_lun = int(one_Staple_lunch['Calories'] + 72 + ve_cal_lunch + Juice['Calories'])
    kcal_din = int(72 + Vegetables_dinner_one['Calories'] + ve_cal_dinner_1 + Nuts['Calories'] / 2)
    kcal_1day = kcal_bre + kcal_lun + kcal_din

    meal_plan = {'meal_plan': {'Breakfast': {'meal_plan': Breakfast_plan, 'kcal': kcal_bre},
                               'Lunch': {'meal_plan': Lunch_plan, 'kcal': kcal_lun},
                               'Dinner': {'meal_plan': Dinner_plan, 'kcal': kcal_din}}, 'kcal': kcal_1day}
    meal_plan_json = json.dumps(meal_plan, ensure_ascii=False)
    return meal_plan_json

# show the recipes:
# no setting
print(show_plan(food_dict))

## low calories
print(show_plan(food_dict_cal))

## low GI
print(show_plan(food_dict_GI))

## both low calories and low GI
print(show_plan(food_dict_cal_GI))

## vegetarian
print(show_vegetarian_plan(food_dict))

## low calories and vegetarian
print(show_vegetarian_plan(food_dict_cal))

## low GI and vegetarian
print(show_vegetarian_plan(food_dict_GI))

### low calories low GI and vegetarian
print(show_vegetarian_plan(food_dict_cal_GI))