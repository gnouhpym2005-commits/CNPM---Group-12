import tkinter as tk
from tkinter import ttk, messagebox

from database.password_repository import PasswordRepository


class ManagePasswordApp:

    def __init__(self, parent_frame):

        self.parent = parent_frame
        self.repo = PasswordRepository()

        # ================= TITLE =================

        tk.Label(
            self.parent,
            text="MANAGE PASSWORD",
            font=("Arial",16,"bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        # ================= FORM =================

        form_frame = tk.LabelFrame(
            self.parent,
            text="Password Information",
            bg="#f4f6f9",
            padx=10,
            pady=10
        )

        form_frame.pack(
            fill=tk.X,
            padx=10,
            pady=5
        )

        form_frame.columnconfigure(1,weight=1)
        form_frame.columnconfigure(3,weight=1)

        # User ID

        tk.Label(
            form_frame,
            text="User ID:",
            bg="#f4f6f9"
        ).grid(row=0,column=0,padx=5,pady=5,sticky="w")

        self.entry_id = ttk.Entry(form_frame,width=30)

        self.entry_id.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # Role

        tk.Label(
            form_frame,
            text="Role:",
            bg="#f4f6f9"
        ).grid(row=0,column=2,padx=5,pady=5,sticky="w")

        self.cbo_role = ttk.Combobox(
            form_frame,
            values=[
                "Student",
                "Lecturer",
                "Admin"
            ],
            state="readonly",
            width=25
        )

        self.cbo_role.grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # Password

        tk.Label(
            form_frame,
            text="Password:",
            bg="#f4f6f9"
        ).grid(row=1,column=0,padx=5,pady=5,sticky="w")

        self.entry_password = ttk.Entry(
            form_frame,
            width=30
        )

        self.entry_password.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # ================= BUTTON =================

        btn_frame = tk.Frame(
            self.parent,
            bg="#f4f6f9"
        )

        btn_frame.pack(
            fill=tk.X,
            padx=10,
            pady=10
        )

        tk.Button(
            btn_frame,
            text="Update Password",
            bg="#3498db",
            fg="white",
            width=18,
            command=self.update_password
        ).pack(side=tk.LEFT,padx=5)

        tk.Button(
            btn_frame,
            text="Reset Password",
            bg="#f39c12",
            fg="white",
            width=18,
            command=self.reset_password
        ).pack(side=tk.LEFT,padx=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            bg="#2ecc71",
            fg="white",
            width=15,
            command=self.load_users
        ).pack(side=tk.LEFT,padx=5)

        # ================= TABLE =================

        columns = (
            "id",
            "name",
            "role",
            "password"
        )

        self.tree = ttk.Treeview(
            self.parent,
            columns=columns,
            show="headings",
            height=15
        )

        self.tree.heading("id",text="User ID")
        self.tree.heading("name",text="Full Name")
        self.tree.heading("role",text="Role")
        self.tree.heading("password",text="Password")

        self.tree.column("id",width=120)
        self.tree.column("name",width=220)
        self.tree.column("role",width=120)
        self.tree.column("password",width=180)

        self.tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=5
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_user
        )

        self.load_users()

    def load_users(self):

        self.tree.delete(*self.tree.get_children())

        rows = self.repo.get_all_users()

        for row in rows:

            self.tree.insert(
                "",
                "end",
                values=(
                    row.userID,
                    row.fullName,
                    row.role,
                    row.password
                )
            )
    
    def select_user(self,event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected)["values"]

        self.entry_id.delete(0,tk.END)
        self.entry_id.insert(0,values[0])
        self.cbo_role.set(values[2])
        self.entry_password.delete(0,tk.END)
        self.entry_password.insert(0,values[3])

    def update_password(self):
        self.repo.admin_update_password(
            self.entry_id.get(),
            self.cbo_role.get(),
            self.entry_password.get()
        )
        messagebox.showinfo(
            "Success",
            "Password updated successfully."
        )
        self.load_users()
    
    def reset_password(self):
        self.repo.admin_reset_password(
            self.entry_id.get(),
            self.cbo_role.get()
        )
        messagebox.showinfo(
            "Success",
            "Password has been reset.\nDefault password: 123456"
        )
        self.load_users()