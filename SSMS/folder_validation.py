import os
import tkinter as tk
from tkinter import messagebox, ttk

# Global variables
pdf_files = []
folder_path = r'C:\Users\Nikhil Sharma\Desktop\Internship'  # Replace with your folder path
file_combo = None

def check_pdf_files():
    global pdf_files, file_combo
    
    if not os.path.exists(folder_path):
        messagebox.showerror("Folder Not Found", f"The folder path '{folder_path}' does not exist.")
        return
    
    pdf_files.clear()  # Clear previous files
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.lower().endswith(".pdf"):
            pdf_files.append(filename)
    
    if not pdf_files:
        messagebox.showinfo("No PDF Files", "No PDF files found in the folder.")
    else:
        # Update combobox with pdf file names
        file_combo['values'] = pdf_files
        file_combo.current(0)  # Select the first item by default

def delete_selected_file():
    global pdf_files, file_combo, folder_path
    
    selected_file = file_combo.get()
    if not selected_file:
        messagebox.showwarning("No File Selected", "Please select a PDF file to delete.")
        return
    
    confirmation = messagebox.askyesno("Delete File", f"Do you want to delete the file '{selected_file}'?")
    if confirmation:
        try:
            os.remove(os.path.join(folder_path, selected_file))
            messagebox.showinfo("File Deleted", f"File '{selected_file}' deleted successfully.")
            # Refresh list after deletion
            check_pdf_files()
        except Exception as e:
            messagebox.showerror("Error Deleting File", f"Error deleting file '{selected_file}': {e}")

def delete_all_files():
    global pdf_files, folder_path
    
    if not pdf_files:
        messagebox.showinfo("No PDF Files", "No PDF files to delete.")
        return
    
    confirmation = messagebox.askyesno("Delete All Files", "Do you want to delete all PDF files in the folder?")
    if confirmation:
        try:
            for filename in pdf_files:
                os.remove(os.path.join(folder_path, filename))
            messagebox.showinfo("Files Deleted", "All PDF files deleted successfully.")
            # Refresh list after deletion
            check_pdf_files()
        except Exception as e:
            messagebox.showerror("Error Deleting Files", f"Error deleting files: {e}")

def periodic_check():
    check_pdf_files()
    root.after(10000, periodic_check)  # Check every 10 seconds

def create_gui():
    global file_combo
    
    global root
    root = tk.Tk()
    root.title("PDF Checker and Deleter")
    root.geometry("400x200")  # Set window size
    
    label = tk.Label(root, text="Select a PDF file to delete:")
    label.pack(pady=10)
    
    file_combo = ttk.Combobox(root, state='readonly')
    file_combo.pack(pady=10)
    
    check_pdf_files()
    
    delete_button = tk.Button(root, text="Delete Selected File", command=delete_selected_file)
    delete_button.pack(pady=10)
    
    delete_all_button = tk.Button(root, text="Delete All Files", command=delete_all_files)
    delete_all_button.pack(pady=10)
    
    periodic_check()  # Start periodic check
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
