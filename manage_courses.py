import tkinter as tk
from tkinter import ttk, messagebox

class ManageCoursesApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        tk.Label(self.parent, text="QUẢN LÝ MÔN HỌC (SUBJECTS)", font=("Arial", 16, "bold"), bg="#f4f6f9").pack(pady=10)

        form_frame = tk.LabelFrame(self.parent, text="Thông tin Môn học", font=("Arial", 10), bg="#f4f6f9", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(form_frame, text="Mã Môn:", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_id = ttk.Entry(form_frame, width=15)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tên Môn:", bg="#f4f6f9").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_name = ttk.Entry(form_frame, width=35)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Số Tín chỉ:", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_credits = ttk.Entry(form_frame, width=15)
        self.entry_credits.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self.parent, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Thêm", bg="#2ecc71", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cập nhật", bg="#f39c12", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa Môn", bg="#c0392b", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        columns = ("id", "name", "credits")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="Mã Môn")
        self.tree.heading("name", text="Tên Môn Học")
        self.tree.heading("credits", text="Tín chỉ")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)