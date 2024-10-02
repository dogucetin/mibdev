import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import platform

def select_folder1():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder1_entry.delete(0, tk.END)
        folder1_entry.insert(0, folder_path)

def select_folder2():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder2_entry.delete(0, tk.END)
        folder2_entry.insert(0, folder_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_path)

def concatenate_files(file_paths, output_file):
    """Concatenates files using system tools based on the OS."""
    if platform.system() == "Windows":
        # Using copy command for Windows
        with open(output_file, 'wb') as outfile:
            for fname in file_paths:
                with open(fname, 'rb') as infile:
                    outfile.write(infile.read())
    else:
        # Using cat command for Unix-like systems
        with open(output_file, 'wb') as outfile:
            for fname in file_paths:
                with open(fname, 'rb') as infile:
                    outfile.write(infile.read())

def merge_databases():
    folder1 = folder1_entry.get()
    folder2 = folder2_entry.get()
    output_folder = output_folder_entry.get()

    if not (folder1 and folder2 and output_folder):
        messagebox.showerror("Error", "Please select all folders.")
        return

    # Get lists of files in both folders
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)

    for file in set(files1).union(set(files2)):
        file1_path = os.path.join(folder1, file)
        file2_path = os.path.join(folder2, file)
        output_file_path = os.path.join(output_folder, file)

        try:
            if file in files1 and file in files2:
                # Both files exist, concatenate them
                file_paths = []
                if os.path.getsize(file1_path) > 0:
                    file_paths.append(file1_path)
                if os.path.getsize(file2_path) > 0:
                    file_paths.append(file2_path)

                if file_paths:
                    concatenate_files(file_paths, output_file_path)
                else:
                    # Create an empty file if both files are empty
                    open(output_file_path, 'a').close()

            elif file in files1:
                # If the file is only in folder1
                if os.path.getsize(file1_path) > 0:
                    with open(file1_path, 'rb') as infile, open(output_file_path, 'wb') as outfile:
                        outfile.write(infile.read())
                else:
                    # Create an empty file if it's empty
                    open(output_file_path, 'a').close()

            elif file in files2:
                # If the file is only in folder2
                if os.path.getsize(file2_path) > 0:
                    with open(file2_path, 'rb') as infile, open(output_file_path, 'wb') as outfile:
                        outfile.write(infile.read())
                else:
                    # Create an empty file if it's empty
                    open(output_file_path, 'a').close()

        except Exception as e:
            # Handle any other exceptions (optional logging)
            print(f"Error processing {file}: {e}")

    messagebox.showinfo("Success", "Merging complete!")

# Create main application window
root = tk.Tk()
root.title("SCOS2000 MIB Database Merger")

# Layout
folder1_label = tk.Label(root, text="Select Folder 1:")
folder1_label.pack()
folder1_entry = tk.Entry(root, width=50)
folder1_entry.pack()
folder1_button = tk.Button(root, text="Browse", command=select_folder1)
folder1_button.pack()

folder2_label = tk.Label(root, text="Select Folder 2:")
folder2_label.pack()
folder2_entry = tk.Entry(root, width=50)
folder2_entry.pack()
folder2_button = tk.Button(root, text="Browse", command=select_folder2)
folder2_button.pack()

output_folder_label = tk.Label(root, text="Select Output Folder:")
output_folder_label.pack()
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.pack()
output_folder_button = tk.Button(root, text="Browse", command=select_output_folder)
output_folder_button.pack()

merge_button = tk.Button(root, text="Merge Databases", command=merge_databases)
merge_button.pack()

# Start the application
root.mainloop()
