import tkinter as tk
from tkinter import ttk, messagebox

class ManageLecturersApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        tk.Label(self.parent, text="QUẢN LÝ GIẢNG VIÊN", font=("Arial", 16, "bold"), bg="#f4f6f9").pack(pady=10)

        form_frame = tk.LabelFrame(self.parent, text="Thông tin Giảng viên", font=("Arial", 10), bg="#f4f6f9", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(form_frame, text="Mã GV:", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_id = ttk.Entry(form_frame, width=20)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Họ Tên:", bg="#f4f6f9").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_name = ttk.Entry(form_frame, width=30)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Khoa (Dept):", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cbo_dept = ttk.Combobox(form_frame, values=["CNTT", "Toán cơ bản", "Ngoại ngữ"], width=17)
        self.cbo_dept.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Trạng thái:", bg="#f4f6f9").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.cbo_status = ttk.Combobox(form_frame, values=["ACTIVE", "LOCKED"], width=27)
        self.cbo_status.grid(row=1, column=3, padx=5, pady=5)

        btn_frame = tk.Frame(self.parent, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Thêm (Create)", bg="#2ecc71", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sửa (Update)", bg="#f39c12", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Khóa/Mở Khóa", bg="#e74c3c", fg="white", width=15).pack(side=tk.LEFT, padx=5)

        columns = ("id", "name", "dept", "status")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="Mã GV")
        self.tree.heading("name", text="Họ Tên")
        self.tree.heading("dept", text="Khoa")
        self.tree.heading("status", text="Trạng Thái")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)