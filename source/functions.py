import tkinter as tk
import shutil
import os
import pathlib
from . import globals as glb


# function used for tree view mode, level defines
# the depth view
def walk_level(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for cur_root, dirs, files in os.walk(some_dir):
        yield cur_root, dirs, files
        num_sep_this = cur_root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def path_change(*event):
    # Clearing the list
    glb.list.delete(0, tk.END)

    for cur_root, dirs, files in walk_level(
        glb.current_path.get(), level=glb.tree_view_max_level
    ):
        cur_level = cur_root.replace(glb.current_path.get(), "").count(os.sep)
        indent = "  -> " * (cur_level - 1)
        if cur_level > 0:
            glb.list.insert(glb.list.size(), "{}{}/".format(indent, os.path.basename(cur_root)))
            glb.list.itemconfig(glb.list.size() - 1, bg="orange")
        subindent = "  -> " * cur_level

        if cur_level != glb.tree_view_max_level:
            for f in files:
                glb.list.insert(glb.list.size(), "{}{}".format(subindent, f))
                if os.access(os.path.join(cur_root, f), os.X_OK):
                    glb.list.itemconfig(glb.list.size() - 1, bg="green")


# Binding changes in this variable to the pathChange function
glb.current_path.trace("w", path_change)


def change_path_by_click(event=None):
    # Get path of clicked item
    path = get_path_of_selection()
    # Check if item is file, then open it
    if os.path.isfile(path):
        print("Opening: " + path)
        os.startfile(path)
    # Set new path -> trigger path_change function.
    else:
        glb.current_path.set(path)


# Binding path changing to double-click
# so that double click starts a file or opens a directory
glb.list.bind("<Double-1>", change_path_by_click)


# In this version view mode depth of view is
# fixed and can be 1 or 3. In future versions
# it will be possible to add a user prompt for
# custom depth of view
def change_view_mode():
    if glb.tree_view_max_level == 1:
        glb.tree_view_max_level = 3
    else:
        glb.tree_view_max_level = 1
    path_change()


def folder_up(event=None):
    # get the new path
    new_path = pathlib.Path(glb.current_path.get()).parent
    # set it to currentPath
    glb.current_path.set(new_path)
    # log message
    print("Going Back")


def open_popup():
    global top
    top = tk.Toplevel(glb.root)
    top.geometry("250x150")
    top.resizable(False, False)
    top.title("Child Window")
    top.columnconfigure(0, weight=1)
    tk.Label(top, text="Enter File or Folder name").grid()
    tk.Entry(top, textvariable=glb.new_file_name).grid(column=0, pady=10, sticky="NSEW")
    tk.Button(top, text="Create", command=new_file_or_folder).grid(pady=10, sticky="NSEW")


def new_file_or_folder():
    # check if it is a file name or a folder
    if len(glb.new_file_name.get().split(".")) != 1:
        open(os.path.join(glb.current_path.get(), glb.new_file_name.get()), "w").close()
    else:
        os.mkdir(os.path.join(glb.current_path.get(), glb.new_file_name.get()))
    # destroy the top
    top.destroy()
    path_change()


clipboard_path = os.path.join(pathlib.Path.cwd(), "clipboard")


def clear_clipboard():
    for filename in os.listdir(clipboard_path):
        file_path = os.path.join(clipboard_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def get_path_of_selection():
    picked_index = glb.list.curselection()[0]
    picked = glb.list.get(picked_index)
    if picked[-1] == "/":
        picked = picked[:-1]
    path_elements = [picked.split("->")[-1].strip()]
    cur_depth = picked.count("->")
    while cur_depth > 0:
        picked_index -= 1
        picked = glb.list.get(picked_index)
        if picked.count("->") < cur_depth:
            path_elements.append(picked.split("->")[-1].strip()[:-1])
            cur_depth -= 1
    path = glb.current_path.get()
    for i in path_elements[::-1]:
        path = os.path.join(path, i)
    print(path)
    return path


def copy_file():
    # Get clicked item.
    path = get_path_of_selection()

    if glb.current_path.get() == clipboard_path:
        print("Can't operate with files in clipboard directory")
        return

    # Check if item is file, then open it
    if os.path.isfile(path):
        clear_clipboard()
        print("Copying: " + path)
        shutil.copy(path, clipboard_path)
    # Set new path, will trigger pathChange function.
    else:
        print("Selection is not a file")


def cut_file():
    if glb.current_path.get() != clipboard_path:
        copy_file()
        delete_file()
    else:
        print("Can't operate with files in clipboard directory")


def insert_file():
    if glb.current_path == clipboard_path:
        print("Can't operate with files in clipboard directory")
        return
    path = glb.current_path.get()
    for filename in os.listdir(clipboard_path):
        shutil.copy(os.path.join(clipboard_path, filename), path)
    path_change()


def delete_file():
    # Get clicked item.
    path = get_path_of_selection()

    if glb.current_path.get() == clipboard_path:
        print("Can't operate with files in clipboard directory")
        return

    # Check if item is file, then open it
    if os.path.isfile(path):
        print("Deleting: " + path)
        os.remove(path)
    # Set new path, will trigger pathChange function.
    else:
        print("Selection is not a file")
    path_change()
