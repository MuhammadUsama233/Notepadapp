from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import win32api
import win32print

def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)
    update_status_bar()
    update_bottom_bar()

def openFile():
    global file
    file = askopenfilename(defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                      ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        with open(file, "r") as f:
            TextArea.insert(1.0, f.read())
    update_status_bar()
    update_bottom_bar()

def saveFile():
    global file
    if file is None:
        file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                  filetypes=[("All Files", "*.*"),
                                             ("Text Documents", "*.txt")])
        if file == "":
            file = None
        else:
            with open(file, "w") as f:
                f.write(TextArea.get(1.0, END))
            root.title(os.path.basename(file) + " - Notepad")
    else:
        with open(file, "w") as f:
            f.write(TextArea.get(1.0, END))
    update_status_bar()
    update_bottom_bar()

def saveAsFile():
    global file
    file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                              filetypes=[("All Files", "*.*"),
                                        ("Text Documents", "*.txt")])
    if file != "":
        with open(file, "w") as f:
            f.write(TextArea.get(1.0, END))
        root.title(os.path.basename(file) + " - Notepad")
    update_status_bar()
    update_bottom_bar()

def printFile():
    content = TextArea.get(1.0, END)
    temp_file = "temp.txt"
    try:
        with open(temp_file, "w") as f:
            f.write(content)
        win32api.ShellExecute(0, "print", temp_file, None, ".", 0)
    except Exception as e:
        showinfo("Error", f"An error occurred while printing: {str(e)}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def quitApp():
    root.destroy()

def cut():
    TextArea.event_generate("<<Cut>>")
    update_status_bar()
    update_bottom_bar()

def copy():
    TextArea.event_generate("<<Copy>>")

def paste():
    TextArea.event_generate("<<Paste>>")
    update_status_bar()
    update_bottom_bar()

def undo():
    try:
        TextArea.edit_undo()
        update_status_bar()
        update_bottom_bar()
    except Exception:
        pass

def redo():
    try:
        TextArea.edit_redo()
        update_status_bar()
        update_bottom_bar()
    except Exception:
        pass

def about():
    showinfo("Notepad", "Welcome to the Notepad application! Developed by Muhammad Usama.")

def feedback():
    feedback_popup = Toplevel(root)
    feedback_popup.title("Feedback")
    feedback_popup.geometry("400x300")
    feedback_popup.resizable(False, False)

    Label(feedback_popup, text="We value your feedback!", font="lucida 12 bold").pack(pady=10)
    Label(feedback_popup, text="Please share your comments or suggestions below:", font="lucida 10").pack(pady=5)

    feedback_text = Text(feedback_popup, font="lucida 10", wrap=WORD, height=10, width=40)
    feedback_text.pack(pady=10)

    def save_feedback():
        user_feedback = feedback_text.get(1.0, END).strip()
        if user_feedback:
            feedback_file = "feedback.txt"
            with open(feedback_file, "a") as f:
                f.write(user_feedback + "\n" + "-"*40 + "\n")
            showinfo("Thank You!", "Your feedback has been saved. Thank you for helping us improve!")
            feedback_popup.destroy()
        else:
            showinfo("Empty Feedback", "Please provide meaningful feedback before submitting.")

    Button(feedback_popup, text="Submit", command=save_feedback).pack(pady=5)
    Button(feedback_popup, text="Close", command=feedback_popup.destroy).pack(pady=5)

def update_status_bar(event=None):
    line, col = TextArea.index(INSERT).split('.')
    status_var.set(f"Line: {line}, Column: {col}")

def update_bottom_bar():
    if file:
        file_name = os.path.basename(file)
        file_size = os.path.getsize(file) if os.path.exists(file) else 0
        char_count = len(TextArea.get(1.0, END)) - 1
        bottom_var.set(f"File: {file_name} | Size: {file_size} bytes | Characters: {char_count}")
    else:
        bottom_var.set("No file selected")

def toggle_word_wrap():
    global word_wrap
    word_wrap = not word_wrap
    TextArea.config(wrap=WORD if word_wrap else NONE)

def change_font_size_popup():
    def apply_font_size():
        size = font_size_var.get()
        try:
            size = int(size)
            TextArea.config(font=f"lucida {size}")
            font_popup.destroy()
        except ValueError:
            showinfo("Error", "Invalid font size. Please enter a valid number.")

    font_popup = Toplevel(root)
    font_popup.title("Change Font Size")
    font_popup.geometry("250x100")
    font_popup.resizable(False, False)

    Label(font_popup, text="Enter Font Size:", font="lucida 10").pack(pady=5)
    font_size_var = StringVar()
    Entry(font_popup, textvariable=font_size_var, font="lucida 10").pack(pady=5)
    Button(font_popup, text="Apply", command=apply_font_size).pack(pady=5)

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    colors = {"bg": "black", "fg": "white", "insert": "white"} if dark_mode else {"bg": "white", "fg": "black", "insert": "black"}
    TextArea.config(bg=colors["bg"], fg=colors["fg"], insertbackground=colors["insert"])
    StatusBar.config(bg=colors["bg"], fg=colors["fg"])
    BottomBar.config(bg="red" if not dark_mode else "black", fg=colors["fg"])

# Main Code
if __name__ == '__main__':
    root = Tk()
    root.title("Untitled - Notepad")
    root.geometry("644x788")

    TextArea = Text(root, font="lucida 13", undo=True, wrap=WORD)
    TextArea.pack(expand=True, fill=BOTH)

    Scroll = Scrollbar(TextArea)
    Scroll.pack(side=RIGHT, fill=Y)
    Scroll.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=Scroll.set)

    file = None
    word_wrap = True
    dark_mode = False

    MenuBar = Menu(root)
    FileMenu = Menu(MenuBar, tearoff=0)
    FileMenu.add_command(label="New", command=newFile)
    FileMenu.add_command(label="Open", command=openFile)
    FileMenu.add_command(label="Save", command=saveFile)
    FileMenu.add_command(label="Save As", command=saveAsFile)
    FileMenu.add_command(label="Print", command=printFile)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=quitApp)
    MenuBar.add_cascade(label="File", menu=FileMenu)

    EditMenu = Menu(MenuBar, tearoff=0)
    EditMenu.add_command(label="Cut", command=cut)
    EditMenu.add_command(label="Copy", command=copy)
    EditMenu.add_command(label="Paste", command=paste)
    EditMenu.add_command(label="Undo", command=undo)
    EditMenu.add_command(label="Redo", command=redo)
    MenuBar.add_cascade(label="Edit", menu=EditMenu)

    FormatMenu = Menu(MenuBar, tearoff=0)
    FormatMenu.add_command(label="Word Wrap", command=toggle_word_wrap)
    FormatMenu.add_command(label="Change Font Size", command=change_font_size_popup)
    MenuBar.add_cascade(label="Format", menu=FormatMenu)

    ViewMenu = Menu(MenuBar, tearoff=0)
    ViewMenu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
    MenuBar.add_cascade(label="View", menu=ViewMenu)

    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="About Notepad", command=about)
    HelpMenu.add_command(label="Feedback", command=feedback)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    root.config(menu=MenuBar)

    status_var = StringVar()
    status_var.set("Line: 1, Column: 1")
    StatusBar = Label(root, textvariable=status_var, anchor='w', font="lucida 10", relief=SUNKEN, bg="lightgrey")
    StatusBar.pack(side=BOTTOM, fill=X)

    bottom_var = StringVar()
    bottom_var.set("No file selected")
    BottomBar = Label(root, textvariable=bottom_var, anchor='w', font="lucida 10 bold", relief=SUNKEN, bg="red", fg="white")
    BottomBar.pack(side=BOTTOM, fill=X)

    TextArea.bind("<KeyRelease>", lambda event: (update_status_bar(), update_bottom_bar()))

    root.mainloop()
