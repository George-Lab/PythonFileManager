import tkinter as tk
import shutil
import os
import pathlib
from . import globals as glb


def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for cur_root, dirs, files in os.walk(some_dir):
        yield cur_root, dirs, files
        num_sep_this = cur_root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def pathChange(*event):
    # Clearing the list
    glb.list.delete(0, tk.END)

    for cur_root, dirs, files in walklevel(
        glb.currentPath.get(), level=glb.tree_view_max_level
    ):
        cur_level = cur_root.replace(glb.currentPath.get(), "").count(os.sep)
        indent = "  -> " * (cur_level - 1)
        if cur_level > 0:
            glb.list.insert(glb.list.size(), "{}{}/".format(indent, os.path.basename(cur_root)))
            glb.list.itemconfig(glb.list.size() - 1, bg="orange")
        subindent = "  -> " * (cur_level)

        if cur_level != glb.tree_view_max_level:
            for f in files:
                glb.list.insert(glb.list.size(), "{}{}".format(subindent, f))
                if os.access(os.path.join(cur_root, f), os.X_OK):
                    glb.list.itemconfig(glb.list.size() - 1, bg="green")

# Binding changes in this variable to the pathChange function
glb.currentPath.trace("w", pathChange)

def changePathByClick(event=None):
    # Get clicked item.
    path = getPathOfSelection()
    # Check if item is file, then open it
    if os.path.isfile(path):
        print("Opening: " + path)
        os.startfile(path)
    # Set new path, will trigger pathChange function.
    else:
        glb.currentPath.set(path)
# Binding path changing to double click
glb.list.bind("<Double-1>", changePathByClick)


def changeViewMode():
    if glb.tree_view_max_level == 1:
        glb.tree_view_max_level = 3
    else:
        glb.tree_view_max_level = 1
    pathChange()


def folderUp(event=None):
    # get the new path
    newPath = pathlib.Path(glb.currentPath.get()).parent
    # set it to currentPath
    glb.currentPath.set(newPath)
    # simple message
    print("Going Back")


def open_popup():
    global top
    top = tk.Toplevel(glb.root)
    top.geometry("250x150")
    top.resizable(False, False)
    top.title("Child Window")
    top.columnconfigure(0, weight=1)
    tk.Label(top, text="Enter File or Folder name").grid()
    tk.Entry(top, textvariable=glb.newFileName).grid(column=0, pady=10, sticky="NSEW")
    tk.Button(top, text="Create", command=newFileOrFolder).grid(pady=10, sticky="NSEW")


def newFileOrFolder():
    # check if it is a file name or a folder
    if len(glb.newFileName.get().split(".")) != 1:
        open(os.path.join(glb.currentPath.get(), glb.newFileName.get()), "w").close()
    else:
        os.mkdir(os.path.join(glb.currentPath.get(), glb.newFileName.get()))
    # destroy the top
    top.destroy()
    pathChange()


clipboard_path = os.path.join(pathlib.Path.cwd(), "clipboard")


def clearClipboard():
    for filename in os.listdir(clipboard_path):
        file_path = os.path.join(clipboard_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def getPathOfSelection():
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
    path = glb.currentPath.get()
    for i in path_elements[::-1]:
        path = os.path.join(path, i)
    print(path)
    return path


def copyFile():
    # Get clicked item.
    path = getPathOfSelection()

    if glb.currentPath.get() == clipboard_path:
        print("Can't operate with files in clipboard directory")
        return

    # Check if item is file, then open it
    if os.path.isfile(path):
        clearClipboard()
        print("Copying: " + path)
        shutil.copy(path, clipboard_path)
    # Set new path, will trigger pathChange function.
    else:
        print("Selection is not a file")


def cutFile():
    if glb.currentPath.get() != clipboard_path:
        copyFile()
        deleteFile()
    else:
        print("Can't operate with files in clipboard directory")


def insertFile():
    if glb.currentPath == clipboard_path:
        print("Can't operate with files in clipboard directory")
        return
    path = glb.currentPath.get()
    for filename in os.listdir(clipboard_path):
        shutil.copy(os.path.join(clipboard_path, filename), path)
    pathChange()


def deleteFile():
    # Get clicked item.
    path = getPathOfSelection()

    if glb.currentPath.get() == clipboard_path:
        print("Can't operate with files in clipboard directory")
        return

    # Check if item is file, then open it
    if os.path.isfile(path):
        print("Deleting: " + path)
        os.remove(path)
    # Set new path, will trigger pathChange function.
    else:
        print("Selection is not a file")
    pathChange()