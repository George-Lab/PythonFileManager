import tkinter as tk
import os
import pathlib

root = tk.Tk()

# variable storing path to clipboard
clipboard_path = os.path.join(pathlib.Path.cwd(), "clipboard")

# String variables
new_file_name = tk.StringVar(root, "File.dot", "new_name")
current_path = tk.StringVar(root, name="currentPath", value=pathlib.Path.cwd())


# List of files and folder
list = tk.Listbox(root)
list.grid(sticky="NSEW", column=1, row=1, rowspan=10, ipady=10, ipadx=10)

# variable defining max depth of tree view mode
tree_view_max_level = 1