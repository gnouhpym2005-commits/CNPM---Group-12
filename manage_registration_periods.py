import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.registration_repository import RegistrationPeriodRepository


class ManageRegistrationPeriodsApp:
   
    STATUS_VALUES = ["Upcoming", "Open", "Closed"]

    DATE_FMT = "%d/%m/%Y"
    DATETIME_FMT = "%d/%m/%Y %H:%M"

    def __init__(self, parent):
        self.parent = parent
        self.repo = RegistrationPeriodRepository()
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

        label_opts = {"font": ("Arial", 11), "bg": "#f4f6f9", "anchor": "w"}
        entry_opts = {"font": ("Arial", 11), "width": 26}

        # Row 0: Period ID | Semester Name
        tk.Label(info_frame, text="Period ID", **label_opts).grid(row=0, column=0, sticky="w", pady=6, padx=(0, 8))
        self.entry_period_id = tk.Entry(info_frame, **entry_opts)
        self.entry_period_id.grid(row=0, column=1, pady=6, padx=(0, 40))

        tk.Label(info_frame, text="Semester Name", **label_opts).grid(row=0, column=2, sticky="w", pady=6, padx=(0, 8))
        self.entry_semester_name = tk.Entry(info_frame, **entry_opts)
        self.entry_semester_name.grid(row=0, column=3, pady=6)

        # Row 1: Start Date | End Date
        tk.Label(info_frame, text="Start Date", **label_opts).grid(row=1, column=0, sticky="w", pady=6, padx=(0, 8))
        self.entry_start_date = tk.Entry(info_frame, **entry_opts)
        self.entry_start_date.grid(row=1, column=1, pady=6, padx=(0, 40))

        tk.Label(info_frame, text="End Date", **label_opts).grid(row=1, column=2, sticky="w", pady=6, padx=(0, 8))
        self.entry_end_date = tk.Entry(info_frame, **entry_opts)
        self.entry_end_date.grid(row=1, column=3, pady=6)

        # Row 2: Reg Open Date | Reg Close Date
        tk.Label(info_frame, text="Reg Open Date", **label_opts).grid(row=2, column=0, sticky="w", pady=6, padx=(0, 8))
        self.entry_reg_open = tk.Entry(info_frame, **entry_opts)
        self.entry_reg_open.grid(row=2, column=1, pady=6, padx=(0, 40))

        tk.Label(info_frame, text="Reg Close Date", **label_opts).grid(row=2, column=2, sticky="w", pady=6, padx=(0, 8))
        self.entry_reg_close = tk.Entry(info_frame, **entry_opts)
        self.entry_reg_close.grid(row=2, column=3, pady=6)

        # Row 3: Status | format hint
        tk.Label(info_frame, text="Status", **label_opts).grid(row=3, column=0, sticky="w", pady=6, padx=(0, 8))
        self.combo_status = ttk.Combobox(
            info_frame, values=self.STATUS_VALUES, state="readonly",
            font=("Arial", 11), width=24
        )
        self.combo_status.current(0)
        self.combo_status.grid(row=3, column=1, pady=6, padx=(0, 40))

        tk.Label(
            info_frame,
            text="Format: Date = YYYY-MM-DD   |   DateTime = YYYY-MM-DD HH:MM",
            font=("Arial", 9, "italic"),
            fg="#666666",
            bg="#f4f6f9",
        ).grid(row=3, column=2, columnspan=2, sticky="w", pady=6)

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

        tk.Button(
            btn_frame, text="Add", bg="#27ae60", activebackground="#219150",
            command=self.add_period, **btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

        tk.Button(
            btn_frame, text="Edit", bg="#f39c12", activebackground="#d68910",
            command=self.edit_period, **btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

        tk.Button(
            btn_frame, text="Open / Close", bg="#e74c3c", activebackground="#c0392b",
            command=self.toggle_status, **btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

        tk.Button(
            btn_frame, text="Clear", bg="#7f8c8d", activebackground="#616a6b",
            command=self.clear_form, **btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

        tk.Button(
            btn_frame, text="Refresh", bg="#3498db", activebackground="#2874a6",
            command=self.refresh, **btn_opts
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

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
        self.entry_period_id.config(state="normal")
        self.entry_period_id.delete(0, tk.END)
        self.entry_semester_name.delete(0, tk.END)
        self.entry_start_date.delete(0, tk.END)
        self.entry_end_date.delete(0, tk.END)
        self.entry_reg_open.delete(0, tk.END)
        self.entry_reg_close.delete(0, tk.END)
        self.combo_status.current(0)
        self.selected_period_id = None
        self.tree.selection_remove(self.tree.selection())
        self.show_msg("")

    def read_form(self):
        return {
            "periodID": self.entry_period_id.get().strip(),
            "semesterName": self.entry_semester_name.get().strip(),
            "startDate": self.entry_start_date.get().strip(),
            "endDate": self.entry_end_date.get().strip(),
            "regOpenDate": self.entry_reg_open.get().strip(),
            "regCloseDate": self.entry_reg_close.get().strip(),
            "status": self.combo_status.get().strip(),
        }

    def _parse_dates(self, data):
        """Returns (start_dt, end_dt, open_dt, close_dt) or raises ValueError."""
        start_dt = datetime.strptime(data["startDate"], self.DATE_FMT)
        end_dt = datetime.strptime(data["endDate"], self.DATE_FMT)
        open_dt = datetime.strptime(data["regOpenDate"], self.DATETIME_FMT)
        close_dt = datetime.strptime(data["regCloseDate"], self.DATETIME_FMT)
        return start_dt, end_dt, open_dt, close_dt

    def validate(self, data, is_edit=False):
        if not all(data.values()):
            return "Please fill in all fields before saving."

        try:
            start_dt, end_dt, open_dt, close_dt = self._parse_dates(data)
        except ValueError:
            return ("Invalid date format. Use YYYY-MM-DD for Start/End Date "
                    "and YYYY-MM-DD HH:MM for Reg Open/Close Date.")

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

        self.entry_start_date.delete(0, tk.END)
        self.entry_start_date.insert(0, values[2])

        self.entry_end_date.delete(0, tk.END)
        self.entry_end_date.insert(0, values[3])

        self.entry_reg_open.delete(0, tk.END)
        self.entry_reg_open.insert(0, values[4])

        self.entry_reg_close.delete(0, tk.END)
        self.entry_reg_close.insert(0, values[5])

        self.combo_status.set(values[6])
        self.show_msg("")

    def add_period(self):
        self.entry_period_id.config(state="normal")
        data = self.read_form()
        error = self.validate(data, is_edit=False)

        warning = None
        if error and error.startswith("__WARNING__"):
            warning = error.replace("__WARNING__ ", "")
        elif error:
            self.show_msg(error)
            return

        try:
            self.repo.add(
                data["periodID"], data["semesterName"], data["startDate"], data["endDate"],
                data["regOpenDate"], data["regCloseDate"], data["status"],
            )
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.load_data()
        self.clear_form()
        if warning:
            self.show_msg(f'Period created, but {warning[0].lower()}{warning[1:]}')
        else:
            self.show_msg(f'Registration period "{data["periodID"]}" created successfully.', ok=True)

    def edit_period(self):
        if not self.selected_period_id:
            self.show_msg("Please select a registration period from the table to edit.")
            return

        data = self.read_form()
        data["periodID"] = self.selected_period_id  # enforce, entry is readonly anyway

        error = self.validate(data, is_edit=True)
        warning = None
        if error and error.startswith("__WARNING__"):
            warning = error.replace("__WARNING__ ", "")
        elif error:
            self.show_msg(error)
            return

        try:
            self.repo.update(
                data["periodID"], data["semesterName"], data["startDate"], data["endDate"],
                data["regOpenDate"], data["regCloseDate"], data["status"],
            )
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.load_data()
        if warning:
            self.show_msg(f'Period updated, but {warning[0].lower()}{warning[1:]}')
        else:
            self.show_msg(f'Registration period "{data["periodID"]}" updated successfully.', ok=True)

    def toggle_status(self):
        if not self.selected_period_id:
            self.show_msg("Please select a registration period from the table first.")
            return

        try:
            current = self.repo.get_by_id(self.selected_period_id)
            if not current:
                self.show_msg("Selected period no longer exists.")
                return

            current_status = current[6]
            new_status = "Closed" if current_status == "Open" else "Open"

            self.repo.update_status(self.selected_period_id, new_status)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.combo_status.set(new_status)
        self.load_data()
        self.show_msg(f'Registration for "{self.selected_period_id}" is now {new_status}.', ok=True)

    def refresh(self):
        semester_filter = self.entry_semester_name.get().strip()
        self.load_data(semester_filter=semester_filter if semester_filter else None)
        if semester_filter:
            self.show_msg(f'Filtered by semester containing "{semester_filter}".', ok=True)
        else:
            self.show_msg("List refreshed.", ok=True)