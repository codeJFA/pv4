import pandas as pd
import calendar

def filter_by_id_menu(df_dict):
    """
    Interaktívan szűri az összes DataFrame-et az 'id_menu' oszlop alapján.

    Args:
        df_dict (dict): Egy szótár, amely a DataFrame-eket tartalmazza pékségnevekkel azonosítva.

    Returns:
        dict: Egy szótár, amely a szűrt DataFrame-eket tartalmazza.
    """
    selected_dfs = {}

    # Kiírjuk a felhasználónak a szűrési feltételek kérése előtt
    print("Kérlek, add meg a szűrési feltételeket az 'id_menu' oszlop alapján:")
    id_menu_conditions = input("Példa: '1,2,3' vagy '1-3,5,7-9' (vesszővel és/vagy kötőjellel elválasztva): ")

    # Feltételek feldolgozása
    conditions = []
    for cond in id_menu_conditions.split(","):
        if "-" in cond:
            start, end = map(int, cond.split("-"))
            conditions.extend(range(start, end + 1))
        else:
            conditions.append(int(cond))

    # Szűrés minden DataFrame-re
    for name, df in df_dict.items():
        filtered_df = df[df['id_menu'].isin(conditions)]
        selected_dfs[name] = filtered_df

    return selected_dfs

def filter_by_year(df_dict):
    """
    Interaktívan szűri az összes DataFrame-et a 'year_p' oszlop alapján.

    Args:
        df_dict (dict): Egy szótár, amely a DataFrame-eket tartalmazza pékségnevekkel azonosítva.

    Returns:
        dict: Egy szótár, amely a szűrt DataFrame-eket tartalmazza.
    """
    # Lehetőségek listázása
    years = sorted(set(year for df in df_dict.values() for year in df['year_p'].unique()))
    print("Válassz az alábbi évek közül:")
    for i, year in enumerate(years, start=1):
        print(f"{i}. {year}")

    # Szűrési feltételek beolvasása
    selected_years = []
    while True:
        try:
            selected_indices = input("Válassz egy vagy több számot (vesszővel elválasztva): ")
            selected_indices = [int(index.strip()) for index in selected_indices.split(",")]
            for index in selected_indices:
                if index < 1 or index > len(years):
                    raise ValueError
            selected_years = [years[index - 1] for index in selected_indices]
            break
        except ValueError:
            print("Hibás bemenet. Kérlek, válassz érvényes számokat.")

    # Szűrés minden DataFrame-re
    selected_dfs = {}
    for name, df in df_dict.items():
        filtered_df = df[df['year_p'].isin(selected_years)]
        selected_dfs[name] = filtered_df

    return selected_dfs

def filter_by_month(df_dict):
    """
    Interaktívan szűri az összes DataFrame-et a 'month_p' oszlop alapján.

    Args:
        df_dict (dict): Egy szótár, amely a DataFrame-eket tartalmazza pékségnevekkel azonosítva.

    Returns:
        dict: Egy szótár, amely a szűrt DataFrame-eket tartalmazza.
    """
    # Lehetőségek listázása
    months = sorted(set(month for df in df_dict.values() for month in df['month_p'].unique()), key=lambda m: list(calendar.month_name).index(m))
    print("Válassz az alábbi hónapok közül:")
    for i, month in enumerate(months, start=1):
        print(f"{i}. {month}")

    # Szűrési feltételek beolvasása
    selected_months = []
    while True:
        try:
            selected_indices = input("Válassz egy vagy több számot (vesszővel elválasztva): ")
            selected_indices = [int(index.strip()) for index in selected_indices.split(",")]
            for index in selected_indices:
                if index < 1 or index > len(months):
                    raise ValueError
            selected_months = [months[index - 1] for index in selected_indices]
            break
        except ValueError:
            print("Hibás bemenet. Kérlek, válassz érvényes számokat.")

    # Szűrés minden DataFrame-re
    selected_dfs = {}
    for name, df in df_dict.items():
        filtered_df = df[df['month_p'].isin(selected_months)]
        selected_dfs[name] = filtered_df

    return selected_dfs


def filter_by_day(df_dict):
    """
    Interaktívan szűri az összes DataFrame-et a 'day_p' oszlop alapján.

    Args:
        df_dict (dict): Egy szótár, amely a DataFrame-eket tartalmazza pékségnevekkel azonosítva.

    Returns:
        dict: Egy szótár, amely a szűrt DataFrame-eket tartalmazza.
    """
    # Hét napjainak sorrendje
    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Lehetőségek listázása és rendezése
    days = sorted(set(day for df in df_dict.values() for day in df['day_p'].unique()), key=lambda d: week_days.index(d))
    
    # Lehetőségek kiíratása
    print("Válassz az alábbi napok közül:")
    for i, day in enumerate(days, start=1):
        print(f"{i}. {day}")

    # Szűrési feltételek beolvasása interaktív módon
    while True:
        selected_indices = input("Válassz egy vagy több napot (vesszővel elválasztva, pl. '1,3'): ")
        selected_indices = [int(index.strip()) for index in selected_indices.split(",")]
        selected_days = [days[index - 1] for index in selected_indices if 1 <= index <= len(days)]
        if selected_days:
            break
        else:
            print("Hibás bemenet. Kérlek, válassz érvényes napokat.")

    # Szűrés minden DataFrame-re
    selected_dfs = {name: df[df['day_p'].isin(selected_days)] for name, df in df_dict.items()}

    return selected_dfs

def filter_by_hour(df_dict):
    """
    Interaktívan szűri az összes DataFrame-et az 'hour_p' oszlop alapján.

    Args:
        df_dict (dict): Egy szótár, amely a DataFrame-eket tartalmazza pékségnevekkel azonosítva.

    Returns:
        dict: Egy szótár, amely a szűrt DataFrame-eket tartalmazza.
    """
    # Lehetőségek listázása
    hours = sorted(set(hour for df in df_dict.values() for hour in df['hour_p'].unique()))
    print("Válassz az alábbi órák közül:")
    for i, hour in enumerate(hours, start=1):
        print(f"{i}. {hour}")

    # Szűrési feltételek beolvasása
    selected_hours = []
    while True:
        try:
            selected_indices = input("Válassz egy vagy több számot (vesszővel elválasztva): ")
            selected_indices = [int(index.strip()) for index in selected_indices.split(",")]
            for index in selected_indices:
                if index < 1 or index > len(hours):
                    raise ValueError
            selected_hours = [hours[index - 1] for index in selected_indices]
            break
        except ValueError:
            print("Hibás bemenet. Kérlek, válassz érvényes számokat.")

    # Szűrés minden DataFrame-re
    selected_dfs = {}
    for name, df in df_dict.items():
        filtered_df = df[df['hour_p'].isin(selected_hours)]
        selected_dfs[name] = filtered_df

    return selected_dfs

def filter_columns(df_dict, selected_columns=None):
    """
    Interaktívan szűri az összes DataFrame-et az oszlopok alapján.

    Args:
        df_dict (dict): Egy szótár, amely a DataFrame-eket tartalmazza pékségnevekkel azonosítva.
        selected_columns (list): Az előzőleg kiválasztott oszlopok listája.

    Returns:
        dict: Egy szótár, amely a szűrt DataFrame-eket tartalmazza.
    """
    if selected_columns is None:
        # Ha nincs előzőleg kiválasztott oszlop, akkor kérjük be a felhasználótól
        selected_columns = []
        # Lehetőségek kiíratása egyszer
        print("Válassz az alábbi oszlopok közül:")
        first_df = next(iter(df_dict.values()))
        columns = first_df.columns.tolist()
        for i, col in enumerate(columns, start=1):
            print(f"{i}. {col}")

        # Szűrési feltételek beolvasása egyszer
        while True:
            selected_indices = input("Válassz egy vagy több oszlopot (vesszővel elválasztva, pl. '1,3'): ")
            selected_indices = [int(index.strip()) for index in selected_indices.split(",")]
            selected_columns.extend([columns[index - 1] for index in selected_indices if 1 <= index <= len(columns)])
            if selected_columns:
                break
            else:
                print("Hibás bemenet. Kérlek, válassz érvényes oszlopokat.")

    # Szűrés minden DataFrame-re
    selected_dfs = {}
    for name, df in df_dict.items():
        # DataFrame oszlopok kiválasztása
        selected_df = df[selected_columns]
        selected_dfs[name] = selected_df

    return selected_dfs




# Példa használat:
if __name__ == "__main__":
    # Pékség DataFrame-ek példányosítása (például pekseg1, pekseg2)
    # df_dict = {"pekseg1": pekseg1_df, "pekseg2": pekseg2_df}
    # Szűrés az 'id_menu' oszlop alapján
    # selected_dfs = filter_by_id_menu(df_dict)
    pass  # Ha a kód önállóan fut, akkor a példák nem futnak le, csak importáláskor.
