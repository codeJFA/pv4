import pandas as pd
import pickle
from fx_main import select_and_filter_bakery_data, run_data_filter_inter
from data_filter_inter import filter_by_id_menu, filter_by_year, filter_by_month, filter_by_day, filter_by_hour, filter_columns
from utils import export_to_excel

# DataFrame-ek betöltése a pickle fájlból
with open('pekseg_dataframes.pkl', 'rb') as f:
    pekseg_df_dict = pickle.load(f)

# selected_bakery_data DataFrame létrehozása a select_and_filter_bakery_data függvénnyel
selected_bakery_data = select_and_filter_bakery_data(pekseg_df_dict)

print(selected_bakery_data.keys())

# Szűrjük az összes DataFrame-et az 'id_menu' oszlop alapján
#filtered_dataframes = filter_by_id_menu(selected_bakery_data)

# Szűrjük az összes DataFrame-et az 'year_p' oszlop alapján
#filtered_dataframes = filter_by_year(selected_bakery_data)

# Szűrjük az összes DataFrame-et az '(month_p)' oszlop alapján
#filtered_dataframes = filter_by_month(selected_bakery_data)

# Szűrjük az összes DataFrame-et az '(hour_p)' oszlop alapján
#filtered_dataframes = filter_by_hour(selected_bakery_data)

selected_filters = ['filter_by_id_menu', 'filter_by_year', 'filter_by_month', 'filter_by_day', 'filter_by_hour']


filtered_dataframes = run_data_filter_inter(selected_bakery_data, selected_filters)

filtered_dataframes = filter_columns(selected_bakery_data)



# Kiírjuk az első néhány sort minden szűrt DataFrame-nek
for key, df in filtered_dataframes.items():
    print(f"DataFrame '{key}':")
    print(df.head())
