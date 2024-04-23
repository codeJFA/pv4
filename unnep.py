import pandas as pd
import pickle
from fx_main_test import select_and_filter_bakery_data
from data_filter_inter import filter_by_id_menu, filter_by_year, filter_by_month, filter_by_day, filter_by_hour, filter_columns
from utils import export_to_excel, export_to_excel_group

# DataFrame-ek betöltése a pickle fájlból
with open('pekseg_dataframes.pkl', 'rb') as f:
    pekseg_df_dict = pickle.load(f)

# Szűrők listája
selected_filters = []

# Interaktív választás a szűrők közül
print("Válassz a következő szűrők közül:")
print("1. ID menü alapján")
print("2. Év alapján")
print("3. Hónap alapján")
print("4. Nap alapján")
print("5. Óra alapján")
print("6. Oszlopok szerinti szűrés")

while True:
    try:
        selected_filter = int(input("Válassz egy számot a kívánt szűrőhöz: "))
        if selected_filter < 1 or selected_filter > 6:
            raise ValueError
        selected_filters.append(selected_filter)
        add_more = input("Szeretnél még egy szűrőt választani? (igen/nem): ")
        if add_more.lower() != 'igen':
            break
    except ValueError:
        print("Hibás bemenet. Kérlek, válassz érvényes számot.")

# Szűrt adatok csoportosítása "id_menu" oszlop alapján minden napra
def group_by_id_menu_within_day(dataframes):
    grouped_dataframes = {}
    for key, df in dataframes.items():
        # Az index átalakítása dátum formátumra, csak hónap, nap, év
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%m-%d-%Y')
        # Beállítjuk az új indexet a 'date' oszlopra
        df.set_index('date', inplace=True)
        # Csoportosítás nap és id_menu alapján
        grouped_data = df.groupby([df.index, 'id_menu'])
        # Hozzáadás a csoportosított DataFrame-ekhez
        grouped_dataframes[key] = grouped_data
    return grouped_dataframes


# DataFrame-ek kiválasztása és szűrése
selected_bakery_data = select_and_filter_bakery_data(pekseg_df_dict)

# Szűrők alkalmazása a DataFrame-ekre
filtered_dataframes = selected_bakery_data
for selected_filter in selected_filters:
    if selected_filter == 1:
        filtered_dataframes = filter_by_id_menu(filtered_dataframes)
    elif selected_filter == 2:
        filtered_dataframes = filter_by_year(filtered_dataframes)
    elif selected_filter == 3:
        filtered_dataframes = filter_by_month(filtered_dataframes)
    elif selected_filter == 4:
        filtered_dataframes = filter_by_day(filtered_dataframes)
    elif selected_filter == 5:
        filtered_dataframes = filter_by_hour(filtered_dataframes)
    elif selected_filter == 6:
        filtered_dataframes = filter_columns(filtered_dataframes)

# DataFrame-ek csoportosítása az "id_menu" oszlop alapján minden napra
grouped_dataframes = group_by_id_menu_within_day(filtered_dataframes)

# Kiírjuk az első néhány sort minden csoportosított DataFrame-nek
for key, group_df in grouped_dataframes.items():
    print(f"Csoportosított DataFrame '{key}':")
    for (date, id_menu), df in group_df:
        print(f"Dátum: {date}, ID menü: {id_menu}")
        print(df.head())

#Excel-fájl exportálása
excel_file_name = "grouped_bakery_data.xlsx"
export_to_excel_group(grouped_dataframes, excel_file_name)