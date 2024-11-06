import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip
import pyzipper  
from tkinter import messagebox,Label
import os
from PIL import Image, ImageTk 

def generate_password(length, use_upper, use_lower, use_digits, use_special):
    characters = ''
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        return ""

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def copy_to_clipboard(password):
    pyperclip.copy(password)
    messagebox.showinfo("Copy", "Password copied to clipboard!")

def save_password(password):
    folder_name = filedialog.asksaveasfilename(defaultextension=".zip", title="Save Password", filetypes=[("ZIP files", "*.zip")])
    if not folder_name:
        return

    password_protection = simpledialog.askstring("Password", "Enter a password to protect the ZIP file:", show='*')
    if not password_protection:
        return


    with open('password.txt', 'w') as f:
        f.write(password)


    with pyzipper.AESZipFile(folder_name, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password_protection.encode())
        zipf.write('password.txt')
    

    os.remove('password.txt')

    messagebox.showinfo("Save", "Password saved in a protected ZIP file!")


def on_generate():
    length = length_var.get()
    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digit_var.get()
    use_special = special_var.get()

    password = generate_password(length, use_upper, use_lower, use_digits, use_special)
    password_label.config(text=password)


root = tk.Tk()
root.title("Password Generator")
root.geometry("500x600")
root.configure(bg="#000000")  


frame = ttk.Frame(root, padding="20", style="TFrame")
frame.pack(fill=tk.BOTH, expand=True)

style = ttk.Style()
style.configure("TFrame", background="#36454F")  
style.configure("TLabel", font=("Comic Sans MS", 10))
style.configure("TCheckbutton", font=("Comic Sans MS", 10))
style.configure("TButton", font=("Comic Sans MS", 10))




title = ttk.Label(frame, text="Password Generator", font=("Comic Sans MS", 16), foreground="#ECF0F1", background="#36453F")
title.pack()

bg_path = r"C:\Users\user\Desktop\PasswordGenerator\background1.png"  
bg_image = Image.open(bg_path)
bg_image = bg_image.resize((100, 100)) 
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(frame, image=bg_photo)
bg_label.image = bg_photo 
bg_label.pack(pady=10) 

length_var = tk.IntVar(value=12)
length_label = ttk.Label(frame, text="Length:", foreground="#ECF0F1", background="#36453F", font=("Comic Sans MS", 10))
length_label.pack(pady=5)

length_slider = ttk.Scale(frame, from_=5, to=15, variable=length_var, orient="horizontal", length=200, command=lambda x: length_value_label.config(text=f"{int(float(x))}"))
length_slider.pack()

length_value_label = ttk.Label(frame, text="12", foreground="#000000", background="#36450F", font=("Comic Sans MS", 15))
length_value_label.pack()

check_frame1 = ttk.Frame(frame, padding="10")
check_frame1.pack()

style.configure("TCheckbutton", background="#36453F", foreground="black")  


upper_var = tk.BooleanVar(value=True)
upper_check = ttk.Checkbutton(check_frame1, text="Use Uppercase", variable=upper_var, style="TCheckbutton")
upper_check.pack(side=tk.LEFT)

lower_var = tk.BooleanVar(value=True)
lower_check = ttk.Checkbutton(check_frame1, text="Use Lowercase", variable=lower_var, style="TCheckbutton")
lower_check.pack(side=tk.LEFT)


check_frame2 = ttk.Frame(frame, padding="10")
check_frame2.pack()


digit_var = tk.BooleanVar(value=True)
digit_check = ttk.Checkbutton(check_frame2, text="Use Digits", variable=digit_var, style="TCheckbutton")
digit_check.pack(side=tk.LEFT)

special_var = tk.BooleanVar(value=False)
special_check = ttk.Checkbutton(check_frame2, text="Use Special Characters", variable=special_var, style="TCheckbutton")
special_check.pack(side=tk.LEFT)


generate_button = ttk.Button(frame, text="Generate Password", command=on_generate)
generate_button.pack(pady=10)


style.configure("Generate.TButton", font=("Comic Sans MS", 13)) 
generate_button.configure(style="Generate.TButton")  


password_label = ttk.Label(frame, text="", wraplength=300, background="#34495E", foreground="white", font=("Comic Sans MS", 14, "bold"), relief="solid", padding=10)
password_label.pack(pady=10)


copy_button = ttk.Button(frame, text="Copy to Clipboard", command=lambda: copy_to_clipboard(password_label['text']))
copy_button.pack(pady=5)


save_button = ttk.Button(frame, text="Save Password as ZIP", command=lambda: save_password(password_label['text']))
save_button.pack(pady=5)


root.mainloop()
