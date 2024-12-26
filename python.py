import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import tkinter.font as font

# Functions
def new_file():
    text_area.delete(1.0, tk.END)
    root.title("Untitled - Notepad")

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(1.0, file.read())
            root.title(f"{file_path} - Notepad")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file: {e}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, tk.END))
            root.title(f"{file_path} - Notepad")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot save file: {e}")

def exit_app():
    if messagebox.askyesno("Exit", "Do you want to save changes before exiting?"):
        save_file()
    root.destroy()

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def find_text():
    def search():
        text_area.tag_remove("highlight", "1.0", tk.END)
        query = search_entry.get()
        if query:
            start_pos = "1.0"
            while True:
                start_pos = text_area.search(query, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(query)}c"
                text_area.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            text_area.tag_config("highlight", background="yellow", foreground="black")
    
    search_window = tk.Toplevel(root)
    search_window.title("Find")
    search_window.geometry("300x100")
    tk.Label(search_window, text="Find:").pack(side="left", padx=10, pady=10)
    search_entry = tk.Entry(search_window, width=25)
    search_entry.pack(side="left", padx=10, pady=10)
    tk.Button(search_window, text="Search", command=search).pack(side="left", padx=10, pady=10)

def about():
    messagebox.showinfo("About Notepad", "Notepad using Tkinter\n\nCreated with Python.")

def toggle_word_wrap():
    if text_area.cget("wrap") == "none":
        text_area.config(wrap="word")
    else:
        text_area.config(wrap="none")

def zoom_in():
    current_size = default_font.cget("size")
    default_font.config(size=current_size + 2)

def zoom_out():
    current_size = default_font.cget("size")
    default_font.config(size=max(current_size - 2, 1))  # Prevent font size from becoming too small

def apply_light_theme():
    text_area.config(bg="white", fg="black")

def apply_dark_theme():
    text_area.config(bg="black", fg="white")

def apply_custom_theme():
    bg_color = colorchooser.askcolor(title="Choose Background Color")[1]
    if not bg_color:
        return  # User canceled the selection
    fg_color = colorchooser.askcolor(title="Choose Text Color")[1]
    if not fg_color:
        return  # User canceled the selection
    text_area.config(bg=bg_color, fg=fg_color)

# Initialize root window
root = tk.Tk()
root.title("Untitled - Notepad")
root.geometry("800x600")

# Set default font
default_font = font.Font(family="TkDefaultFont", size=12)

# Create text area with scrollbar
frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

text_area = tk.Text(frame, wrap="word", undo=True, yscrollcommand=scrollbar.set, font=default_font)
text_area.pack(expand=True, fill="both")

scrollbar.config(command=text_area.yview)

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Search menu
search_menu = tk.Menu(menu_bar, tearoff=0)
search_menu.add_command(label="Find", command=find_text)
menu_bar.add_cascade(label="Search", menu=search_menu)

# View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Toggle Word Wrap", command=toggle_word_wrap)
view_menu.add_command(label="Light Theme", command=apply_light_theme)
view_menu.add_command(label="Dark Theme", command=apply_dark_theme)
view_menu.add_command(label="Custom Theme", command=apply_custom_theme)
menu_bar.add_cascade(label="View", menu=view_menu)

# Format menu
format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Zoom In", command=zoom_in)
format_menu.add_command(label="Zoom Out", command=zoom_out)
menu_bar.add_cascade(label="Format", menu=format_menu)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Run the application
root.mainloop()
