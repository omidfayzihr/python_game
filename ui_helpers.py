import tkinter as tk
from tkinter import font
import sys

_app = None


class App:
    # Main GUI application class for the adventure game
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚔️ Adventure Game")
        self.root.geometry("700x500")
        self.root.configure(bg="#1a1a2e")

        try:
            self.root.attributes("-topmost", True)
            self.root.after(
                200, lambda: self.root.attributes("-topmost", False))
        except Exception:
            pass

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.text_font = font.Font(family="Arial", size=11)
        self.hud_font = font.Font(family="Consolas", size=10)

        self.hud_frame = tk.Frame(self.root, bg="#16213e", height=50)
        self.hud_frame.pack(fill="x", padx=0, pady=0)
        self.hud_frame.pack_propagate(False)

        self.hud = tk.Label(
            self.hud_frame,
            text="—",
            font=self.hud_font,
            bg="#16213e",
            fg="#00d9ff",
            anchor="w",
            padx=15,
            pady=10
        )
        self.hud.pack(fill="both", expand=True)

        self.content_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.title_lbl = tk.Label(
            self.content_frame,
            text="",
            font=self.title_font,
            bg="#1a1a2e",
            fg="#f39c12",
            wraplength=640
        )
        self.title_lbl.pack(pady=(5, 10))

        self.text_lbl = tk.Label(
            self.content_frame,
            text="",
            font=self.text_font,
            bg="#1a1a2e",
            fg="#ecf0f1",
            wraplength=640,
            justify="left"
        )
        self.text_lbl.pack(pady=(0, 15))

        self.btn_frame = tk.Frame(self.content_frame, bg="#1a1a2e")
        self.btn_frame.pack(pady=10)

        self._choice_var = tk.StringVar()
        self._current_widgets = []

        for i in range(1, 6):
            self.root.bind(str(i), lambda e, idx=i - 1: self._press_index(idx))

    def _on_close(self):
        # Handle window close button - confirm quit
        c = self.yes_no(
            "Quit Game", "Are you sure you want to leave the adventure?")
        if c:
            try:
                self.root.destroy()
            finally:
                sys.exit(0)

    def _clear_widgets(self):
        for w in self._current_widgets:
            w.destroy()
        self._current_widgets.clear()

    def _press_index(self, idx):
        if 0 <= idx < len(self._current_widgets):
            if isinstance(self._current_widgets[idx], tk.Button):
                self._current_widgets[idx].invoke()

    def update_hud(self, *, name, klass, hp, max_hp, xp):
        # Update HUD status bar with player name, class, health, and XP
        hp_color = "#2ecc71" if hp > max_hp * \
            0.5 else "#e74c3c" if hp <= max_hp * 0.3 else "#f39c12"
        self.hud.config(
            text=f"👤 {name or '-'}   |   🎭 {klass or '-'}   |   ❤️ {hp}/{max_hp}   |   ⭐ {xp} XP",
            fg=hp_color if hp <= max_hp * 0.5 else "#00d9ff"
        )

    def message(self, title, text):
        # Display a message dialog with OK button
        self.title_lbl.config(text=title)
        self.text_lbl.config(text=text)
        self._clear_widgets()

        btn = tk.Button(
            self.btn_frame,
            text="✓ OK",
            width=40,
            height=2,
            font=self.text_font,
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self._set_choice("__ok__")
        )
        btn.pack(pady=5)
        self._current_widgets.append(btn)

        self._choice_var.set("")
        self.root.update()
        self.root.wait_variable(self._choice_var)

    def choice(self, title, text, options):
        # Display choice dialog with colored option buttons
        self.title_lbl.config(text=title)
        self.text_lbl.config(text=text)
        self._clear_widgets()

        colors = ["#3498db", "#9b59b6", "#e67e22", "#16a085", "#c0392b"]

        for i, opt in enumerate(options):
            color = colors[i % len(colors)]
            label = f"{i + 1}. {opt}"

            btn = tk.Button(
                self.btn_frame,
                text=label,
                width=40,
                height=2,
                font=self.text_font,
                bg=color,
                fg="white",
                activebackground=self._darken_color(color),
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=lambda o=opt: self._set_choice(o)
            )
            btn.pack(pady=4)
            self._current_widgets.append(btn)

        self._choice_var.set("")
        self.root.update()
        self.root.wait_variable(self._choice_var)
        return self._choice_var.get()

    def ask_text(self, title, prompt, default=""):
        # Show text input field with confirm button
        self.title_lbl.config(text=title)
        self.text_lbl.config(text=prompt)
        self._clear_widgets()

        entry_frame = tk.Frame(self.btn_frame, bg="#1a1a2e")
        entry_frame.pack(pady=(5, 10))
        self._current_widgets.append(entry_frame)

        entry = tk.Entry(
            entry_frame,
            width=45,
            font=self.text_font,
            bg="#2c3e50",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=5
        )
        entry.insert(0, default or "")
        entry.pack(pady=5)

        out = {"val": ""}

        def ok():
            out["val"] = entry.get().strip()
            self._set_choice("__ok__")

        entry.bind("<Return>", lambda e: ok())

        btn = tk.Button(
            self.btn_frame,
            text="✓ Confirm",
            width=40,
            height=2,
            font=self.text_font,
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=ok
        )
        btn.pack(pady=5)
        self._current_widgets.append(btn)

        self._choice_var.set("")
        self.root.update()
        entry.focus_set()
        self.root.wait_variable(self._choice_var)
        return out["val"]

    def yes_no(self, title, text):
        # Show yes/no choice dialog
        c = self.choice(title, text, ["Yes", "No"])
        return c == "Yes"

    def _set_choice(self, value):
        self._choice_var.set(value)

    def _darken_color(self, color):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        darker = tuple(int(c * 0.8) for c in rgb)
        return '#' + ''.join(f'{c:02x}' for c in darker)


def ui_init():
    global _app
    if _app is None:
        _app = App()
    return _app


def ui_update_hud(name, klass, hp, max_hp, xp):
    ui_init().update_hud(name=name, klass=klass, hp=hp, max_hp=max_hp, xp=xp)


def alert(title, text):
    ui_init().message(title, text)


def ask_choice(title, question, options):
    # Show choice dialog and return selected option
    return ui_init().choice(title, question, options)


def ask_text(title, prompt, default=""):
    # Show text input dialog and return user input
    return ui_init().ask_text(title, prompt, default)


def welcome_popup():
    # Welcome popup with confirmation dialogs for starting game
    start = ui_init().yes_no(
        "🎮 Welcome to the Adventure!",
        "Embark on an epic journey filled with danger and treasure.\n\nAre you ready to begin your adventure?"
    )
    if start:
        return True

    again = ui_init().choice(
        "Not Ready?",
        "Are you sure you don't want to start?\nThe adventure awaits...",
        ["Start Adventure", "Quit Game"]
    )
    if again == "Start Adventure":
        return True

    last = ui_init().choice(
        "Final Chance",
        "This is your last chance! Epic battles and treasures are waiting.\n\nWhat will it be?",
        ["Fine, I'll Start!", "I'm Out"]
    )
    return last == "Fine, I'll Start!"
