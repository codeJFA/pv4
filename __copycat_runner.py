import pandas as pd
import pickle
from fast_test import select_and_filter_bakery_data
from data_filter_inter import filter_by_id_menu, filter_by_year, filter_by_month, filter_by_day, filter_by_hour, filter_columns
from utils import export_to_excel, export_to_excel_group
import difflib
from itertools import combinations
import re
from tabulate import tabulate


def run_your_code():
    # Itt található a fő kód és a print üzenet
    print("Ez egy fontos üzenet, amit ki kell írni!")


    # DataFrame-ek betöltése a pickle fájlból
    with open('pekseg_dataframes.pkl', 'rb') as f:
        pekseg_df_dict = pickle.load(f)

    # Function to calculate similarity percentage between two strings
    def similarity_percentage(str1, str2):
        seq = difflib.SequenceMatcher(None, str1, str2)
        return seq.ratio() * 100

    def print_first_last_rows(df):
        # Csak a 'product' és 'nett' oszlopok neveinek kiírása
        headers = df.columns.tolist()

        # Az első 10 sor kiírása
        first_rows = df.head(10).values.tolist()

        # Az utolsó 10 sor kiírása
        last_rows = df.tail(10).values.tolist()

        # Táblázat formázása a tabulate segítségével
        print("First 10 rows:")
        print(tabulate(first_rows, headers=headers, tablefmt="grid"))
        print("\nLast 10 rows:")
        print(tabulate(last_rows, headers=headers, tablefmt="grid"))

        

    # Reguláris kifejezés a numerikus számok kereséséhez
    numeric_only = re.compile(r'\d+')

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
        
        # 'quantity' oszlop értékeinek vizsgálata, csak egész számok esetén hozzáadja a 'nett' oszlopot
        if (grouped['quantity'] % 1 == 0).all():
            # A 'product' oszlop értékeinek tisztítása és 'nett' oszlop hozzáadása
            grouped['nett'] = grouped['product'].str.replace('eg', '').replace('sz', '').replace('EL', '').replace('HF', '')
            grouped['nett'] = grouped['nett'].str.extract('(\d+)').astype(float)  # Kiszűrés csak a számokból
            grouped['nett'] = grouped['nett'].astype(float)  # 'nett' oszlop értékének float típusúvá alakítása

            # Eredmény mentése
            filtered_dataframes[key] = grouped

            # Az első és utolsó sorok kiírása
            print_first_last_rows(grouped)




        


if __name__ == "__main__":
    run_your_code()

    # Iterate through each DataFrame
    for key, df in filtered_dataframes.items():
        grouped = df.groupby('date')
        for date, group in grouped:
            for (idx1, row1), (idx2, row2) in combinations(group.iterrows(), 2):
                similarity = similarity_percentage(row1['product'], row2['product'])
                endsid1 = row1['product'].endswith(('eg', 'sz'))
                endsid2 = row2['product'].endswith(('sz', 'eg'))
                starid1 = row1['product'].startswith(('EL', 'HF'))
                starid2 = row2['product'].startswith(('HF', 'EL'))
                
                if (similarity >= 67 and endsid1 and endsid2) or (similarity >= 67 and starid1 and starid2):
                    combined_id = str(df.loc[idx1, 'id_menu']) + "/" + str(row2['id_menu'])
                    
                    df.loc[idx1, 'id_menu'] = combined_id
                    df.loc[idx1, 'id_menu2'] = combined_id.replace("/", "")
                    df.loc[idx1, 'merged'] = 'M+'
                    df.loc[idx1, 'product'] += ', ' + row2['product']
                    cleared_row1 = row1['product'].replace('eg', '').replace('sz', '').replace('EL', '').replace('HF', '')
                    df.loc[idx1, 'product_c'] = cleared_row1
                    cleared_nett = "".join(numeric_only.findall(cleared_row1))
                    df.loc[idx1, 'nett'] = cleared_nett
                    df.loc[idx1, 'quantity'] += row2['quantity']
                    df.loc[idx1, 'price'] += row2['price']
                    df.loc[idx1, 'amount'] += row2['amount']
                    df.loc[idx1, 'discount'] += row2['discount']
                    df.loc[idx1, 'paid'] += row2['paid']


        # Csak a kívánt oszlopok megtartása
        filtered_dataframes[key] = df[['date', 'id_menu', 'id_menu2', 'merged', 'product_c', 'product', 'nett',
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
