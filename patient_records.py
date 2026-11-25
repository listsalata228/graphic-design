
# Designed with https://visualtkinter.com
import tkinter as tk
from tkinter import ttk, messagebox


THEME_BG = "#d4ecf7"
THEME_FG = "#1a1a1a"
THEME_ACCENT = "#2a7de1"
THEME_ACCENT_FG = "#ffffff"
THEME_FIELD_BG = "#ffffff"
THEME_FONT = ("Helvetica", 10)


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


class Application:
    def __init__(self, root):
        self.root = root

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
        pass

    def on_button2(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
