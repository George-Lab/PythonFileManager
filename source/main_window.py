import tkinter as tk
import os
import pathlib
import shutil

from source.functions import walk_level


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("File Manager")

        # # creating a frame and assigning it to container
        # container = tk.Frame(self, height=400, width=600)
        # # specifying the region where the frame is packed in root
        # container.pack(side="top", fill="both", expand=True)

        # String variables
        self.new_file_name = tk.StringVar(self, "File.dot", "new_name")
        self.current_path = tk.StringVar(self, name="currentPath", value=pathlib.Path.cwd())

        # List of files and folder
        self.list = tk.Listbox(self)
        self.list.grid(sticky="NSEW", column=1, row=1, rowspan=10, ipady=10, ipadx=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(10, weight=1)

        tk.Button(self, text="Folder Up", command=self.folder_up).grid(sticky="NSEW", column=0, row=0)
        # Keyboard shortcut for going up
        self.bind("<Alt-Up>", self.folder_up)

        tk.Button(self, text="Add File or Folder", command=self.open_popup).grid(
            sticky="NSEW", column=0, row=1, rowspan=1
        )

        tk.Button(self, text="Copy", command=self.copy_file).grid(
            sticky="NSEW", column=0, row=2, rowspan=1
        )

        tk.Button(self, text="Cut", command=self.cut_file).grid(
            sticky="NSEW", column=0, row=3, rowspan=1
        )

        tk.Button(self, text="Delete", command=self.delete_file).grid(
            sticky="NSEW", column=0, row=4, rowspan=1
        )

        tk.Button(self, text="Insert", command=self.insert_file).grid(
            sticky="NSEW", column=0, row=5, rowspan=1
        )

        tk.Button(self, text="View Mode", command=self.change_view_mode).grid(
            sticky="NSEW", column=0, row=6, rowspan=1
        )

        tk.Button(self, text="Quit", command=self.quit).grid(
            sticky="NSEW", column=0, row=7, rowspan=1
        )

        tk.Entry(self, textvariable=self.current_path).grid(
            sticky="NSEW", column=1, row=0, ipady=10, ipadx=10
        )

    def path_change(self, *event):
        # Clearing the list
        self.list.delete(0, tk.END)
        print(self.tree_view_max_level)

        for cur_root, dirs, files in walk_level(self.current_path.get(), level=self.tree_view_max_level):
            cur_level = cur_root.replace(self.current_path.get(), "").count(os.sep)
            indent = "  -> " * (cur_level - 1)
            if cur_level > 0:
                self.list.insert(self.list.size(), "{}{}/".format(indent, os.path.basename(cur_root)))
                self.list.itemconfig(self.list.size() - 1, bg="orange")
            subindent = "  -> " * cur_level

            if cur_level != self.tree_view_max_level:
                for f in files:
                    self.list.insert(self.list.size(), "{}{}".format(subindent, f))
                    if os.access(os.path.join(cur_root, f), os.X_OK):
                        self.list.itemconfig(self.list.size() - 1, bg="green")

    def change_path_by_click(self, event=None):
        # Get path of clicked item
        path = self.get_path_of_selection()
        # Check if item is file, then open it
        if os.path.isfile(path):
            print("Opening: " + path)
            os.startfile(path)
        # Set new path -> trigger path_change function.
        else:
            self.current_path.set(path)

    # In this version view mode depth of view is
    # fixed and can be 1 or 3. In future versions
    # it will be possible to add a user prompt for
    # custom depth of view
    def change_view_mode(self):
        if self.tree_view_max_level == 1:
            self.tree_view_max_level = 3
        else:
            self.tree_view_max_level = 1
        self.path_change()

    def folder_up(self, event=None):
        # get the new path
        new_path = pathlib.Path(self.current_path.get()).parent
        # set it to currentPath
        self.current_path.set(new_path)
        # log message
        print("Going Back")

    def open_popup(self, event=None):
        global top
        top = tk.Toplevel(self)
        top.geometry("250x150")
        top.resizable(False, False)
        top.title("Child Window")
        top.columnconfigure(0, weight=1)
        tk.Label(top, text="Enter File or Folder name").grid()
        tk.Entry(top, textvariable=self.new_file_name).grid(column=0, pady=10, sticky="NSEW")
        tk.Button(top, text="Create", command=self.new_file_or_folder).grid(pady=10, sticky="NSEW")

    def new_file_or_folder(self, *event):
        # check if it is a file name or a folder
        if len(self.new_file_name.get().split(".")) != 1:
            open(os.path.join(self.current_path.get(), self.new_file_name.get()), "w").close()
        else:
            os.mkdir(os.path.join(self.current_path.get(), self.new_file_name.get()))
        # destroy the top
        top.destroy()
        self.path_change()

    def clear_clipboard(self):
        for filename in os.listdir(self.clipboard_path):
            file_path = os.path.join(self.clipboard_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def get_path_of_selection(self):
        picked_index = self.list.curselection()[0]
        picked = self.list.get(picked_index)
        if picked[-1] == "/":
            picked = picked[:-1]
        path_elements = [picked.split("->")[-1].strip()]
        cur_depth = picked.count("->")
        while cur_depth > 0:
            picked_index -= 1
            picked = self.list.get(picked_index)
            if picked.count("->") < cur_depth:
                path_elements.append(picked.split("->")[-1].strip()[:-1])
                cur_depth -= 1
        path = self.current_path.get()
        for i in path_elements[::-1]:
            path = os.path.join(path, i)
        print(path)
        return path

    def copy_file(self):
        # Get clicked item.
        path = self.get_path_of_selection()

        if self.current_path.get() == self.clipboard_path:
            print("Can't operate with files in clipboard directory")
            return

        # Check if item is file, then open it
        if os.path.isfile(path):
            self.clear_clipboard()
            print("Copying: " + path)
            shutil.copy(path, self.clipboard_path)
        # Set new path, will trigger pathChange function.
        else:
            print("Selection is not a file")

    def cut_file(self):
        if self.current_path.get() != self.clipboard_path:
            self.copy_file()
            self.delete_file()
        else:
            print("Can't operate with files in clipboard directory")

    def insert_file(self):
        if self.current_path == self.clipboard_path:
            print("Can't operate with files in clipboard directory")
            return
        path = self.current_path.get()
        for filename in os.listdir(self.clipboard_path):
            shutil.copy(os.path.join(self.clipboard_path, filename), path)
        self.path_change()

    def delete_file(self):
        # Get clicked item.
        path = self.get_path_of_selection()

        if self.current_path.get() == self.clipboard_path:
            print("Can't operate with files in clipboard directory")
            return

        # Check if item is file, then open it
        if os.path.isfile(path):
            print("Deleting: " + path)
            os.remove(path)
        # Set new path, will trigger pathChange function.
        else:
            print("Selection is not a file")
        self.path_change()

    # variable storing path to clipboard
    clipboard_path = os.path.join(pathlib.Path.cwd(), "clipboard")

    # variable defining max depth of tree view mode
    tree_view_max_level = 1
