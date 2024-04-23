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

# Speciális feltételek alapján módosítás
for key, df in filtered_dataframes.items():
    # Ha az 'id_menu' értéke '126', akkor szorozzuk meg a 'quantity' oszlopot 3-mal
    df.loc[df['id_menu'] == 126, 'quantity'] *= 3
    # Ellenőrizzük a módosítást
    print(f"Módosított DataFrame '{key}':")
    print(df[df['id_menu'] == 126][['id_menu', 'quantity']])

    # Kiírjuk az 'id_menu' és 'product' oszlop értékeit
    print(f"'{key}' DataFrame 'id_menu' és 'product' oszlop értékei:")
    print(df[['id_menu', 'product']].drop_duplicates())

    # Új oszlop hozzáadása az új sorok jelöléséhez
    df['new_row'] = False

    # Új sorok hozzáadása speciális feltételek alapján
    special_rows_list = []
    for date, group in df.groupby('date'):
        # Ellenőrizzük, hogy az első két szó megegyezik-e a 'product' oszlopban
        product_first_words = group['product'].str.split().apply(lambda x: ' '.join(x[:2]))
        if product_first_words.nunique() == 1:
            # Ha minden termék első két szava megegyezik, hozzáadjuk az új sort
            combined_row = group.iloc[0].copy()
            combined_row['id_menu'] = ''.join(str(x) for x in sorted(group['id_menu'].unique()))
            combined_row['product'] = ' '.join(group.iloc[0]['product'].split()[:2])
            combined_row[['quantity', 'price', 'amount', 'discount', 'paid']] = group[['quantity', 'price', 'amount', 'discount', 'paid']].sum()
            special_rows_list.append((key, combined_row))
# Módosított DataFrame-ek előállítása a speciális sorok hozzáadásával
for key, row in special_rows_list:
    df = filtered_dataframes[key].copy()  # Eredeti DataFrame másolata
    df = pd.concat([df, row.to_frame().transpose()], ignore_index=True)  # Új sor hozzáadása

    # Új oszlop hozzáadása az új sorok jelöléséhez
    df['new_row'] = False  # Az új sorokhoz hozzáadott 'new_row' oszlop alapértelmezett értékkel

    row_index = df[df['date'] == row['date']].index[-1]  # Az utolsó hozzáadott sor indexe
    df.at[row_index, 'new_row'] = True

    filtered_dataframes[key] = df  # Az eredeti DataFrame frissítése az új DataFrame-mel

# Csak az igaz értékű new_row oszlopok megtartása
for key, df in filtered_dataframes.items():
    df = df.fillna(False)
    df = df.infer_objects(copy=False)
    filtered_dataframes[key] = df[df['new_row']]

# 'date' oszlopok átalakítása a '%m-%d-%Y' formátumba
for key, df in filtered_dataframes.items():
    df['date'] = pd.to_datetime(df['date'], format='%m-%d-%Y')

# Kiírjuk az első néhány sort minden módosított DataFrame-nek
for key, df in filtered_dataframes.items():
    print(f"Módosított DataFrame '{key}':")
    print(df.head())

# Excel-fájl exportálása
excel_file_name = "filtered_bakery_data.xlsx"
export_to_excel(filtered_dataframes, excel_file_name)

