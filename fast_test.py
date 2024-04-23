import pandas as pd
import importlib
import os
import shutil


import pandas as pd

def select_and_filter_bakery_data(pekseg_df_dict):
    """
    Kiválasztja, melyik pékség vagy pékségek adatait szeretnénk használni, majd interaktívan szűri a DataFrame-eket
    egy adott időszak alapján a "date" oszlop szerint.

    Args:
        pekseg_df_dict (dict): A pékség DataFrame-eket tartalmazó szótár.

    Returns:
        dict: Egy dictionary, amely a szűrt DataFrame-eket tartalmazza, kulcsként a pékségnevekkel.
    """
    pekseg_nevek = list(pekseg_df_dict.keys())
    kivalasztott_pekseg_nevek = []

    # print("Kérlek, válassz egy vagy több pékséget a következők közül:")
    # for i, pekseg_neve in enumerate(pekseg_nevek, start=1):
    #     print(f"{i}. {pekseg_neve}")

    # print(f"{len(pekseg_nevek) + 1}. Minden pékség")

    # valasztottak = [2, 4, 5, 6]  # Alapértelmezett választások
    valasztottak = "2, 4, 5, 6"

    valasztottak = [int(val.strip()) for val in valasztottak.split(",")]
    
    valasztott_pékségek = []
    total_df = pd.DataFrame()  # Összesített "TOTAL" DataFrame inicializálása

    for val in valasztottak:
        if val == len(pekseg_nevek) + 1:
            valasztott_pékségek.extend(list(pekseg_df_dict.values()))
            total_df = pd.concat(list(pekseg_df_dict.values()))  # Összesített "TOTAL" DataFrame létrehozása
        else:
            pekseg_nev = pekseg_nevek[val - 1]
            kivalasztott_pekseg_nevek.append(pekseg_nev)
            valasztott_pékségek.append(pekseg_df_dict[pekseg_nev])
            total_df = pd.concat([total_df, pekseg_df_dict[pekseg_nev]])  # Összesített "TOTAL" DataFrame frissítése

    # A kiválasztott pékségek adatait tartalmazó dictionary összeállítása
    kivalasztott_péksegek_adatok = {pekseg_nev: df for pekseg_nev, df in zip(kivalasztott_pekseg_nevek, valasztott_pékségek)}
    kivalasztott_péksegek_adatok["TOTAL"] = total_df  # "TOTAL" DataFrame hozzáadása a dictionary-hez

    # DataFrame date oszlopának átalakítása Timestamp objektumokká
    for df_name, df in kivalasztott_péksegek_adatok.items():
        df['date'] = pd.to_datetime(df['date'])

    # Ellenőrizzük, hogy van-e 'date' oszlop a DataFrame-ekben
    for name, df in kivalasztott_péksegek_adatok.items():
        if 'date' not in df.columns:
            raise ValueError(f"A(z) '{name}' pékség DataFrame-je nem tartalmaz 'date' nevű oszlopot!")

    # Interaktívan szűrjük a DataFrame-eket egy adott időszak alapján
    szurt_dfs = {}
    # kulonbozo_datumok = "nem"  # Állandó választás: nem
    # if kulonbozo_datumok.lower() == 'igen':
    #     for name, df in kivalasztott_péksegek_adatok.items():
    #         print(f"Interaktív szűrés {name} pékség adataira:")
    #         kezdo_ev = input("Kérem, adja meg a kezdő évét (pl. 2024): ") or "2023"
    #         kezdo_ho = input("Kérem, adja meg a kezdő hónapot (pl. 01): ") or "03"
    #         kezdo_nap = input("Kérem, adja meg a kezdő napot (pl. 01): ") or "01"
    #         veg_ev = input("Kérem, adja meg a végdátum évét (pl. 2024): ") or "2023"
    #         veg_ho = input("Kérem, adja meg a végdátum hónapot (pl. 12): ") or "03"
    #         veg_nap = input("Kérem, adja meg a végdátum napot (pl. 31): ") or "05"
    #         kezdo_datum = pd.Timestamp(f"{kezdo_ev}-{kezdo_ho}-{kezdo_nap}")
    #         veg_datum = pd.Timestamp(f"{veg_ev}-{veg_ho}-{veg_nap}")
    #         szurt_df = df[(df['date'] >= kezdo_datum) & (df['date'] <= veg_datum)]
    #         szurt_dfs[name] = szurt_df
    # else:
    kezdo_ev = "2023"
    kezdo_ho = "03"
    kezdo_nap = "01"
    veg_ev = "2023"
    veg_ho = "03"
    veg_nap = "05"
    kezdo_datum = pd.Timestamp(f"{kezdo_ev}-{kezdo_ho}-{kezdo_nap}")
    veg_datum = pd.Timestamp(f"{veg_ev}-{veg_ho}-{veg_nap}")
    for name, df in kivalasztott_péksegek_adatok.items():
        szurt_df = df[(df['date'] >= kezdo_datum) & (df['date'] <= veg_datum)]
        szurt_dfs[name] = szurt_df

    # Új dictionary létrehozása a szűrt DataFrame-ekkel
    default_filter = {}
    for key, value in szurt_dfs.items():
        default_filter [key] = value.copy()

    return default_filter
