import tkinter as tk
from tkinter import ttk

class ManageSectionsApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        tk.Label(self.parent, text="QUẢN LÝ LỚP HỌC PHẦN (COURSE SECTIONS)", font=("Arial", 16, "bold"), bg="#f4f6f9").pack(pady=10)

        form_frame = tk.LabelFrame(self.parent, text="Thiết lập Lớp & Phân công", font=("Arial", 10), bg="#f4f6f9", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(form_frame, text="Mã Lớp (ClassID):", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_classid = ttk.Entry(form_frame, width=15)
        self.entry_classid.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Môn học:", bg="#f4f6f9").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.cbo_subject = ttk.Combobox(form_frame, values=["SE101 - CNPM", "DB201 - Cơ sở DL"], width=20)
        self.cbo_subject.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Giảng viên:", bg="#f4f6f9").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.cbo_lecturer = ttk.Combobox(form_frame, values=["GV001 - Ng Văn An", "GV002 - Trần Thị B"], width=20)
        self.cbo_lecturer.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(form_frame, text="Thứ (Day):", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cbo_day = ttk.Combobox(form_frame, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], width=13)
        self.cbo_day.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tiết học (Ví dụ: 1-3):", bg="#f4f6f9").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_period = ttk.Entry(form_frame, width=22)
        self.entry_period.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Sĩ số Max:", bg="#f4f6f9").grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_capacity = ttk.Entry(form_frame, width=22)
        self.entry_capacity.grid(row=1, column=5, padx=5, pady=5)

        btn_frame = tk.Frame(self.parent, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Mở Lớp (Create)", bg="#3498db", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cập nhật Lịch/Sĩ số", bg="#f39c12", fg="white", width=18).pack(side=tk.LEFT, padx=5)

        columns = ("classID", "subject", "lecturer", "schedule", "capacity")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=10)
        self.tree.heading("classID", text="Mã Lớp")
        self.tree.heading("subject", text="Môn Học")
        self.tree.heading("lecturer", text="Giảng Viên")
        self.tree.heading("schedule", text="Lịch Học")
        self.tree.heading("capacity", text="Sĩ Số")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)