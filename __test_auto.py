import pandas as pd
import pickle
from fx_main_test import select_and_filter_bakery_data
from data_filter_inter import filter_by_id_menu, filter_by_year, filter_by_month, filter_by_day, filter_by_hour, filter_columns
from utils import export_to_excel, export_to_excel_group
import difflib
from itertools import combinations

# DataFrame-ek betöltése a pickle fájlból
with open('pekseg_dataframes.pkl', 'rb') as f:
    pekseg_df_dict = pickle.load(f)

# Function to calculate similarity percentage between two strings
def similarity_percentage(str1, str2):
    seq = difflib.SequenceMatcher(None, str1, str2)
    return seq.ratio() * 100

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
    print(grouped.head())

# Iterate through each DataFrame
for key, df in filtered_dataframes.items():
    # Group rows by date
    grouped = df.groupby('date')
    # Iterate through groups
    for date, group in grouped:
        # min 65% hasonlóság a végződés 'eg' + 'sz' vagy min 65% hasonlóság a kezdő 'HF' + 'EL'
        for (idx1, row1), (idx2, row2) in combinations(group.iterrows(), 2):
            similarity = similarity_percentage(row1['product'], row2['product'])
            endsid1 = row1['product'].endswith('eg' or 'sz')
            endsid2 = row2['product'].endswith('sz' or 'eg')
            starid1 = row1['product'].startswith('EL' or 'HF')
            starid2 = row2['product'].startswith('HF' or 'EL')
            
            if (similarity >= 70 and endsid1 and endsid2) or (similarity >= 70 and starid1 and starid2):
         
                # Itt folytathatod a kódodat, ha mindkét feltétel teljesül
                # Merge values into the first row
                #idx1 az index, amelyre hivatkozunk
                # row2 az a sor, amelyből az id_menu értékét hozzá szeretnénk adni az idx1 indexű sorhoz
                # Az alábbi sorral az eredeti értékhez fűzzük a row2-ben lévő értéket
                df.loc[idx1, 'date'] = row2['date']
                df.loc[idx1, 'id_menu'] = str(df.loc[idx1, 'id_menu']) + str(row2['id_menu'])
                df.loc[idx1, 'product'] += ', ' + row2['product']
                df.loc[idx1, 'quantity'] += row2['quantity']
                df.loc[idx1, 'price'] += row2['price']
                df.loc[idx1, 'amount'] += row2['amount']
                df.loc[idx1, 'discount'] += row2['discount']
                df.loc[idx1, 'paid'] += row2['paid']

    # Csak a kívánt oszlopok megtartása
    filtered_dataframes[key] = df[['date', 'id_menu', 'product',
                                    'quantity', 'price', 'amount', 'discount', 'paid']]

    print(df.head())


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
