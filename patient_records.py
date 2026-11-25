import tkinter as tk
from tkinter import ttk, messagebox


#основные цвета приложения
THEME_BG = "#d4ecf7"
THEME_FG = "#1a1a1a"
THEME_ACCENT = "#2a7de1"
THEME_ACCENT_FG = "#ffffff"
THEME_FIELD_BG = "#ffffff"
THEME_FONT = ("Helvetica", 10)

#цвета и шрифт главной страницы
BUTTON_BG = "#fff0fc"
BUTTON_FG = "#4e7179"
FLOWERS_FG = "#897da6"
BUTTON_FONT = ("Helvetica", 12, "bold italic")


def apply_theme(root):
    """Настраивает общую цветовую тему приложения."""
    root.configure(bg=THEME_BG)
    root.option_add("*background", THEME_BG)
    root.option_add("*foreground", THEME_FG)
    root.option_add("*font", THEME_FONT)
    root.option_add("*Entry.background", THEME_FIELD_BG)
    root.option_add("*Text.background", THEME_FIELD_BG)
    root.option_add("*Listbox.background", THEME_FIELD_BG)

    # Для ttk-виджетов выбираем тему, в которой можно задавать цвета.
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


def make_button(parent, text, command, width=None, height=None):
    """Создаёт обычную прямоугольную объёмную кнопку Tkinter."""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        fg=BUTTON_FG,
        bg=BUTTON_BG,
        activebackground="#f4dff0",
        activeforeground=BUTTON_FG,
        font=BUTTON_FONT,
        relief=tk.RAISED,
        borderwidth=4,
        highlightthickness=1
    )

    if width is not None:
        button.configure(width=width)
    if height is not None:
        button.configure(height=height)

    return button


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Мой учетчик")
        self.root.geometry("520x383")
        self.root.resizable(False, False)
        apply_theme(self.root)

        # Пока список пустой. На следующих этапах сюда будут добавляться пациенты.
        self.patients = []

        # Все три страницы находятся в одном главном окне.
        self.home_frame = tk.Frame(self.root, bg=THEME_BG)
        self.patients_frame = tk.Frame(self.root, bg=THEME_BG)
        self.statistics_frame = tk.Frame(self.root, bg=THEME_BG)

        self.create_home_page()
        self.create_patients_page()
        self.create_statistics_page()

        self.show_home()

    def hide_all_pages(self):
        """Скрывает все страницы перед показом нужной."""
        self.home_frame.pack_forget()
        self.patients_frame.pack_forget()
        self.statistics_frame.pack_forget()

    def show_home(self):
        """Показывает главную страницу и возвращает исходный размер окна."""
        self.hide_all_pages()
        self.root.geometry("520x383")
        self.root.resizable(False, False)
        self.home_frame.pack(fill="both", expand=True)

    def show_patients(self):
        """Показывает страницу пациентов и обновляет таблицу."""
        self.hide_all_pages()
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        self.patients_frame.pack(fill="both", expand=True)
        self.update_table()

    def show_statistics(self):
        """Показывает страницу сводной статистики."""
        self.hide_all_pages()
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        self.statistics_frame.pack(fill="both", expand=True)

    def create_home_page(self):
        """Создаёт главную страницу в соответствии с твоим дизайном."""
        # Декоративные цветы сверху — сохраняем текст и расположение из твоего кода.
        self.label_flowers = tk.Label(
            self.home_frame,
            text="❀ ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀  ✿  ❀",
            fg=FLOWERS_FG,
            bg=THEME_BG,
            font=("Helvetica", 21)
        )
        self.label_flowers.place(x=0, y=10, width=520, height=70)

        # Главные кнопки оставлены на тех же местах и с тем же размером.
        self.button_patients = make_button(
            self.home_frame,
            "Мои пациенты",
            self.show_patients
        )
        self.button_patients.place(x=155, y=120, width=210, height=40)

        self.button_statistics = make_button(
            self.home_frame,
            "Сводная статистика",
            self.show_statistics
        )
        self.button_statistics.place(x=155, y=190, width=210, height=40)

        # Надпись внизу слева работает как ссылка-кнопка.
        self.label_complaint = tk.Label(
            self.home_frame,
            text="хочу оставить жалобу",
            fg=BUTTON_FG,
            bg=THEME_BG,
            font=("Helvetica", 8),
            cursor="hand2"
        )
        self.label_complaint.place(x=10, y=357, width=135, height=26)
        self.label_complaint.bind("<Button-1>", self.show_complaint)

    def create_patients_page(self):
        """Создаёт страницу со списком пациентов и таблицей."""
        # Верхняя часть: кнопка «Назад», заголовок и кнопки управления.
        header_frame = tk.Frame(self.patients_frame, bg=THEME_BG)
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=2)
        header_frame.grid_columnconfigure(2, weight=1)

        back_button = make_button(
            header_frame,
            "Назад",
            self.show_home
        )
        back_button.grid(row=0, column=0, sticky="w", padx=(0, 5))

        title = tk.Label(
            header_frame,
            text="Мои пациенты",
            bg=THEME_BG,
            fg=BUTTON_FG,
            font=("Helvetica", 18, "bold")
        )
        title.grid(row=0, column=1)

        # По задумке кнопка редактирования располагается над кнопкой добавления.
        actions_frame = tk.Frame(header_frame, bg=THEME_BG)
        actions_frame.grid(row=0, column=2, sticky="e")

        edit_button = make_button(
            actions_frame,
            "Отредактировать",
            self.show_edit_placeholder
        )
        edit_button.pack(fill="x", pady=(0, 5))

        add_button = make_button(
            actions_frame,
            "Добавить",
            self.show_add_placeholder
        )
        add_button.pack(fill="x")

        # Область таблицы занимает всё оставшееся место страницы.
        table_frame = tk.Frame(self.patients_frame, bg=THEME_BG)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        columns = ("name", "age", "sex", "height", "weight", "bmi")
        self.patient_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Patients.Treeview"
        )

        # Названия и ширина столбцов таблицы.
        self.patient_table.heading("name", text="ФИО")
        self.patient_table.heading("age", text="Возраст")
        self.patient_table.heading("sex", text="Пол")
        self.patient_table.heading("height", text="Рост, см")
        self.patient_table.heading("weight", text="Вес, кг")
        self.patient_table.heading("bmi", text="ИМТ")

        self.patient_table.column("name", width=280, minwidth=180, anchor="w")
        self.patient_table.column("age", width=100, minwidth=70, anchor="center")
        self.patient_table.column("sex", width=90, minwidth=60, anchor="center")
        self.patient_table.column("height", width=120, minwidth=80, anchor="center")
        self.patient_table.column("weight", width=120, minwidth=80, anchor="center")
        self.patient_table.column("bmi", width=120, minwidth=80, anchor="center")

        # Настраиваем вид таблицы в общей цветовой гамме.
        style = ttk.Style(self.root)
        style.configure(
            "Patients.Treeview",
            background="white",
            fieldbackground="white",
            foreground=THEME_FG,
            rowheight=30,
            font=("Helvetica", 10)
        )
        style.configure(
            "Patients.Treeview.Heading",
            background=BUTTON_BG,
            foreground=BUTTON_FG,
            font=("Helvetica", 10, "bold"),
            relief="raised"
        )
        style.map(
            "Patients.Treeview",
            background=[("selected", "#c8e5f2")],
            foreground=[("selected", THEME_FG)]
        )

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.patient_table.yview
        )
        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.patient_table.xview
        )

        self.patient_table.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.patient_table.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        self.empty_table_label = tk.Label(
            table_frame,
            text="Пока нет пациентов. Нажми «Добавить», чтобы создать первую запись.",
            bg=THEME_BG,
            fg=BUTTON_FG,
            font=("Helvetica", 10, "italic")
        )
        self.empty_table_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Обновляем таблицу при первом открытии страницы.
        self.update_table()

    def update_table(self):
        """Удаляет старые строки и заново показывает текущий список пациентов."""
        # Сначала очищаем таблицу, чтобы записи не дублировались.
        for row in self.patient_table.get_children():
            self.patient_table.delete(row)

        # Затем добавляем в таблицу все записи из списка пациентов.
        for patient in self.patients:
            self.patient_table.insert(
                "",
                "end",
                values=(
                    patient["name"],
                    patient["age"],
                    patient["sex"],
                    patient["height"],
                    patient["weight"],
                    patient["bmi"]
                )
            )

        # Если список пуст, показываем подсказку под таблицей.
        if self.patients:
            self.empty_table_label.grid_remove()
        else:
            self.empty_table_label.grid()

    def show_add_placeholder(self):
        """Временное сообщение: форму добавления сделаем на следующем этапе."""
        messagebox.showinfo(
            "Добавление пациента",
            "Форму добавления пациента мы сделаем на следующем этапе."
        )

    def show_edit_placeholder(self):
        """Временное сообщение: редактирование сделаем отдельным этапом."""
        messagebox.showinfo(
            "Редактирование пациента",
            "Выбор пациента и форму редактирования мы добавим на следующем этапе."
        )

    def create_statistics_page(self):
        """Пока создаёт основу страницы статистики; графики добавим отдельным этапом."""
        back_button = make_button(
            self.statistics_frame,
            "Назад",
            self.show_home
        )
        back_button.place(x=20, y=20, width=100, height=35)

        title = tk.Label(
            self.statistics_frame,
            text="Сводная статистика",
            bg=THEME_BG,
            fg=BUTTON_FG,
            font=("Helvetica", 18, "bold")
        )
        title.pack(pady=(25, 10))

        message = tk.Label(
            self.statistics_frame,
            text="Здесь будут размещены четыре графика по данным пациентов.",
            bg=THEME_BG,
            fg=THEME_FG,
            font=("Helvetica", 12)
        )
        message.pack(pady=30)

    def show_complaint(self, event=None):
        """Открывает шуточное красное окно с надписью «НЕТ»."""
        complaint_window = tk.Toplevel(self.root)
        complaint_window.title("Жалоба")
        complaint_window.configure(bg="red")
        complaint_window.resizable(False, False)
        complaint_window.transient(self.root)

        # Размещаем небольшое окно по центру главного окна.
        complaint_window.update_idletasks()
        window_width = 300
        window_height = 170
        x = self.root.winfo_rootx() + (self.root.winfo_width() - window_width) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - window_height) // 2
        complaint_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        no_label = tk.Label(
            complaint_window,
            text="НЕТ",
            bg="red",
            fg="black",
            font=("Helvetica", 38, "bold")
        )
        no_label.pack(expand=True, fill="both")

        close_button = tk.Button(
            complaint_window,
            text="Закрыть",
            command=complaint_window.destroy,
            bg="#fff0fc",
            fg="#4e7179",
            font=("Helvetica", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=4
        )
        close_button.pack(pady=(0, 10))

        complaint_window.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
