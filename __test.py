import pandas as pd

# A db_import modul betöltése
from loader_db_import import pekseg_df_dict

# A data_filter.py modulból importáljuk a szükséges függvényeket
from data_filter_inter import filter_dataframe_by_date_interactively, select_bakery_data, filter_dataframe_by_date_interactively_bakery

def első_5_sor_kiirasa(df):
    print(df.head())

# Pékség adatok kiválasztása a select_bakery_data függvénnyel
selected_bakery_data = select_bakery_data(pekseg_df_dict)

# DataFrame date oszlopának átalakítása Timestamp objektumokká
for df_name, df in selected_bakery_data.items():
    df['date'] = pd.to_datetime(df['date'])

# Szűrjük a DataFrame-et interaktív módon
filtered_dfs = filter_dataframe_by_date_interactively_bakery(selected_bakery_data)

# Kiírjuk az első 5 sort minden szűrt adatból
for name, df in filtered_dfs.items():
    print(f"-------- {name} pékség adatai --------")
    első_5_sor_kiirasa(df)

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