def print_dataframe25(df):
        #printcolumns(df.columns, sort=False)
        print("\t".join(df.columns))
        # Csak az első 25 sor kiírása
        for index, row in df.head(25).iterrows():
            print("\t".join(str(row[coll]) for coll in df.columns))

    def print_dataframe(df):
    
        # Beállítjuk a pandas megjelenítési beállításait
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
    
        # Oszlopok neveinek kiírása
        print("\t".join(df.columns))
        
        # Sorok kiírása
        for index, row in df.head(10).iterrows():
            print("\t".join(str(row[coll]) for coll in df.columns))

    def print_dataframe_nettx(df):

        # Csak a 'product' és 'nett' oszlopok neveinek kiírása
        print("product", "nett", sep="\t")

        # Sorok kiírása
        for index, row in df.head(10).iterrows():
            print(row['product'], row['nett'], sep="\t")

    def print_dataframe_nett(df):
        # Csak a 'product' és 'nett' oszlopok neveinek kiírása
        headers = ['product', 'nett']

        # Sorok kiírása
        rows = []
        for index, row in df.head(10).iterrows():
            rows.append([row['product'], row['nett']])

        # Táblázat formázása a tabulate segítségével
        print(tabulate(rows, headers=headers, tablefmt="grid"))



    def print_status(df):
        print(df.head())
        print(df.info())
        print(df.describe())
        print(df.dtypes)
        print(df.shape)
        print(df.columns)
        print(df.index)
        print(df.values)
        print(df.size)
        print(df.empty)
        print(df.ndim)
        print(df.memory_usage())
        print(df.memory_usage(index=True).sum())
        print(df.memory_usage(deep=True))
        print(df.memory_usage(deep=True).sum())
        print(df.memory_usage(index=True))
        print(df.memory_usage(index=True).sum())
        print(df.memory_usage(deep=True, index=True))
        print(df.memory_usage(deep=True, index=True).sum())