import pandas as pd
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, '../output/all_company_data.csv')
all_data = pd.read_csv(my_file)
tech_data = all_data[all_data['finnhubIndustry'] == 'Technology'].reset_index()
tech_data.to_csv('../output/tech_company_data.csv')
