import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip
import pyzipper  
from tkinter import messagebox,Label
import os
from PIL import Image, ImageTk 

# פונקציה ליצירת סיסמא
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

# פונקציה להעתקת הסיסמא ללוח
def copy_to_clipboard(password):
    pyperclip.copy(password)
    messagebox.showinfo("Copy", "Password copied to clipboard!")

# פונקציה לשמירת הסיסמא כקובץ טקסט בתוך ZIP עם הצפנת סיסמה
def save_password(password):
    folder_name = filedialog.asksaveasfilename(defaultextension=".zip", title="Save Password", filetypes=[("ZIP files", "*.zip")])
    if not folder_name:
        return

    # בקשת סיסמה מהמשתמש להגנה על ZIP
    password_protection = simpledialog.askstring("Password", "Enter a password to protect the ZIP file:", show='*')
    if not password_protection:
        return

    # כתיבת הסיסמא לקובץ טקסט זמני
    with open('password.txt', 'w') as f:
        f.write(password)

    # יצירת קובץ ZIP מוצפן עם סיסמה
    with pyzipper.AESZipFile(folder_name, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password_protection.encode())
        zipf.write('password.txt')
    
    # מחיקת הקובץ הטקסטואלי
    os.remove('password.txt')

    messagebox.showinfo("Save", "Password saved in a protected ZIP file!")

# פונקציה ליצירת סיסמא והצגתה
def on_generate():
    length = length_var.get()
    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digit_var.get()
    use_special = special_var.get()

    password = generate_password(length, use_upper, use_lower, use_digits, use_special)
    password_label.config(text=password)

# יצירת חלון
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x600")
root.configure(bg="#000000")  # רקע שחור על כל החלון

# מסגרת לסיסמא
frame = ttk.Frame(root, padding="20", style="TFrame")
frame.pack(fill=tk.BOTH, expand=True)

# הגדרת סגנון למסגרת
style = ttk.Style()
style.configure("TFrame", background="#36454F")  # מסגרת ברקע שחור
style.configure("TLabel", font=("Comic Sans MS", 10))
style.configure("TCheckbutton", font=("Comic Sans MS", 10))
style.configure("TButton", font=("Comic Sans MS", 10))



# כותרת
title = ttk.Label(frame, text="Password Generator", font=("Comic Sans MS", 16), foreground="#ECF0F1", background="#36453F")
title.pack()

bg_path = r"C:\Users\user\Desktop\PasswordGenerator\background1.png"  # יש לשנות לנתיב התמונה שלך ולוודא את הסיומת
bg_image = Image.open(bg_path)
bg_image = bg_image.resize((100, 100))  # שינוי גודל התמונה במידת הצורך
bg_photo = ImageTk.PhotoImage(bg_image)

# תווית לרקע
bg_label = Label(frame, image=bg_photo)
bg_label.image = bg_photo  # שמירת עותק כדי למנוע מהזיכרון למחוק את התמונה
bg_label.pack(pady=10)  # הצגת התמונה מתחת לכותרת

# סליידר לבחירת אורך הסיסמא
length_var = tk.IntVar(value=12)
length_label = ttk.Label(frame, text="Length:", foreground="#ECF0F1", background="#36453F", font=("Comic Sans MS", 10))
length_label.pack(pady=5)

# סליידר עם תצוגת ערכים
length_slider = ttk.Scale(frame, from_=5, to=15, variable=length_var, orient="horizontal", length=200, command=lambda x: length_value_label.config(text=f"{int(float(x))}"))
length_slider.pack()


# תווית להצגת ערך הסליידר
length_value_label = ttk.Label(frame, text="12", foreground="#000000", background="#36450F", font=("Comic Sans MS", 15))
length_value_label.pack()

# מסגרת לארגון תיבות הבחירה
check_frame1 = ttk.Frame(frame, padding="10")
check_frame1.pack()

style.configure("TCheckbutton", background="#36453F", foreground="black")  # רקע כהה עם כתב לבן

# תיבות בחירה לשורה הראשונה
upper_var = tk.BooleanVar(value=True)
upper_check = ttk.Checkbutton(check_frame1, text="Use Uppercase", variable=upper_var, style="TCheckbutton")
upper_check.pack(side=tk.LEFT)

lower_var = tk.BooleanVar(value=True)
lower_check = ttk.Checkbutton(check_frame1, text="Use Lowercase", variable=lower_var, style="TCheckbutton")
lower_check.pack(side=tk.LEFT)

# מסגרת לשורה השנייה
check_frame2 = ttk.Frame(frame, padding="10")
check_frame2.pack()

# תיבות בחירה לשורה השנייה
digit_var = tk.BooleanVar(value=True)
digit_check = ttk.Checkbutton(check_frame2, text="Use Digits", variable=digit_var, style="TCheckbutton")
digit_check.pack(side=tk.LEFT)

special_var = tk.BooleanVar(value=False)
special_check = ttk.Checkbutton(check_frame2, text="Use Special Characters", variable=special_var, style="TCheckbutton")
special_check.pack(side=tk.LEFT)

# כפתור יצירת הסיסמא
generate_button = ttk.Button(frame, text="Generate Password", command=on_generate)
generate_button.pack(pady=10)

# הגדרת סגנון חדש עבור כפתור הגנרציה
style.configure("Generate.TButton", font=("Comic Sans MS", 13))  # הגדרת גודל גופן 13 עבור כפתור הגנרציה
generate_button.configure(style="Generate.TButton")  # עדכון הסגנון של כפתור הגנרציה

# תווית להציג את הסיסמא
password_label = ttk.Label(frame, text="", wraplength=300, background="#34495E", foreground="white", font=("Comic Sans MS", 14, "bold"), relief="solid", padding=10)
password_label.pack(pady=10)

# כפתור להעתקת הסיסמא ללוח
copy_button = ttk.Button(frame, text="Copy to Clipboard", command=lambda: copy_to_clipboard(password_label['text']))
copy_button.pack(pady=5)

# כפתור לשמירת הסיסמא כקובץ טקסט בתוך תיקיה עם סיסמה
save_button = ttk.Button(frame, text="Save Password as ZIP", command=lambda: save_password(password_label['text']))
save_button.pack(pady=5)

# הפעלת הלולאת Tkinter
root.mainloop()
