from source.main_window import MainWindow


# Main Function
def main():
    app = MainWindow()

    # Binding changes in this variable to the pathChange function
    app.current_path.trace("w", app.path_change)

    # Binding path changing to double-click
    # so that double click starts a file or opens a directory
    app.list.bind("<Double-1>", app.change_path_by_click)

    app.path_change("")
    app.mainloop()
