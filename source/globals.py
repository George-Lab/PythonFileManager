import tkinter as tk
import os
import pathlib

root = tk.Tk()

clipboard_path = os.path.join(pathlib.Path.cwd(), "clipboard")

# String variables
newFileName = tk.StringVar(root, "File.dot", "new_name")
currentPath = tk.StringVar(root, name="currentPath", value=pathlib.Path.cwd())


# List of files and folder
list = tk.Listbox(root)
list.grid(sticky="NSEW", column=1, row=1, rowspan=10, ipady=10, ipadx=10)

tree_view_max_level = 1