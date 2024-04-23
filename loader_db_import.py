import configparser
import pandas as pd
from sqlalchemy import create_engine
from load_100 import simulate_loading

# Config fájl beolvasása
config = configparser.ConfigParser()
config.read('config.ini')

# PostgreSQL adatbázis elérési útvonala config fájlból
db_username = config['postgresql']['username']
db_password = config['postgresql']['password']
db_host = config['postgresql']['host']
db_port = config['postgresql']['port']
db_name = config['postgresql']['dbname']

# PostgreSQL adatbázis elérési útja
db_path = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# Adatbázis motor létrehozása
engine = create_engine(db_path)
print("Adatbázis motor létrehozva")

# Pékség nevek tárolása
pekseg_nevek = ['algyo', 'arkad', 'morzsika', 'szechenyi', 'tesco', 'tisza']

def adatok_betoltese(pekseg_neve, engine):
    # SQL lekérdezés előkészítése a megadott pékség adatainak lekérésére
    query = f"SELECT * FROM {pekseg_neve}"
    
    # Adatok betöltése a DataFrame-be szeletelve a sorokat több részre
    chunk_size = 10000  # A szeletek mérete (állítsd be igény szerint)
    chunks = pd.read_sql(query, engine, chunksize=chunk_size)
    
    # Minden szeletet hozzáadjuk az eredményhez
    df = pd.concat(chunks)
    
    return df

# Adatok betöltése minden pékség táblából
pekseg_df_dict = {}
for pekseg_neve in pekseg_nevek:
    print(f"{pekseg_neve} tábla betöltése folyamatban...")
    simulate_loading(10)  # Betöltőcsík szimulálása
    pekseg_df_dict[pekseg_neve] = adatok_betoltese(pekseg_neve, engine)
    print(f"{pekseg_neve} tábla betöltése kész")

print("Adatok sikeresen betöltve")

# DataFrame-ek mentése modulként
import pickle

with open('pekseg_dataframes.pkl', 'wb') as f:
    pickle.dump(pekseg_df_dict, f)
