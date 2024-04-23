import configparser
import pandas

def read_db_config(filename='config.ini', section='postgresql'):
    """
    Beolvassa a konfigurációs fájlt és visszaadja a kapcsolódási adatokat.
    """
    # Create a parser
    parser = configparser.ConfigParser()
    # Read config file
    parser.read(filename)

    # Get section, default to database
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db_config

config = read_db_config()
dbname = config['dbname']
user = config['username']
password = config['password']
host = config['host']
port = config['port']

# Most már ezekkel az adatokkal hozhatod létre a kapcsolatot vagy folytathatod az adatbázisműveleteket.

#Mappa rendszer előkszítése:


