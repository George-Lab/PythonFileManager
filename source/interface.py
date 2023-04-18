import tkinter as tk

from . import functions as fnc
from . import globals as glb

# set a title for the file explorer main window
glb.root.title("File Manager")

glb.root.grid_columnconfigure(1, weight=1)
glb.root.grid_rowconfigure(10, weight=1)


tk.Button(glb.root, text="Folder Up", command=fnc.folder_up).grid(sticky="NSEW", column=0, row=0)
# Keyboard shortcut for going up
glb.root.bind("<Alt-Up>", fnc.folder_up)

tk.Button(glb.root, text="Add File or Folder", command="").grid(
    sticky="NSEW", column=0, row=1, rowspan=1
)

tk.Button(glb.root, text="Copy", command=fnc.copy_file).grid(
    sticky="NSEW", column=0, row=2, rowspan=1
)

tk.Button(glb.root, text="Cut", command=fnc.cut_file).grid(
    sticky="NSEW", column=0, row=3, rowspan=1
)

tk.Button(glb.root, text="Delete", command=fnc.delete_file).grid(
    sticky="NSEW", column=0, row=4, rowspan=1
)

tk.Button(glb.root, text="Insert", command=fnc.insert_file).grid(
    sticky="NSEW", column=0, row=5, rowspan=1
)

tk.Button(glb.root, text="View Mode", command=fnc.change_view_mode).grid(
    sticky="NSEW", column=0, row=6, rowspan=1
)

tk.Button(glb.root, text="Quit", command=glb.root.quit).grid(
    sticky="NSEW", column=0, row=7, rowspan=1
)

tk.Entry(glb.root, textvariable=glb.current_path).grid(
    sticky="NSEW", column=1, row=0, ipady=10, ipadx=10
)
