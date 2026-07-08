import tkinter as tk
from tkinter import messagebox

from database.password_repository import PasswordRepository


class ChangePasswordApp:

    def __init__(self, parent, user_id, role):

        self.parent = parent
        self.user_id = user_id
        self.role = role

        self.repository = PasswordRepository()   
        self.create_widgets()

    # =====================================================

    def create_widgets(self):

        self.main = tk.Frame(
            self.parent,
            bg="#f4f6f9"
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            self.main,
            text="Change Password",
            bg="#f4f6f9",
            font=("Segoe UI", 20, "bold")
        ).pack(
            pady=(40, 30)
        )

        form = tk.Frame(
            self.main,
            bg="white",
            bd=1,
            relief="solid"
        )

        form.pack(
            pady=10,
            ipadx=30,
            ipady=25
        )

        # ================= CURRENT PASSWORD =================

        tk.Label(
            form,
            text="Current Password",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=12
        )

        self.txtCurrent = tk.Entry(
            form,
            width=30,
            show="*",
            font=("Segoe UI", 11)
        )

        self.txtCurrent.grid(
            row=0,
            column=1,
            padx=20,
            pady=12
        )

        # ================= NEW PASSWORD =================

        tk.Label(
            form,
            text="New Password",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=12
        )

        self.txtNew = tk.Entry(
            form,
            width=30,
            show="*",
            font=("Segoe UI", 11)
        )

        self.txtNew.grid(
            row=1,
            column=1,
            padx=20,
            pady=12
        )

        # ================= CONFIRM PASSWORD =================

        tk.Label(
            form,
            text="Confirm Password",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=12
        )

        self.txtConfirm = tk.Entry(
            form,
            width=30,
            show="*",
            font=("Segoe UI", 11)
        )

        self.txtConfirm.grid(
            row=2,
            column=1,
            padx=20,
            pady=12
        )

        # ================= BUTTON =================

        button_frame = tk.Frame(
            self.main,
            bg="#f4f6f9"
        )

        button_frame.pack(
            pady=20
        )

        tk.Button(
            button_frame,
            text="Update Password",
            bg="#3498db",
            fg="white",
            width=18,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            command=self.update_password
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            button_frame,
            text="Clear",
            bg="#95a5a6",
            fg="white",
            width=10,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            command=self.clear
        ).pack(
            side="left",
            padx=10
        )

    # =====================================================

    def clear(self):

        self.txtCurrent.delete(0, tk.END)
        self.txtNew.delete(0, tk.END)
        self.txtConfirm.delete(0, tk.END)

        self.txtCurrent.focus()

    # =====================================================

    def update_password(self):

        current = self.txtCurrent.get().strip()
        new = self.txtNew.get().strip()
        confirm = self.txtConfirm.get().strip()

        if current == "" or new == "" or confirm == "":

            messagebox.showwarning(
                "Warning",
                "Please fill in all information."
            )

            return

        if new != confirm:

            messagebox.showerror(
                "Error",
                "Confirm password does not match."
            )

            return

        success = self.repository.check_password(
            self.user_id,
            self.role,
            current
        )

        if success:

            self.repository.update_password(
                self.user_id,
                self.role,
            new
        )

            messagebox.showinfo(
                "Success",
                "Password updated successfully."
            )
            self.clear()
        else:
            messagebox.showerror(
            "Error",
            "Current password is incorrect."
        )