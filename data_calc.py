# calculations.py
import pandas as pd

def calculate_sum(dataframe):
    """
    Megjeleníti az összes numerikus oszlopot a DataFrame-ben, és lehetővé teszi a felhasználó számára, hogy kiválassza,
    melyik oszlopot szeretné összeadni.

    Args:
        dataframe (DataFrame): A DataFrame, amelyből az oszlopokat meg kívánjuk jeleníteni.

    Returns:
        float: Az összeg.
    """
    # Numerikus oszlopok kiválasztása
    numeric_columns = dataframe.select_dtypes(include=['number']).columns.tolist()
    
    # Numerikus oszlopok megjelenítése
    print("Elérhető numerikus oszlopok:")
    for i, column_name in enumerate(numeric_columns, start=1):
        print(f"{i}. {column_name}")
    
    # Felhasználó által választott oszlop kérése
    selected_column_index = int(input("Válassz egy oszlopot az összeadáshoz (szám megadása): ")) - 1
    
    if selected_column_index < 0 or selected_column_index >= len(numeric_columns):
        raise ValueError("Érvénytelen választás. Kérlek válassz egy érvényes oszlopot az összeadáshoz.")
    
    selected_column_name = numeric_columns[selected_column_index]
    
    # Összeadás az által kiválasztott oszlopon
    column_data = dataframe[selected_column_name]
    column_sum = column_data.sum()
    
    return column_sum
