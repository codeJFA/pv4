import os
import pandas as pd

def export_to_excel(dataframes_dict, file_name):
    """
    Exportálja a DataFrame-eket egy Excel-fájlba, külön sheet-ként.

    Args:
        dataframes_dict (dict): Egy dictionary, ahol a kulcsok a sheet nevek, az értékek pedig a DataFrame-ek.
        file_name (str): Az Excel-fájl neve, amibe exportálunk. A "export" mappába fogja menteni.
    """
    export_path = os.path.join("export", file_name)  # Az exportálási elérési út

    with pd.ExcelWriter(export_path) as writer:
        for sheet_name, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    export_choice = input("Szeretnéd exportálni az adatokat Excel-fájlba? (igen/nem): ")
    if export_choice.lower() == 'igen':
        print(f"A DataFrame sikeresen exportálva lett az '{export_path}' nevű Excel-fájlba.")
    elif export_choice.lower() == 'nem':
        print("Az adatok nem lettek exportálva Excel-fájlba.")
    else:
        print("Érvénytelen válasz. Az adatok nem lettek exportálva Excel-fájlba.")


def export_to_excel_group2(dataframes_dict, file_name):
    """
    Export DataFrames to an Excel file, each on a separate sheet.

    Args:
        dataframes_dict (dict): A dictionary where keys are sheet names and values are DataFrames.
        file_name (str): The name of the Excel file to export to. It will be saved in the "export" folder.
    """
    export_path = os.path.join("export", file_name)  # Export path

    with pd.ExcelWriter(export_path) as writer:
        for sheet_name, df in dataframes_dict.items():
            # Export each DataFrame as a separate sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    export_choice = input("Do you want to export the data to an Excel file? (yes/no): ")
    if export_choice.lower() == 'yes':
        print(f"The DataFrame has been successfully exported to the Excel file '{export_path}'.")
    elif export_choice.lower() == 'no':
        print("The data was not exported to an Excel file.")
    else:
        print("Invalid response. The data was not exported to an Excel file.")



def export_to_excel_group(dataframes_dict, file_name):
    """
    Export DataFrames to an Excel file, each on a separate sheet.

    Args:
        dataframes_dict (dict): A dictionary where keys are sheet names and values are DataFrames.
        file_name (str): The name of the Excel file to export to. It will be saved in the "export" folder.
    """
    export_path = os.path.join("export", file_name)  # Export path

    with pd.ExcelWriter(export_path) as writer:
        for sheet_name, df in dataframes_dict.items():
            # Export each DataFrame as a separate sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    export_choice = input("Do you want to export the data to an Excel file? (yes/no): ")
    if export_choice.lower() == 'yes':
        print(f"The DataFrame has been successfully exported to the Excel file '{export_path}'.")
    elif export_choice.lower() == 'no':
        print("The data was not exported to an Excel file.")
    else:
        print("Invalid response. The data was not exported to an Excel file.")






