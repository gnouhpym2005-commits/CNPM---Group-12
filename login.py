import tkinter as tk
from tkinter import messagebox
from authentication import Authentication

auth = Authentication()

def login():

    username = txtUsername.get().strip()
    password = txtPassword.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter your username and password."
        )
        return

    role = auth.login(username, password)

    if role is None:
        return

    messagebox.showinfo(
        "Login Successful",
        "Welcome to the Course Registration System."
    )

    if role == "Student":
        #window.destroy()        # Đóng cửa sổ đăng nhập
        #student_dashboard()
        print("Student Dashboard")

    elif role == "Lecturer":
        #window.destroy()        
        #lecturer_dashboard()
        print("Lecturer Dashboard")

    elif role == "Administrator":
        #window.destroy()        
        #admin_dashboard()
        print("Administrator Dashboard")


# ==========================
# GUI
# ==========================

window = tk.Tk()

window.title("Course Registration System")
window.geometry("400x250")
window.resizable(False, False)

# Title
title = tk.Label(
    window,
    text="LOGIN",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

# Username
tk.Label(window, text="Username").pack()

txtUsername = tk.Entry(window, width=30)
txtUsername.pack(pady=5)

# Password
tk.Label(window, text="Password").pack()

txtPassword = tk.Entry(window, show="*", width=30)
txtPassword.pack(pady=5)

# Login Button
btnLogin = tk.Button(
    window,
    text="Login",
    width=15,
    command=login
)
btnLogin.pack(pady=20)

window.mainloop()