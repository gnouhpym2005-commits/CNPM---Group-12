import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from database.period_repository import PeriodRepository


class ManageRegistrationPeriodsApp:

    STATUS_VALUES = ["Upcoming", "Open", "Closed"]

    # Format shown to the user inside the Treeview table (unchanged)
    DATE_FMT = "%d/%m/%Y"
    DATETIME_FMT = "%d/%m/%Y %H:%M"

    # Format shown inside the DateEntry picker widgets themselves.
    # tkcalendar's own pattern syntax (yyyy/mm/dd), separate from strftime.
    DATE_ENTRY_PATTERN = "yyyy/mm/dd"

    def __init__(self, parent):
        self.parent = parent
        self.repo = PeriodRepository()
        self.selected_period_id = None

        self.build_ui()
        self.load_data()

    # ------------------------------------------------------------------
    # UI CONSTRUCTION
    # ------------------------------------------------------------------
    def build_ui(self):
        tk.Label(
            self.parent,
            text="MANAGE REGISTRATION PERIODS",
            font=("Arial", 18, "bold"),
            bg="#f4f6f9",
        ).pack(pady=(0, 15))

        # ---------------- Information group box ----------------
        info_frame = tk.LabelFrame(
            self.parent,
            text="Registration Period Information",
            font=("Arial", 10),
            bg="#f4f6f9",
            padx=15,
            pady=15,
        )
        info_frame.pack(fill=tk.X, padx=5, pady=(0, 15))

        # Fixed-width columns: label | input | label | input
        # Using uniform groups keeps col0==col2 and col1==col3 exactly equal,
        # which is what actually keeps every row's widgets lined up.
        info_frame.columnconfigure(0, minsize=140, weight=0, uniform="lbl")
        info_frame.columnconfigure(1, minsize=280, weight=0, uniform="inp")
        info_frame.columnconfigure(2, minsize=140, weight=0, uniform="lbl")
        info_frame.columnconfigure(3, minsize=280, weight=0, uniform="inp")

        label_opts = {"font": ("Arial", 11), "bg": "#f4f6f9", "anchor": "w"}
        entry_opts = {"font": ("Arial", 11), "width": 26}

        ROW_PADY = 8

        # ================= Row 0 =================
        tk.Label(info_frame, text="Period ID", **label_opts).grid(
            row=0, column=0, sticky="w", pady=ROW_PADY, padx=(0, 8)
        )
        self.entry_period_id = tk.Entry(info_frame, **entry_opts)
        self.entry_period_id.grid(row=0, column=1, sticky="w", pady=ROW_PADY, padx=(0, 20))

        tk.Label(info_frame, text="Semester Name", **label_opts).grid(
            row=0, column=2, sticky="w", pady=ROW_PADY, padx=(0, 8)
        )
        self.entry_semester_name = tk.Entry(info_frame, **entry_opts)
        self.entry_semester_name.grid(row=0, column=3, sticky="w", pady=ROW_PADY)

        # ================= Row 1 =================
        tk.Label(info_frame, text="Start Date", **label_opts).grid(
            row=1, column=0, sticky="w", pady=ROW_PADY, padx=(0, 8)
        )
        self.entry_start_date = DateEntry(
            info_frame, date_pattern=self.DATE_ENTRY_PATTERN, font=("Arial", 11), width=23
        )
        self.entry_start_date.grid(row=1, column=1, sticky="w", pady=ROW_PADY, padx=(0, 20))

        tk.Label(info_frame, text="End Date", **label_opts).grid(
            row=1, column=2, sticky="w", pady=ROW_PADY, padx=(0, 8)
        )
        self.entry_end_date = DateEntry(
            info_frame, date_pattern=self.DATE_ENTRY_PATTERN, font=("Arial", 11), width=23
        )
        self.entry_end_date.grid(row=1, column=3, sticky="w", pady=ROW_PADY)

        # ================= Row 2 =================
        tk.Label(info_frame, text="Reg Open Date", **label_opts).grid(
            row=2, column=0, sticky="w", pady=ROW_PADY, padx=(0, 8)
        )

        # Fixed-width container so this frame lines up exactly like the
        # plain DateEntry widgets above/below it (same total column width).
        open_frame = tk.Frame(info_frame, bg="#f4f6f9", width=280, height=30)
        open_frame.grid(row=2, column=1, sticky="w", pady=ROW_PADY, padx=(0, 20))
        open_frame.grid_propagate(False)

        self.entry_reg_open = DateEntry(
            open_frame, date_pattern=self.DATE_ENTRY_PATTERN, font=("Arial", 11), width=14
        )
        self.entry_reg_open.pack(side=tk.LEFT)

        self.cbo_open_hour = ttk.Combobox(
            open_frame, values=[f"{i:02d}" for i in range(24)], width=3, state="readonly"
        )
        self.cbo_open_hour.current(0)
        self.cbo_open_hour.pack(side=tk.LEFT, padx=2)

        tk.Label(open_frame, text=":", bg="#f4f6f9").pack(side=tk.LEFT)

        self.cbo_open_minute = ttk.Combobox(
            open_frame, values=[f"{i:02d}" for i in range(60)], width=3, state="readonly"
        )
        self.cbo_open_minute.current(0)
        self.cbo_open_minute.pack(side=tk.LEFT, padx=2)

        # Status
        tk.Label(info_frame, text="Status", **label_opts).grid(
            row=2, column=2, sticky="w", pady=ROW_PADY, padx=(0, 8)
        )
        self.combo_status = ttk.Combobox(
            info_frame,
            values=self.STATUS_VALUES,
            state="readonly",
            font=("Arial", 11),
            width=24,
        )
        self.combo_status.current(0)
        self.combo_status.grid(row=2, column=3, sticky="w", pady=ROW_PADY)

        # ================= Row 3 =================
        tk.Label(info_frame, text="Reg Close Date", **label_opts).grid(
            row=3, column=0, sticky="w", pady=ROW_PADY, padx=(0, 8)
        )

        close_frame = tk.Frame(info_frame, bg="#f4f6f9", width=280, height=30)
        close_frame.grid(row=3, column=1, sticky="w", pady=ROW_PADY, padx=(0, 20))
        close_frame.grid_propagate(False)

        self.entry_reg_close = DateEntry(
            close_frame, date_pattern=self.DATE_ENTRY_PATTERN, font=("Arial", 11), width=14
        )
        self.entry_reg_close.pack(side=tk.LEFT)

        self.cbo_close_hour = ttk.Combobox(
            close_frame, values=[f"{i:02d}" for i in range(24)], width=3, state="readonly"
        )
        self.cbo_close_hour.current(0)
        self.cbo_close_hour.pack(side=tk.LEFT, padx=2)

        tk.Label(close_frame, text=":", bg="#f4f6f9").pack(side=tk.LEFT)

        self.cbo_close_minute = ttk.Combobox(
            close_frame, values=[f"{i:02d}" for i in range(60)], width=3, state="readonly"
        )
        self.cbo_close_minute.current(0)
        self.cbo_close_minute.pack(side=tk.LEFT, padx=2)

        tk.Label(
            info_frame,
            text="Format: Date = DD/MM/YYYY | DateTime = DD/MM/YYYY HH:MM",
            font=("Arial", 9, "italic"),
            fg="#666666",
            bg="#f4f6f9",
        ).grid(row=3, column=2, columnspan=2, sticky="w", pady=ROW_PADY)

        # ---------------- Message label ----------------
        self.msg_label = tk.Label(
            self.parent, text="", font=("Arial", 10, "bold"),
            bg="#f4f6f9", fg="#c0392b", anchor="w"
        )
        self.msg_label.pack(fill=tk.X, padx=5)

        # ---------------- Button row ----------------
        btn_frame = tk.Frame(self.parent, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=5, pady=(5, 15))

        btn_opts = {
            "font": ("Arial", 11, "bold"),
            "fg": "white",
            "bd": 0,
            "padx": 10,
            "pady": 8,
            "cursor": "hand2",
        }

        tk.Button(btn_frame, text="Add", bg="#27ae60", command=self.add_period, **btn_opts).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=4
        )
        tk.Button(btn_frame, text="Edit", bg="#f39c12", command=self.edit_period, **btn_opts).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=4
        )
        tk.Button(btn_frame, text="Delete", bg="#f2422e", command=self.delete_period, **btn_opts).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=4
        )
        tk.Button(
            btn_frame,
            text="Open / Close",
            bg="#9b59b6",
            activebackground="#7d3c98",
            command=self.toggle_status,
            **btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        tk.Button(btn_frame, text="Refresh", bg="#3498db", command=self.refresh, **btn_opts).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=4
        )
        tk.Button(
            btn_frame,
            text="Manage Classes",
            bg="#16a085",
            activebackground="#128f76",
            command=self.open_manage_classes,
            **btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        tk.Button(btn_frame, text="Clear", bg="#7f8c8d", command=self.clear_form, **btn_opts).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=4
        )

        # ---------------- Table (Treeview) ----------------
        columns = ("periodID", "semesterName", "startDate", "endDate", "regOpenDate", "regCloseDate", "status")
        headers = ("Period ID", "Semester", "Start Date", "End Date", "Reg Open", "Reg Close", "Status")
        widths = (80, 180, 100, 100, 140, 140, 90)

        table_frame = tk.Frame(self.parent, bg="#f4f6f9")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=26)

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for col, head, w in zip(columns, headers, widths):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=w, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.tag_configure("Open", foreground="#1f8b25")
        self.tree.tag_configure("Closed", foreground="#c23a2f")
        self.tree.tag_configure("Upcoming", foreground="#8a6d00")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------
    def show_msg(self, text, ok=False):
        self.msg_label.config(text=text, fg="#1f8b25" if ok else "#c0392b")

    def clear_form(self):
        today = datetime.today()
        self.entry_period_id.config(state="normal")
        self.entry_period_id.delete(0, tk.END)
        self.entry_semester_name.delete(0, tk.END)
        self.entry_start_date.set_date(today)
        self.entry_end_date.set_date(today)
        self.entry_reg_open.set_date(today)
        self.entry_reg_close.set_date(today)
        self.cbo_open_hour.set("00")
        self.cbo_open_minute.set("00")
        self.cbo_close_hour.set("00")
        self.cbo_close_minute.set("00")
        self.combo_status.current(0)
        self.selected_period_id = None
        self.tree.selection_remove(self.tree.selection())
        self.show_msg("")

    def read_form(self):
        # tkcalendar's DateEntry.get_date() returns a real datetime.date
        # object, sidestepping any locale/format ambiguity that .get()
        # (a plain "dd/mm/yyyy" string) would introduce when sent to SQL Server.
        start_date = self.entry_start_date.get_date()
        end_date = self.entry_end_date.get_date()

        open_date = self.entry_reg_open.get_date()
        open_dt = datetime(
            open_date.year, open_date.month, open_date.day,
            int(self.cbo_open_hour.get()), int(self.cbo_open_minute.get())
        )

        close_date = self.entry_reg_close.get_date()
        close_dt = datetime(
            close_date.year, close_date.month, close_date.day,
            int(self.cbo_close_hour.get()), int(self.cbo_close_minute.get())
        )

        return {
            "periodID": self.entry_period_id.get().strip(),
            "semesterName": self.entry_semester_name.get().strip(),
            "startDate": start_date,      # datetime.date
            "endDate": end_date,          # datetime.date
            "regOpenDate": open_dt,       # datetime.datetime
            "regCloseDate": close_dt,     # datetime.datetime
            "status": self.combo_status.get().strip(),
        }

    def _parse_dates(self, data):
        """startDate/endDate/regOpenDate/regCloseDate are already real
        date/datetime objects (see read_form), so just pass them through."""
        return data["startDate"], data["endDate"], data["regOpenDate"], data["regCloseDate"]

    def validate(self, data, is_edit=False):
        if not all(data.values()):
            return "Please fill in all fields before saving."

        start_dt, end_dt, open_dt, close_dt = self._parse_dates(data)

        if end_dt <= start_dt:
            return "End Date must be after Start Date."

        if close_dt <= open_dt:
            return "Reg Close Date must be after Reg Open Date."

        if not is_edit and self.repo.exists(data["periodID"]):
            return f'Period ID "{data["periodID"]}" already exists.'

        if self.repo.has_overlap(data["periodID"], data["startDate"], data["endDate"]):
            return "__WARNING__ This period's date range overlaps another existing period."

        return None

    # ------------------------------------------------------------------
    # DATA OPERATIONS
    # ------------------------------------------------------------------
    def load_data(self, semester_filter=None):
        try:
            if semester_filter:
                rows = self.repo.get_by_semester(semester_filter)
            else:
                rows = self.repo.get_all()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            period_id, semester_name, start_date, end_date, reg_open, reg_close, status = row
            self.tree.insert(
                "", tk.END,
                iid=period_id,
                values=(
                    period_id,
                    semester_name,
                    start_date.strftime(self.DATE_FMT) if hasattr(start_date, "strftime") else start_date,
                    end_date.strftime(self.DATE_FMT) if hasattr(end_date, "strftime") else end_date,
                    reg_open.strftime(self.DATETIME_FMT) if hasattr(reg_open, "strftime") else reg_open,
                    reg_close.strftime(self.DATETIME_FMT) if hasattr(reg_close, "strftime") else reg_close,
                    status,
                ),
                tags=(status,),
            )

    def on_row_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0], "values")
        self.selected_period_id = values[0]

        self.entry_period_id.delete(0, tk.END)
        self.entry_period_id.insert(0, values[0])
        # Period ID is the primary key - lock it while editing an existing row
        self.entry_period_id.config(state="readonly")

        self.entry_semester_name.delete(0, tk.END)
        self.entry_semester_name.insert(0, values[1])

        # Values coming from the Treeview are always formatted as
        # DATE_FMT / DATETIME_FMT (dd/mm/yyyy), regardless of what
        # DATE_ENTRY_PATTERN the DateEntry widgets themselves display.
        # Convert to real date/datetime objects first so set_date()
        # never has to guess a format.
        start_date_obj = datetime.strptime(values[2], self.DATE_FMT).date()
        end_date_obj = datetime.strptime(values[3], self.DATE_FMT).date()
        self.entry_start_date.set_date(start_date_obj)
        self.entry_end_date.set_date(end_date_obj)

        open_dt_obj = datetime.strptime(values[4], self.DATETIME_FMT)
        self.entry_reg_open.set_date(open_dt_obj.date())
        self.cbo_open_hour.set(f"{open_dt_obj.hour:02d}")
        self.cbo_open_minute.set(f"{open_dt_obj.minute:02d}")

        close_dt_obj = datetime.strptime(values[5], self.DATETIME_FMT)
        self.entry_reg_close.set_date(close_dt_obj.date())
        self.cbo_close_hour.set(f"{close_dt_obj.hour:02d}")
        self.cbo_close_minute.set(f"{close_dt_obj.minute:02d}")

        self.combo_status.set(values[6])
        self.show_msg("")

    def add_period(self):
        self.entry_period_id.config(state="normal")
        data = self.read_form()
        error = self.validate(data, is_edit=False)
        if error:
            if error.startswith("__WARNING__"):
                msg = error.replace("__WARNING__", "").strip()
                if not messagebox.askyesno("Confirm", msg + "\n\nDo you want to continue anyway?"):
                    self.show_msg("Add cancelled.")
                    return
            else:
                self.show_msg(error)
                return
        try:
            self.repo.add(
                data["periodID"],
                data["semesterName"],
                data["startDate"],
                data["endDate"],
                data["regOpenDate"],
                data["regCloseDate"],
                data["status"]
            )
            new_period_id = data["periodID"]
            self.repo.initialize_period_classes(new_period_id)
            self.load_data()
            self.clear_form()
            self.show_msg("Registration period added successfully.", ok=True)

            # Highlight the newly created row
            if self.tree.exists(new_period_id):
                self.tree.selection_set(new_period_id)
                self.tree.see(new_period_id)
            self.selected_period_id = new_period_id

            # Immediately let the admin pick which subjects/classes
            # are opened for students in this new registration period.
            self.open_manage_classes()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def edit_period(self):
        if not self.selected_period_id:
            self.show_msg("Please select a registration period.")
            return
        data = self.read_form()
        data["periodID"] = self.selected_period_id
        error = self.validate(data, is_edit=True)
        if error:
            if error.startswith("__WARNING__"):
                msg = error.replace("__WARNING__", "").strip()
                if not messagebox.askyesno("Confirm", msg + "\n\nDo you want to continue anyway?"):
                    self.show_msg("Edit cancelled.")
                    return
            else:
                self.show_msg(error)
                return
        try:
            self.repo.update(
                data["periodID"],
                data["semesterName"],
                data["startDate"],
                data["endDate"],
                data["regOpenDate"],
                data["regCloseDate"],
                data["status"]
            )
            self.load_data()
            self.show_msg("Registration period updated successfully.", ok=True)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_period(self):
        if not self.selected_period_id:
            self.show_msg("Please select a registration period.")
            return
        if not messagebox.askyesno(
            "Confirm",
            f"Delete registration period {self.selected_period_id}?"
        ):
            return

        try:
            self.repo.delete(self.selected_period_id)
            self.load_data()
            self.clear_form()
            self.show_msg("Registration period deleted successfully.", ok=True)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


    def toggle_status(self):
        if not self.selected_period_id:
            self.show_msg("Please select a registration period.")
            return
        try:
            current = self.repo.get_by_id(self.selected_period_id)
            if not current:
                self.show_msg("Registration period not found.")
                return
            current_status = current[6]
            # Upcoming -> Open
            # Open -> Closed
            # Closed -> Open
            if current_status == "Upcoming":
                new_status = "Open"
            elif current_status == "Open":
                new_status = "Closed"
            else:
                new_status = "Open"
            # Nếu mở một kỳ mới thì đóng tất cả kỳ đang Open trước
            if new_status == "Open":
                self.repo.close_all_open_periods()

            # FIX: update_status() trước đây bị thụt vào bên trong khối
            # "if new_status == 'Open':" nên khi Closed, DB không hề được
            # cập nhật dù UI báo đã đổi. Giờ luôn gọi, bất kể Open/Closed.
            self.repo.update_status(
                self.selected_period_id,
                new_status
            )

            self.combo_status.set(new_status)
            self.load_data()
            self.show_msg(
                f"Status changed to {new_status}.",
                ok=True
            )

            # Sync CourseClass.status of this period so students actually
            # see/can register for its subjects once the period is Open
            # (or stop seeing them once it's Closed).
            if messagebox.askyesno(
                "Sync classes?",
                f'Also set ALL classes in "{self.selected_period_id}" to "{new_status}"?\n\n'
                "(Chỉ những lớp có Status = Open mới hiện ra cho sinh viên đăng ký.\n"
                "Chọn No nếu bạn muốn tự chọn từng môn bằng nút 'Manage Classes'.)"
            ):
                self.repo.set_all_classes_status(self.selected_period_id, new_status)
                self.show_msg(
                    f"Status changed to {new_status} (all classes synced).",
                    ok=True
                )
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def refresh(self):
        self.load_data()
        self.clear_form()
        self.show_msg("Data refreshed.", ok=True)

    # ------------------------------------------------------------------
    # MANAGE CLASSES OPENED IN THIS PERIOD
    # ------------------------------------------------------------------
    def open_manage_classes(self):
        if not self.selected_period_id:
            self.show_msg("Please select a registration period first.")
            return

        period_id = self.selected_period_id
        self.repo.initialize_period_classes(period_id)

        win = tk.Toplevel(self.parent)
        win.title(f"Manage Classes - {period_id}")
        win.geometry("780x430")
        win.configure(bg="#f4f6f9")
        win.grab_set()  # modal

        tk.Label(
            win, text=f"Classes in Registration Period: {period_id}",
            font=("Arial", 14, "bold"), bg="#f4f6f9"
        ).pack(pady=(12, 10))

        columns = ("classID", "subjectName", "lecturer", "day", "capacity", "status")
        headers = ("Class ID", "Subject", "Lecturer", "Day", "Enrolled/Max", "Status")
        widths = (80, 220, 150, 90, 100, 90)

        table_frame = tk.Frame(win, bg="#f4f6f9")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15)

        class_tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")
        for col, head, w in zip(columns, headers, widths):
            class_tree.heading(col, text=head)
            class_tree.column(col, width=w, anchor="center")

        vscroll = ttk.Scrollbar(table_frame, orient="vertical", command=class_tree.yview)
        class_tree.configure(yscrollcommand=vscroll.set)
        class_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        class_tree.tag_configure("Open", foreground="#1f8b25")
        class_tree.tag_configure("Closed", foreground="#c23a2f")
        class_tree.tag_configure("Upcoming", foreground="#8a6d00")

        def load_classes():
            class_tree.delete(*class_tree.get_children())
            try:
                rows = self.repo.get_classes_by_period(period_id)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
                return
            for row in rows:
                class_id, subject_name, lecturer_name, day, max_cap, enrolled, status = row
                class_tree.insert(
                    "", tk.END, iid=class_id,
                    values=(class_id, subject_name, lecturer_name, day,
                            f"{enrolled}/{max_cap}", status),
                    tags=(status,),
                )

        def apply_status(new_status, to_all=False):
            try:
                if to_all:
                    if not messagebox.askyesno(
                        "Confirm",
                        f'Set ALL classes in "{period_id}" to "{new_status}"?'
                    ):
                        return
                    self.repo.set_all_classes_status(period_id, new_status)
                else:
                    selected = class_tree.selection()
                    if not selected:
                        messagebox.showwarning("Warning", "Please select at least one class.")
                        return
                    for class_id in selected:
                        self.repo.set_class_status(period_id, class_id,new_status)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
                return
            load_classes()

        info = tk.Label(
            win,
            text="Chỉ những lớp có Status = Open mới hiện ra cho sinh viên đăng ký.",
            font=("Arial", 9, "italic"), fg="#666666", bg="#f4f6f9"
        )
        info.pack(pady=(6, 0))

        btn_row = tk.Frame(win, bg="#f4f6f9")
        btn_row.pack(fill=tk.X, padx=15, pady=12)

        dialog_btn_opts = {
            "font": ("Arial", 10, "bold"), "fg": "white", "bd": 0,
            "padx": 8, "pady": 7, "cursor": "hand2",
        }

        tk.Button(
            btn_row, text="Open Selected", bg="#27ae60", activebackground="#219150",
            command=lambda: apply_status("Open"), **dialog_btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        tk.Button(
            btn_row, text="Close Selected", bg="#e74c3c", activebackground="#c0392b",
            command=lambda: apply_status("Closed"), **dialog_btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        tk.Button(
            btn_row, text="Open All", bg="#2ecc71", activebackground="#27ae60",
            command=lambda: apply_status("Open", to_all=True), **dialog_btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        tk.Button(
            btn_row, text="Close All", bg="#c0392b", activebackground="#922b21",
            command=lambda: apply_status("Closed", to_all=True), **dialog_btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        tk.Button(
            btn_row, text="Refresh", bg="#3498db", activebackground="#2874a6",
            command=load_classes, **dialog_btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        tk.Button(
            btn_row, text="Close Window", bg="#7f8c8d", activebackground="#616a6b",
            command=win.destroy, **dialog_btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        load_classes()