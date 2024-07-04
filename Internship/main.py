import mysql.connector
import csv
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@123',
    'database': 'emprec'
}

def execute_query(query, params=None, fetch=False):
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        cursor = mydb.cursor()
        cursor.execute(query, params)
        if fetch:
            results = cursor.fetchall()
            return results
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def load_table_columns(table_name):
    columns_query = f"SHOW COLUMNS FROM `{table_name}`"
    columns = execute_query(columns_query, fetch=True)
    return [col[0] for col in columns]

def create_table_information_table(cursor):
    create_table_info_sql = """
    CREATE TABLE IF NOT EXISTS table_information (
        table_name VARCHAR(255) NOT NULL PRIMARY KEY,
        column_count INT NOT NULL,
        row_count INT NOT NULL DEFAULT 0
    )
    """
    cursor.execute(create_table_info_sql)

def insert_table_information(cursor, table_name, column_count, row_count):
    insert_sql = """
    INSERT INTO table_information (table_name, column_count, row_count) 
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
    column_count = %s, row_count = %s
    """
    cursor.execute(insert_sql, (table_name, column_count, row_count, column_count, row_count))

def compare_table_columns(cursor, table_name, expected_columns):
    cursor.execute(f"DESCRIBE `{table_name}`")
    existing_columns = [row[0] for row in cursor.fetchall()]
    
    extra_columns = [col for col in expected_columns if col not in existing_columns]
    missing_columns = [col for col in existing_columns if col not in expected_columns]
    
    if extra_columns:
        print(f"Extra columns in table '{table_name}': {extra_columns}")
    
    if missing_columns:
        print(f"Missing columns in table '{table_name}': {missing_columns}")

def process_files(cursor, folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        table_name = os.path.splitext(filename)[0]
        
        if filename.endswith('.csv'):
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                columns = next(csvreader)
                columns = [col.strip() for col in columns if col.strip()]
                
                if table_exists(cursor, table_name):
                    drop_table(cursor, table_name)
                
                create_table(cursor, table_name, columns)
                compare_table_columns(cursor, table_name, columns)
                
                data = [tuple(row) for row in csvreader]
                insert_data_into_table(cursor, table_name, columns, data)
                
                insert_table_information(cursor, table_name, len(columns), len(data))
                
                print(f"Table '{table_name}' replaced with new data from CSV.")
                    
        elif filename.endswith('.xlsx'):
            with pd.ExcelFile(file_path) as xls:
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    columns = df.columns.tolist()
                    columns = [col.strip() for col in columns if col.strip()]
                    
                    if table_exists(cursor, table_name):
                        drop_table(cursor, table_name)
                    
                    create_table(cursor, table_name, columns)
                    compare_table_columns(cursor, table_name, columns)
                    
                    data = [tuple(row) for row in df.values.tolist()]
                    insert_data_into_table(cursor, table_name, columns, data)
                    
                    insert_table_information(cursor, table_name, len(columns), len(data))
                    
                    print(f"Table '{table_name}' replaced with new data from Excel sheet.")

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    return result is not None

def drop_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")

def create_table(cursor, table_name, columns):
    columns = [col.strip() for col in columns if col.strip()]  
    create_table_sql = f"""
    CREATE TABLE `{table_name}` (
        {', '.join([f"`{col}` TEXT" for col in columns])}
    )
    """
    cursor.execute(create_table_sql)

def insert_data_into_table(cursor, table_name, columns, data):
    placeholders = ', '.join(['%s'] * len(columns))
    insert_sql = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in columns])}) VALUES ({placeholders})"
    cursor.executemany(insert_sql, data)

def fetch_data_from_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM `{table_name}`")
    rows = cursor.fetchall()
    return {tuple(row): row for row in rows}

def main():
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        cursor = mydb.cursor()
        create_table_information_table(cursor)
        folder_path = r'C:\Users\Nikhil Sharma\Desktop\testing'  

        while True:
            process_files(cursor, folder_path)
            mydb.commit()
            print("Files processed. Sleeping for 60 seconds...")
            time.sleep(60)

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if 'mydb' in locals() and mydb.is_connected():
            cursor.close()
            mydb.close()

def add_entry_fields():
    global entry_frame, add_button, update_button, delete_button, entry_vars

    for widget in entry_frame.winfo_children():
        widget.destroy()

    columns = load_table_columns(selected_table.get())
    entry_vars = {}

    for i, column in enumerate(columns):
        tk.Label(entry_frame, text=column).grid(row=0, column=i, padx=10, pady=5)
        entry_var = tk.StringVar()
        entry_vars[column] = entry_var
        entry = tk.Entry(entry_frame, textvariable=entry_var)
        entry.grid(row=1, column=i, padx=10, pady=5)

    add_button = tk.Button(entry_frame, text="Add Record", command=add_record)
    update_button = tk.Button(entry_frame, text="Update Record", command=update_record)
    delete_button = tk.Button(entry_frame, text="Delete Record", command=delete_record)
    save_button = tk.Button(entry_frame, text="Save to CSV", command=save_to_csv)

    add_button.grid(row=2, column=0, padx=10, pady=5)
    update_button.grid(row=2, column=1, padx=10, pady=5)
    delete_button.grid(row=2, column=2, padx=10, pady=5)
    save_button.grid(row=2, column=3, padx=10, pady=5)

def add_record():
    if selected_table.get():
        columns = load_table_columns(selected_table.get())
        values = [entry_vars[col].get() for col in columns]
        if all(values):
            columns_str = ', '.join([f"`{col}`" for col in columns])
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO `{selected_table.get()}` ({columns_str}) VALUES ({placeholders})"
            execute_query(query, values)
            refresh_table()
        else:
            messagebox.showwarning("Input Error", "All fields are required")

def update_record():
    if selected_table.get():
        columns = load_table_columns(selected_table.get())
        values = [entry_vars[col].get() for col in columns]
        if values[0]:
            set_clause = ', '.join([f"`{col}` = %s" for col in columns])
            query = f"UPDATE `{selected_table.get()}` SET {set_clause} WHERE `{columns[0]}` = %s"
            execute_query(query, values + [values[0]])
            refresh_table()
        else:
            messagebox.showwarning("Input Error", "Primary key is required")

def delete_record():
    if selected_table.get():
        primary_key = load_table_columns(selected_table.get())[0]
        primary_key_value = entry_vars[primary_key].get()
        if primary_key_value:
            query = f"DELETE FROM `{selected_table.get()}` WHERE `{primary_key}` = %s"
            execute_query(query, (primary_key_value,))
            refresh_table()
        else:
            messagebox.showwarning("Input Error", "Primary key is required")

def refresh_table():
    try:
        for i in tree.get_children():
            tree.delete(i)
    except tk.TclError:
        pass 

    if selected_table.get():
        columns = load_table_columns(selected_table.get())
        query = f"SELECT * FROM `{selected_table.get()}`"
        rows = execute_query(query, fetch=True)

        tree["columns"] = columns
        tree["show"] = "headings"

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        if rows:
            for row in rows:
                tree.insert("", "end", values=row)

def save_to_csv():
    if selected_table.get():
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            columns = load_table_columns(selected_table.get())
            query = f"SELECT * FROM `{selected_table.get()}`"
            rows = execute_query(query, fetch=True)
            if rows:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(columns)
                    csvwriter.writerows(rows)
                messagebox.showinfo("Save Complete", "Data saved successfully to CSV file.")
            else:
                messagebox.showwarning("No Data", "No data to save.")

def main_file_processor():
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        cursor = mydb.cursor()
        create_table_information_table(cursor)
        folder_path = r'C:\Users\Nikhil Sharma\Desktop\testing'  

        while True:
            process_files(cursor, folder_path)
            mydb.commit()
            print("Files processed. Sleeping for 60 seconds...")
            time.sleep(60)

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if 'mydb' in locals() and mydb.is_connected():
            cursor.close()
            mydb.close()

def main():
    global root, entry_frame, add_button, update_button, delete_button, tree, selected_table

    root = tk.Tk()
    root.title("Database Window")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    selected_table = tk.StringVar()
    table_list = execute_query("SHOW TABLES", fetch=True)
    table_names = [table[0] for table in table_list]
    selected_table.set(table_names[0])

    table_menu = tk.OptionMenu(frame, selected_table, *table_names, command=lambda _: add_entry_fields())
    table_menu.grid(row=0, column=0, padx=10, pady=5)
    tk.Button(frame, text="Load Table", command=refresh_table).grid(row=0, column=1, padx=10, pady=5)

    entry_frame = tk.Frame(frame)
    entry_frame.grid(row=1, column=0, columnspan=2, pady=10)

    tree_frame = tk.Frame(root)
    tree_frame.pack(padx=20, pady=10)
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree.pack()

    tree_scroll.config(command=tree.yview)

    add_entry_fields()
    refresh_table()

    root.mainloop()

if __name__ == "__main__":
    threading.Thread(target=main_file_processor).start()
    main()

