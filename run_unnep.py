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


# Szűrők alkalmazása a DataFrame-ekre
for key, df in filtered_dataframes.items():
    # Csoportosítás 'date' és 'id_menu' alapján, majd oszlopok összegzése napi szinten
    grouped = df.groupby(['date', 'id_menu', 'product']).agg({
        'quantity': 'sum',
        'price': 'sum',
        'amount': 'sum',
        'discount': 'sum',
        'paid': 'sum'
    }).reset_index()

    # Csak a kívánt oszlopok megtartása
    grouped = grouped[['date', 'id_menu', 'product',
                       'quantity', 'price', 'amount', 'discount', 'paid']]

    # Az új DataFrame-et elmentjük az eredeti helyére
    filtered_dataframes[key] = grouped

special_rows_list = []

# Speciális feltétel alapján módosítás
for key, df in filtered_dataframes.items():
    # Ha az 'id_menu' értéke '126', akkor szorozzuk meg a 'quantity' oszlopot 3-mal
    df.loc[df['id_menu'] == 126, 'quantity'] *= 3
    df.loc[df['id_menu'] == 128, 'quantity'] *= 1
    df.loc[df['id_menu'] == 169, 'quantity'] *= 2

    # Ellenőrizzük a módosítást
    print(f"Módosított DataFrame '{key}':")
    print(df[df['id_menu'] == 126][['id_menu', 'quantity']])
    # Kiírjuk az 'id_menu' és 'product' oszlop értékeit
    print(f"'{key}' DataFrame 'id_menu' és 'product' oszlop értékei:")
    print(df[['id_menu', 'product']].drop_duplicates())

    # Új sorok hozzáadása speciális feltételek alapján
    for menu_ids in [(126, 127, '126127'), (128, 129, '128129'), (169, 170, '169170')]:
        special_rows = df[df['id_menu'].isin(menu_ids[:2])].groupby(['date']).agg({
            'quantity': 'sum',
            'price': 'sum',
            'amount': 'sum',
            'discount': 'sum',
            'paid': 'sum'
        }).reset_index()

        # Az új sorok hozzáadása az eredeti DataFrame-hez
        for index, row in special_rows.iterrows():
            new_row = row.copy()
            new_row['id_menu'] = menu_ids[2]
            new_row['product'] = 'Combined Products'
            special_rows_list.append((key, new_row))


# Módosított DataFrame-ek előállítása a speciális sorok hozzáadásával
for key, row in special_rows_list:
    df = filtered_dataframes[key]
    df = pd.concat([df, row.to_frame().transpose()], ignore_index=True)
    filtered_dataframes[key] = df
    
    # Kitöröljük azokat a sorokat, amelyeknek az 'products' oszlop értéke nem kezdődik 'Combined' szóval
    if 'product' in df.columns and df['product'].dtype == 'object':
        df = df[df['product'].str.startswith('Combined')]
    # Frissítjük a DataFrame-et a módosított verzióval
    filtered_dataframes[key] = df


    
# 'date' oszlopok átalakítása a '%m-%d-%Y' formátumba
for key, df in filtered_dataframes.items():
    df['date'] = pd.to_datetime(df['date'], format='%m-%d-%Y')

# Kiírjuk az első néhány sort minden módosított DataFrame-nek
for key, df in filtered_dataframes.items():
    print(f"Módosított DataFrame '{key}':")
    print(df.head())

#Excel-fájl exportálása

excel_file_name = "filtered_bakery_data.xlsx"
export_to_excel(filtered_dataframes, excel_file_name)
