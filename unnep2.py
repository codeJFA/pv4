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

# Speciális feltétel alapján módosítás
for key, df in filtered_dataframes.items():
    # Kiírjuk az 'id_menu' oszlop értékeit
    print(f"'{key}' DataFrame 'id_menu' oszlop értékei:")
    print(df['id_menu'].unique())

    # Ha az 'id_menu' értéke '126', akkor szorozzuk meg a 'quantity' oszlopot 3-mal
    df.loc[df['id_menu'] == 126, 'quantity'] *= 3

    # Ellenőrizzük a módosítást
    print(f"Módosított DataFrame '{key}':")
    print(df[df['id_menu'] == 126][['id_menu', 'quantity']])

    # Módosított DataFrame kiíratása
    print(f"Módosított DataFrame '{key}':")
    print(df)

    # 'menu_id' érték alapján összegezzük az oszlopokat, csak azonos napokon
    # és hozzáadjuk az eredményeket egy új sorban
    special_rows = df[df['id_menu'].isin([126, 127])].groupby(['date']).agg({
        'quantity': 'sum',
        'price': 'sum',
        'amount': 'sum',
        'discount': 'sum',
        'paid': 'sum'
    }).reset_index()

    # Az új sorok hozzáadása az eredeti DataFrame-hez
    for index, row in special_rows.iterrows():
        new_row = row.copy()
        new_row['id_menu'] = '126+127'
        new_row['product'] = 'Combined Products'
        df = pd.concat([df, new_row.to_frame().transpose()], ignore_index=True)
        

    # Módosított DataFrame kiíratása
    print(f"Módosított DataFrame '{key}':")
    print(df)




#Excel-fájl exportálása

excel_file_name = "filtered_bakery_data.xlsx"
export_to_excel(filtered_dataframes, excel_file_name)
