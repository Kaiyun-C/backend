import pandas as pd

# dia = pd.read_csv("Type_2_prevalence.csv")
# print(dia)
# dia_year_sex_p = dia[['Year','Males.1','Females.1','Persons.1']]
# dia_year_sex_p.columns = ['year', 'males', 'females','persons']
# print(dia_year_sex_p)
# dia_year_sex_p.to_csv('Type_2_prevalence_yearsex.csv',index=False)

# comp = pd.read_csv("complications_sex.csv")
# print(comp)
#
# comp_sex = comp[['Number of complications','Males.2','Females.2','Persons.2']]
# comp_sex.columns = ['Number_of_complications', 'Males', 'Females','Persons']
# print(comp_sex)
# comp_sex.to_csv('cleanned_complications_sex.csv',index=False)


# comp = pd.read_csv("complications_sex.csv")
# print(comp)

# comp_sex = comp[['Number of complications','Males','Females','Persons']]
# comp_sex.columns = ['Number_of_complications', 'Males', 'Females','Persons']
# print(comp_sex)
# comp_sex.to_csv('cleanned_complications_sex_number.csv',index=False)

cal = pd.read_csv("food_data_v2.csv")
cal_nona = cal.dropna(axis=1, how='all')  # drop na
cols = range(1, 10)
cal_nona.drop(cal_nona.columns[cols], axis=1, inplace=True)  # keep the needed
cal_new = cal_nona.replace('#VALUE!', 0)  # set #VALUE! to 0
cal_new.columns = ['Food', 'Bi_category', 'Tag', 'Unit', 'Grams', 'Calories',
                   'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs', 'GI', 'GI_level']  # rename
cal_new.to_csv('clanned_calories.csv', index=False)
