import tkinter as tk
from tkinter import filedialog, messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.root.geometry("600x400")

        # Create a Text widget (for editing the text)
        self.text_area = tk.Text(self.root, wrap="word", undo=True)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open...", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Exit", command=self.exit_editor)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)

    def new_file(self):
        """Clear the current text area for a new file."""
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        """Open an existing file."""
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        """Save the current file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def exit_editor(self):
        """Exit the editor."""
        if messagebox.askokcancel("Quit", "Do you want to exit without saving?"):
            self.root.quit()

    def undo(self):
        """Undo last action."""
        try:
            self.text_area.edit_undo()
        except Exception as e:
            print("Undo Error:", e)

    def redo(self):
        """Redo last undone action."""
        try:
            self.text_area.edit_redo()
        except Exception as e:
            print("Redo Error:", e)


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
