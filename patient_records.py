import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox


THEME_BG = "#d4ecf7"
THEME_FG = "#1a1a1a"
THEME_ACCENT = "#2a7de1"
THEME_ACCENT_FG = "#ffffff"
THEME_FIELD_BG = "#ffffff"
THEME_FONT = ("Helvetica", 10)


DATABASE = Path(__file__).with_name("patient_records.sqlite3")
SEX_OPTIONS = ("Женский", "Мужской")
FIELDS = ("name", "age", "sex", "height", "weight")
LABELS = ("ФИО", "Возраст", "Пол", "Рост, см", "Вес, кг")


def apply_theme(root):
    """Настройка общего оформления приложения."""
    root.configure(bg=THEME_BG)
    root.option_add("*background", THEME_BG)
    root.option_add("*foreground", THEME_FG)
    root.option_add("*font", THEME_FONT)
    root.option_add("*Entry.background", THEME_FIELD_BG)
    root.option_add("*Text.background", THEME_FIELD_BG)
    root.option_add("*Listbox.background", THEME_FIELD_BG)
    root.option_add("*Button.background", THEME_ACCENT)
    root.option_add("*Button.foreground", THEME_ACCENT_FG)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        ".",
        background=THEME_BG,
        foreground=THEME_FG,
        fieldbackground=THEME_FIELD_BG,
        font=THEME_FONT
    )


def open_database(path):
    database = sqlite3.connect(path)
    database.row_factory = sqlite3.Row
    with database:
        database.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY, name TEXT NOT NULL,
                age INTEGER NOT NULL, sex TEXT NOT NULL,
                height REAL NOT NULL, weight REAL NOT NULL
            )
        """)
    return database


def check_values(name, age, sex, height, weight):
    name = name.strip()
    if not name:
        raise ValueError("Введите ФИО.")
    if sex not in SEX_OPTIONS:
        raise ValueError("Выберите пол.")
    try:
        age = int(age)
        height = float(height.replace(",", "."))
        weight = float(weight.replace(",", "."))
    except ValueError:
        raise ValueError("Укажите возраст целым числом, а рост и вес — числами.") from None

    if not 0 <= age <= 130:
        raise ValueError("Возраст должен быть от 0 до 130 лет.")
    if not 1 <= height <= 300:
        raise ValueError("Рост должен быть от 1 до 300 см.")
    if not 0.01 <= weight <= 1000:
        raise ValueError("Вес должен быть от 0,01 до 1000 кг.")
    return name, age, sex, height, weight


def save_patient(database, values, patient_id=None):
    with database:
        if patient_id is None:
            database.execute(
                "INSERT INTO patients (name, age, sex, height, weight) VALUES (?, ?, ?, ?, ?)",
                values,
            )
        else:
            result = database.execute(
                "UPDATE patients SET name=?, age=?, sex=?, height=?, weight=? WHERE id=?",
                (*values, patient_id),
            )
            if result.rowcount == 0:
                raise ValueError("Эта запись больше не существует.")


def bmi(patient):
    return patient["weight"] / (patient["height"] / 100) ** 2


def count_groups(patients, field, limits):
    counts = [0, 0, 0, 0]
    for patient in patients:
        group = 0
        for limit in limits:
            if patient[field] >= limit:
                group += 1
        counts[group] += 1
    return counts


class Application:
    def __init__(self, root, database):
        self.root = root
        self.database = database
        self.page = None

        root.title("Мой учетчик")
        root.geometry("520x383")
        root.resizable(False, False)

        apply_theme(root)

        # Кнопка перехода к пациентам
        self.w = tk.Button(
            root,
            text="Мои пациенты",
            command=self.on_w,
            fg="#4e7179",
            bg="#fff0fc",
            font=("Helvetica", 12, "bold italic"),
            relief=tk.RAISED
        )
        self.w.place(x=155, y=120, width=210, height=40)

        # Кнопка перехода к статистике
        self.button2 = tk.Button(
            root,
            text="Сводная статистика",
            command=self.on_button2,
            fg="#4e7179",
            bg="#fff0fc",
            font=("Helvetica", 12, "bold italic"),
            relief=tk.RAISED
        )
        self.button2.place(x=155, y=190, width=210, height=40)

        # Цветочное оформление
        self.label1 = tk.Label(
            root,
            text="❀ ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀  ",
            fg="#897da6",
            font=("Helvetica", 21)
        )
        self.label1.place(x=0, y=10, width=520, height=70)

        # Надпись для открытия окна жалобы
        self.label2 = tk.Label(
            root,
            text="ваши жалобы",
            font=("Helvetica", 8),
            cursor="hand2"
        )
        self.label2.place(x=10, y=357, width=90, height=26)

        self.label2.bind("<Button-1>", self.show_complaint)

    # Открытие окна жалобы
    def show_complaint(self, event=None):
        complaint_window = tk.Toplevel(self.root)
        complaint_window.title("Жалоба")
        complaint_window.geometry("300x180")
        complaint_window.configure(bg="red")
        complaint_window.resizable(False, False)

        # Размещение окна по центру главного окна
        self.root.update_idletasks()

        x = self.root.winfo_x() + (520 - 300) // 2
        y = self.root.winfo_y() + (383 - 180) // 2

        complaint_window.geometry(f"300x180+{x}+{y}")

        # Надпись НЕТ
        no_label = tk.Label(
            complaint_window,
            text="НЕТ",
            bg="red",
            fg="black",
            font=("Helvetica", 35, "bold")
        )
        no_label.pack(expand=True)

        # Кнопка закрытия
        close_button = tk.Button(
            complaint_window,
            text="Закрыть",
            command=complaint_window.destroy,
            relief=tk.RAISED
        )
        close_button.pack(pady=10)

    def on_w(self):
        self.show_patients()

    def on_button2(self):
        self.show_statistics()

    def open_page(self):
        if self.page is None:
            self.page = tk.Frame(self.root, bg=THEME_BG, padx=16, pady=12)
            self.page.place(x=0, y=0, relwidth=1, relheight=1)
        for widget in self.page.winfo_children():
            widget.destroy()
        self.root.resizable(True, True)
        self.root.minsize(700, 440)
        self.root.geometry("760x490")

    def close_page(self):
        self.page.destroy()
        self.page = None
        self.root.minsize(1, 1)
        self.root.geometry("520x383")
        self.root.resizable(False, False)

    def read_patients(self):
        try:
            return self.database.execute("SELECT * FROM patients ORDER BY id").fetchall()
        except sqlite3.Error as error:
            messagebox.showerror("Ошибка чтения записей", str(error), parent=self.root)
            return None

    def show_patients(self):
        patients = self.read_patients()
        if patients is None:
            return
        self.open_page()

        buttons = tk.Frame(self.page, bg=THEME_BG)
        buttons.pack(fill="x", pady=(0, 10))
        tk.Label(buttons, text="Мои пациенты", bg=THEME_BG,
                 font=("Helvetica", 13, "bold")).pack(side="left", padx=12)
        tk.Button(buttons, text="Назад", command=self.close_page).pack(side="left")
        tk.Button(buttons, text="Добавить", command=self.patient_form).pack(side="right")
        tk.Button(buttons, text="Отредактировать", command=self.edit_patient).pack(
            side="right", padx=8
        )

        self.patients = {str(patient["id"]): patient for patient in patients}
        table_box = ttk.Frame(self.page)
        table_box.pack(fill="both", expand=True)
        columns = (*FIELDS, "bmi")
        self.table = ttk.Treeview(table_box, columns=columns, show="headings", selectmode="browse")
        scrollbar = ttk.Scrollbar(table_box, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)
        for field, label in zip(columns, (*LABELS, "ИМТ")):
            self.table.heading(field, text=label)
            self.table.column(field, width=215 if field == "name" else 83, minwidth=65)
        for patient_id, patient in self.patients.items():
            values = [patient[field] for field in FIELDS]
            self.table.insert("", "end", iid=patient_id, values=(*values, f"{bmi(patient):.2f}"))
        if not patients:
            tk.Label(self.page, text="Пока нет записей. Нажмите «Добавить».", bg=THEME_BG).pack(pady=5)

    def edit_patient(self):
        selected = self.table.selection()
        if selected:
            self.patient_form(self.patients[selected[0]])
        else:
            messagebox.showinfo("Редактирование", "Выберите строку в таблице.", parent=self.root)

    def patient_form(self, patient=None):
        form = tk.Toplevel(self.root)
        form.title("Редактировать пациента" if patient else "Добавить пациента")
        form.transient(self.root)
        form.resizable(False, False)
        entries = []
        for row, (field, label) in enumerate(zip(FIELDS, LABELS)):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            if field == "sex":
                entry = ttk.Combobox(form, values=SEX_OPTIONS, state="readonly", width=25)
                if patient is not None:
                    entry.set(patient[field])
            else:
                entry = ttk.Entry(form, width=28)
                if patient is not None:
                    entry.insert(0, str(patient[field]))
            entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
            entries.append(entry)

        def save():
            try:
                values = check_values(*(entry.get() for entry in entries))
                patient_id = patient["id"] if patient is not None else None
                save_patient(self.database, values, patient_id)
            except (ValueError, sqlite3.Error) as error:
                messagebox.showerror("Запись не сохранена", str(error), parent=form)
                return
            form.destroy()
            self.show_patients()

        ttk.Button(form, text="Сохранить", command=save).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(form, text="Отмена", command=form.destroy).grid(row=5, column=1, pady=10)
        form.bind("<Return>", lambda event: save())
        form.bind("<Escape>", lambda event: form.destroy())
        form.wait_visibility()
        form.grab_set()
        entries[0].focus_set()

    def show_statistics(self):
        patients = self.read_patients()
        if patients is None:
            return
        self.open_page()
        tk.Button(self.page, text="Назад", command=self.close_page).pack(anchor="w")
        tk.Label(self.page, text="Сводная статистика", bg=THEME_BG,
                 font=("Helvetica", 16, "bold")).pack()
        if not patients:
            tk.Label(self.page, text="Добавьте пациента, чтобы увидеть графики.", bg=THEME_BG).pack(pady=18)
            return

        average = sum(bmi(patient) for patient in patients) / len(patients)
        tk.Label(self.page, text=f"Пациентов: {len(patients)}    Средний ИМТ: {average:.2f}",
                 bg=THEME_BG).pack(pady=6)
        charts = tk.Frame(self.page, bg=THEME_BG)
        charts.pack()
        sex_counts = [sum(patient["sex"] == sex for patient in patients) for sex in SEX_OPTIONS]
        data = (
            ("Возраст, лет", ("<18", "18–39", "40–59", "60+"), count_groups(patients, "age", (18, 40, 60))),
            ("Пол", SEX_OPTIONS, sex_counts),
            ("Рост, см", ("<150", "150–<170", "170–<190", "190+"), count_groups(patients, "height", (150, 170, 190))),
            ("Вес, кг", ("<50", "50–<70", "70–<90", "90+"), count_groups(patients, "weight", (50, 70, 90))),
        )
        for index, (title, labels, counts) in enumerate(data):
            chart = draw_chart(charts, title, labels, counts)
            chart.grid(row=index // 2, column=index % 2, padx=5, pady=5)


def draw_chart(parent, title, labels, counts):
    canvas = tk.Canvas(parent, width=310, height=140, bg="white", highlightthickness=0)
    canvas.create_text(10, 14, text=title, anchor="w", font=("Helvetica", 10, "bold"))
    largest_count = max(1, max(counts))
    for row, (label, count) in enumerate(zip(labels, counts)):
        y = 40 + 25 * row
        bar_end = 90 + 185 * count / largest_count
        canvas.create_text(10, y, text=label, anchor="w")
        if count:
            canvas.create_rectangle(90, y - 6, bar_end, y + 6, fill="#2a7de1", outline="")
        canvas.create_text(bar_end + 5, y, text=str(count), anchor="w")
    return canvas


def main():
    root = tk.Tk()
    try:
        database = open_database(DATABASE)
    except sqlite3.Error as error:
        root.withdraw()
        messagebox.showerror("Не удалось открыть базу данных", str(error), parent=root)
        root.destroy()
        return
    try:
        Application(root, database)
        root.mainloop()
    finally:
        database.close()


if __name__ == "__main__":
    main()
