import tkinter as tk
from tkinter import filedialog, messagebox
from predict import main as predict_text
import threading
import time

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor with Autocomplete")
        self.root.geometry("800x600")

        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Create text widget
        self.text_area = tk.Text(self.main_frame, wrap="word", undo=True, font=("Arial", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Create suggestion label
        self.suggestion_label = tk.Label(
            self.main_frame,
            text="",
            fg="gray",
            bg="white",
            font=("Arial", 12),
            anchor="w"
        )

        # Bind events
        self.text_area.bind('<KeyRelease>', self.on_text_change)
        self.text_area.bind('<Tab>', self.complete_text)
        self.text_area.bind('<Return>', self.clear_suggestion)
        self.text_area.bind('<Button-1>', self.clear_suggestion)  # Clear on click

        # Create menu bar
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

        # Prediction state
        self.last_prediction_time = 0
        self.prediction_delay = 0.5  # seconds
        self.current_suggestion = ""
        self.prediction_thread = None

    def get_current_line(self) -> str:
        """Get the current line of text up to the cursor."""
        current_line = self.text_area.get("insert linestart", "insert")
        return current_line

    def on_text_change(self, event=None):
        """Handle text change events."""
        if event.keysym == 'Tab':
            return 'break'

        # Clear old prediction thread if it exists
        if self.prediction_thread and self.prediction_thread.is_alive():
            return

        # Start new prediction thread
        current_time = time.time()
        if current_time - self.last_prediction_time > self.prediction_delay:
            self.last_prediction_time = current_time
            self.prediction_thread = threading.Thread(target=self.update_suggestion)
            self.prediction_thread.start()

    def update_suggestion(self):
        """Update the suggestion text."""
        try:
            current_line = self.get_current_line()
            if not current_line.strip():
                self.clear_suggestion()
                return

            # Get prediction
            prediction = predict_text(current_line, language="english")
            if prediction:
                self.current_suggestion = prediction
                # Update UI in main thread
                self.root.after(0, self.show_suggestion)
        except Exception as e:
            print(f"Prediction error: {e}")

    def show_suggestion(self):
        """Show the suggestion in gray text."""
        if self.current_suggestion:
            # Get current cursor position
            cursor_pos = self.text_area.index("insert")
            bbox = self.text_area.bbox(cursor_pos)
            if bbox:
                x, y, _, h = bbox
                # Position the suggestion label at cursor position
                self.suggestion_label.place(
                    x=x + self.text_area.winfo_x(),
                    y=y + self.text_area.winfo_y(),
                    height=h
                )
                self.suggestion_label.config(text=self.current_suggestion)
                self.suggestion_label.lift()

    def complete_text(self, event=None):
        """Complete the text with the current suggestion."""
        if self.current_suggestion:
            self.text_area.insert(tk.INSERT, self.current_suggestion)
            self.clear_suggestion()
        return 'break'

    def clear_suggestion(self, event=None):
        """Clear the current suggestion."""
        self.current_suggestion = ""
        self.suggestion_label.place_forget()

    def new_file(self):
        """Clear the current text area for a new file."""
        self.text_area.delete(1.0, tk.END)
        self.clear_suggestion()

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
