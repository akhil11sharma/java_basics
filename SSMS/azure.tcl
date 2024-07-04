import os
import pandas as pd
import pyodbc
from openpyxl import load_workbook

def table_exists(cursor, table_name):
    """
    Check if a table exists in the database.
    """
    query = f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
    cursor.execute(query)
    return cursor.fetchone()[0] == 1

def read_excel_with_merged_cells(file_path):
    """
    Read an Excel file with merged cells and return a DataFrame.
    """
    def merge_empty_columns(columns):
        """
        Function to merge consecutive empty columns into one until a non-empty column is encountered.
        """
        merged_cols = []
        current_col = ""
        for col in columns:
            if col:
                current_col = col
            merged_cols.append(current_col)
        return merged_cols

    wb = load_workbook(file_path, data_only=True)
    df = pd.DataFrame()
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        
        # Fill merged cells with their values
        for merged_cell in ws.merged_cells.ranges:
            first_cell = ws.cell(merged_cell.min_row, merged_cell.min_col)
            value = first_cell.value
            for row in ws.iter_rows(min_row=merged_cell.min_row, max_row=merged_cell.max_row, min_col=merged_cell.min_col, max_col=merged_cell.max_col):
                for cell in row:
                    cell.value = value
        
        data = ws.values
        cols = next(data)
        df = pd.DataFrame(data, columns=cols)
        break  # Assuming we only need the first sheet

    # Clean up column names, handling "Unnamed" and combining adjacent empty names
    df.columns = merge_empty_columns(df.columns)

    return df

def make_columns_unique(df):
    """
    Function to make column names unique by appending suffixes where necessary.
    """
    seen_columns = {}
    new_columns = []

    for col in df.columns:
        if col in seen_columns:
            suffix = 1
            new_col = f"{col}_{suffix}"
            while new_col in seen_columns:
                suffix += 1
                new_col = f"{col}_{suffix}"
            seen_columns[new_col] = 0
        else:
            new_col = col
            seen_columns[new_col] = 0

        new_columns.append(new_col)

    return new_columns

def import_excel_to_sql(input_folder, server_name, database_name):
    """
    Import Excel files from a folder into SQL Server database tables.
    """
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server_name};"
        f"DATABASE={database_name};"
        f"Trusted_Connection=yes;"
    )

    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        for file_name in os.listdir(input_folder):
            if file_name.startswith('~$'):
                continue  # Skip temporary files

            file_path = os.path.join(input_folder, file_name)
            
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                df = read_excel_with_merged_cells(file_path)
            else:
                continue  # Skip files that are not Excel files

            table_name = os.path.splitext(file_name)[0]
            table_name = table_name.replace(' ', '_').replace('-', '_').replace('.', '_')

            if table_exists(cursor, table_name):
                continue  # Skip if table already exists

            # Ensure all column names are unique with numeric suffixes
            new_columns = make_columns_unique(df)
            df.columns = new_columns

            # Create table with columns matching Excel headers
            columns_definition = ", ".join(f"[{col}] VARCHAR(MAX)" for col in df.columns)
            create_table_query = f"CREATE TABLE {table_name} ({columns_definition})"
            cursor.execute(create_table_query)

            # Insert data into SQL Server table
            for index, row in df.iterrows():
                row = ["" if pd.isna(x) else x for x in row]  # Convert NaNs to empty string for SQL insertion
                insert_query = f"INSERT INTO {table_name} ({', '.join(f'[{col}]' for col in df.columns)}) VALUES ({', '.join(['?']*len(df.columns))})"
                cursor.execute(insert_query, tuple(row))
            
            connection.commit()

        cursor.close()
        connection.close()
        print("Files imported successfully to SQL Server.")

    except Exception as e:
        print(f"Failed to import files to SQL Server: {e}")

if __name__ == "__main__":
    input_folder = r"C:\Users\Nikhil Sharma\Desktop\Internship"  # Replace with your input folder path
    server_name = 'DESKTOP-PLHJ2M7'
    database_name = 'test'
    import_excel_to_sql(input_folder, server_name, database_name)

