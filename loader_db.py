import os
import pandas as pd
import config
from connect_DB import create_connection, close_connection, execute_query
import psycopg2

try:
    # Kapcsolat létrehozása az adatbázissal
    connection = create_connection()

    # UPDATA mappa tartalmának listázása
    updata_dir = "UPDATA"
    files = os.listdir(updata_dir)

    print("A rendelkezésre álló fájlok:")
    for idx, file in enumerate(files):
        print(f"{idx+1}. {file}")

    # Felhasználó által választott fájlok beolvasása
    file_indices = input("Kérem, válassza ki a fenti fájlok közül azok sorszámát, amelyeket feltöltene (vesszővel elválasztva): ").split(",")
    chosen_files = [files[int(idx) - 1] for idx in file_indices if 1 <= int(idx) <= len(files)]

    # Ha nincs kiválasztott fájl, kilépünk
    if not chosen_files:
        print("Nincs kiválasztott fájl.")
        exit()

    # Dátum ellenőrzési mód kiválasztása
    date_check_method = input("Kérem, válassza ki a dátum ellenőrzés módját (új/folytatás): ").strip().lower()

    # A kiválasztott fájlok elérési útjainak előkészítése
    file_paths = [os.path.join(updata_dir, file) for file in chosen_files]

    # Az összes kiválasztott fájl feldolgozása
    for file_path in file_paths:
        # Excel fájl beolvasása pandas segítségével
        excel_data = pd.read_excel(file_path)

        # Egyesített cellák kezelése
        excel_data = excel_data.ffill()

        # Az első oszlop alapján meghatározzuk a tábla nevét
        excel_data["shop"] = excel_data["shop"].map({
            "Algyő": "algyo",
            "Morzsika": "morzsika",
            "Rókusi": "tesco",
            "Széchenyi": "szechenyi",
            "Tisza Lajos": "tisza",
            "Árkád": "arkad"
        })

        # Az első oszlop szerint szétválogatjuk az adatokat az üzletekre
        grouped_data = excel_data.groupby("shop")

        # Adatok importálása a PostgreSQL adatbázisba az üzletek szerint szétválogatva
        for shop, shop_data in grouped_data:
            print(f"Üzlet: {shop}")

            # A tábla nevének meghatározása az üzlet alapján
            table_name = shop

            for idx, row in shop_data.iterrows():
                # Ha új fájl került feltöltésre, ellenőrizzük a dátumokat
                if date_check_method == "új":
                    date_value = row['date']
                    date_check_query = f"SELECT COUNT(*) FROM {table_name} WHERE date = %s"
                    cursor, connection = execute_query(connection, date_check_query, (date_value,))
                    count = cursor.fetchone()[0]

                    if count > 0:
                        print(f"A(z) {date_value} dátum már létezik a táblában, a sor nem lett beszúrva.")
                        continue

                # Ha nincs egyezés, akkor feltöltjük az adatokat
                columns = ",".join(shop_data.columns)
                placeholders = ",".join(["%s" for _ in range(len(shop_data.columns))])
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;"
                values = tuple(row)
                print("Inserting row:", idx+1)  # Az aktuális sor indexének kiírása
                cursor, connection = execute_query(connection, insert_query, values)

    print("Adatok importálva a PostgreSQL adatbázisba.")

except pd.errors.EmptyDataError:
    print("Az Excel fájl üres.")
except Exception as e:
    print("Általános hiba a fő kódban:", e)
finally:
    # Kapcsolat bezárása
    close_connection(connection)
