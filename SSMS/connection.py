import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyodbc
import threading
import pandas as pd

# SQL Server configuration
DB_CONFIG = {
    'server': 'DESKTOP-PLHJ2M7',     # Replace with your SQL Server instance name
    'database': 'test', # Replace with your database name
    'trusted_connection': 'yes',      # Use Windows authentication (trusted connection)
}

# Function to execute SQL queries
def execute_query(query, params=None, fetch=False):
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={DB_CONFIG["server"]};'
            f'DATABASE={DB_CONFIG["database"]};'
            'Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
        else:
            connection.commit()
        
        cursor.close()
        connection.close()
    except pyodbc.Error as err:
        messagebox.showerror("Error", f"SQL Server Error: {err}")

# Function to load column names for a given table
def load_table_columns(table_name):
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
    columns = execute_query(query, fetch=True)
    return [col[0] for col in columns]

# Function to add entry fields based on selected table columns
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

    add_button.grid(row=2, column=0, padx=10, pady=5)
    update_button.grid(row=2, column=1, padx=10, pady=5)
    delete_button.grid(row=2, column=2, padx=10, pady=5)

# Function to add a record to the selected table
def add_record():
    if selected_table.get():
        columns = load_table_columns(selected_table.get())
        values = [entry_vars[col].get() for col in columns]
        
        if all(values):
            columns_str = ', '.join([f"[{col}]" for col in columns])
            placeholders = ', '.join(['?'] * len(columns))
            query = f"INSERT INTO [{selected_table.get()}] ({columns_str}) VALUES ({placeholders})"
            execute_query(query, values)
            refresh_table()
        else:
            messagebox.showwarning("Input Error", "All fields are required")

# Function to update a record in the selected table
def update_record():
    if selected_table.get():
        columns = load_table_columns(selected_table.get())
        values = [entry_vars[col].get() for col in columns]
        
        if values[0]:  # Assuming the first column is the primary key
            set_clause = ', '.join([f"[{col}] = ?" for col in columns[1:]])
            query = f"UPDATE [{selected_table.get()}] SET {set_clause} WHERE [{columns[0]}] = ?"
            execute_query(query, values[1:] + [values[0]])
            refresh_table()
        else:
            messagebox.showwarning("Input Error", "Primary key is required")

# Function to delete a record from the selected table
def delete_record():
    if selected_table.get():
        primary_key = load_table_columns(selected_table.get())[0]  # Assuming the first column is the primary key
        primary_key_value = entry_vars[primary_key].get()
        
        if primary_key_value:
            query = f"DELETE FROM [{selected_table.get()}] WHERE [{primary_key}] = ?"
            execute_query(query, (primary_key_value,))
            refresh_table()
        else:
            messagebox.showwarning("Input Error", "Primary key is required")

# Function to refresh the table view
def refresh_table():
    try:
        for i in tree.get_children():
            tree.delete(i)
    except tk.TclError:
        pass

    if selected_table.get():
        columns = load_table_columns(selected_table.get())
        query = f"SELECT * FROM [{selected_table.get()}]"
        rows = execute_query(query, fetch=True)

        tree["columns"] = columns
        tree["show"] = "headings"

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        if rows:
            for row in rows:
                tree.insert("", "end", values=row)

# Function to initialize the GUI
def main():
    global root, entry_frame, tree, selected_table

    root = tk.Tk()
    root.title("SSMS Database GUI")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    selected_table = tk.StringVar()
    table_list = execute_query("SELECT name FROM sys.tables", fetch=True)
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
    main()
