import pandas as pd
import pyodbc
import os
import tkinter as tk
from tkinter import messagebox, ttk
import time
import threading

DB_CONFIG = {
    'server': 'DESKTOP-PLHJ2M7',
    'database': 'test',
    'trusted_connection': 'yes'
}

# Specify the folder path here
FOLDER_PATH = r"C:\Users\Nikhil Sharma\Desktop\Internship"

def get_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
    )
    return pyodbc.connect(connection_string)

def execute_query(query, params=None, fetch=False):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params if params else ())
        if fetch:
            results = cursor.fetchall()
            return results
        conn.commit()
    except pyodbc.Error as err:
        print(f"SQL Server Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def create_table_information_table(cursor):
    create_table_info_sql = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='table_information' and xtype='U')
    CREATE TABLE table_information (
        table_name NVARCHAR(255) NOT NULL PRIMARY KEY,
        column_count INT NOT NULL,
        row_count INT NOT NULL DEFAULT 0
    )
    """
    cursor.execute(create_table_info_sql)

def insert_table_information(cursor, table_name, column_count, row_count):
    insert_sql = """
    IF EXISTS (SELECT * FROM table_information WHERE table_name = ?)
        UPDATE table_information
        SET column_count = ?, row_count = ?
        WHERE table_name = ?
    ELSE
        INSERT INTO table_information (table_name, column_count, row_count)
        VALUES (?, ?, ?)
    """
    cursor.execute(insert_sql, (table_name, column_count, row_count, table_name, table_name, column_count, row_count))

def compare_table_columns(cursor, table_name, expected_columns):
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", (table_name,))
    existing_columns = [row[0] for row in cursor.fetchall()]
    
    extra_columns = [col for col in expected_columns if col not in existing_columns]
    missing_columns = [col for col in existing_columns if col not in expected_columns]
    
    if extra_columns:
        print(f"Extra columns in table '{table_name}': {extra_columns}")
    
    if missing_columns:
        print(f"Missing columns in table '{table_name}': {missing_columns}")

def process_files_in_folder():
    if not FOLDER_PATH or not os.path.isdir(FOLDER_PATH):
        messagebox.showerror("Error", "Please provide a valid folder path.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        create_table_information_table(cursor)

        iteration_count = 0

        while True:
            iteration_count += 1

            for filename in os.listdir(FOLDER_PATH):
                file_path = os.path.join(FOLDER_PATH, filename)
                table_name = os.path.splitext(filename)[0].replace("-", "_")  # Replace hyphen with underscore

                if filename.endswith('.csv'):
                    df = pd.read_csv(file_path)
                    columns = df.columns.tolist()

                    if table_exists(cursor, table_name):
                        drop_table(cursor, table_name)

                    create_table(cursor, table_name, columns)
                    compare_table_columns(cursor, table_name, columns)

                    # Convert columns to str type to avoid float issues
                    df = df.astype(str)

                    data = df.values.tolist()
                    insert_data_into_table(cursor, table_name, columns, data)

                    insert_table_information(cursor, table_name, len(columns), len(data))

                    print(f"Table '{table_name}' replaced with new data from CSV.")

                elif filename.endswith('.xlsx'):
                    with pd.ExcelFile(file_path) as xls:
                        for sheet_name in xls.sheet_names:
                            df = pd.read_excel(xls, sheet_name=sheet_name)
                            columns = df.columns.tolist()

                            if table_exists(cursor, table_name):
                                drop_table(cursor, table_name)

                            create_table(cursor, table_name, columns)
                            compare_table_columns(cursor, table_name, columns)

                            # Convert columns to str type to avoid float issues
                            df = df.astype(str)

                            data = df.values.tolist()
                            insert_data_into_table(cursor, table_name, columns, data)

                            insert_table_information(cursor, table_name, len(columns), len(data))

                            print(f"Table '{table_name}' replaced with new data from Excel sheet.")

            conn.commit()
            print(f"Iteration Count: {iteration_count}. Last update: {time.strftime('%H:%M:%S')}")

            print(f"Files processed. Sleeping for 30 seconds...")
            time.sleep(30)

    except pyodbc.Error as err:
        print(f"SQL Server Error: {err}")

    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()

def table_exists(cursor, table_name):
    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", (table_name,))
    result = cursor.fetchone()
    return result is not None

def drop_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS [{table_name}]")

def create_table(cursor, table_name, columns):
    columns = [col.strip() for col in columns if col.strip()]
    create_table_sql = f"""
    CREATE TABLE [{table_name}] (
        {', '.join([f"[{col}] NVARCHAR(MAX)" for col in columns])}
    )
    """
    cursor.execute(create_table_sql)

def insert_data_into_table(cursor, table_name, columns, data):
    placeholders = ', '.join(['?'] * len(columns))
    insert_sql = f"INSERT INTO [{table_name}] ({', '.join([f'[{col}]' for col in columns])}) VALUES ({placeholders})"
    cursor.executemany(insert_sql, data)

def start_processing():
    threading.Thread(target=process_files_in_folder).start()

def end_program():
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Folder File Processor")
    root.geometry("600x200")

    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    start_button = ttk.Button(frame, text="Start Processing", command=start_processing)
    start_button.pack(pady=10)

    count_label = ttk.Label(frame, text="Iteration Count: 0")
    count_label.pack(pady=10)

    end_button = ttk.Button(frame, text="End Program", command=end_program)
    end_button.pack(pady=10)

    root.mainloop()
