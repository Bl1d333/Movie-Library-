import tkinter as tk
from tkinter import ttk, messagebox
from models import MovieLibrary

class MovieApp:
    def __init__(self, root: tk.Tk, library: MovieLibrary):
        self.root = root
        self.library = library
        self.root.title("Movie Library — Личная кинотека")
        self.root.geometry("820x600")
        self.root.resizable(True, True)

        self.title_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.rating_var = tk.StringVar()
        self.filter_genre_var = tk.StringVar()
        self.filter_year_var = tk.StringVar()

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # --- Ввод данных ---
        input_frame = ttk.LabelFrame(self.root, text="Добавить фильм", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(input_frame, textvariable=self.title_var, width=50).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(input_frame, textvariable=self.genre_var, width=50).grid(row=1, column=1, padx=5)

        ttk.Label(input_frame, text="Год выпуска:").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(input_frame, textvariable=self.year_var, width=20).grid(row=2, column=1, sticky="w", padx=5)

        ttk.Label(input_frame, text="Рейтинг (0–10):").grid(row=3, column=0, sticky="w", pady=3)
        ttk.Entry(input_frame, textvariable=self.rating_var, width=20).grid(row=3, column=1, sticky="w", padx=5)

        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Добавить фильм", command=self.add_movie).pack(side="left", padx=5)

        # --- Фильтрация ---
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky="w")
        self.genre_combo = ttk.Combobox(filter_frame, textvariable=self.filter_genre_var, state="readonly", width=20)
        self.genre_combo.grid(row=0, column=1, padx=5)
        self.genre_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        ttk.Label(filter_frame, text="По году:").grid(row=0, column=2, sticky="w", padx=(15, 0))
        ttk.Entry(filter_frame, textvariable=self.filter_year_var, width=10).grid(row=0, column=3, padx=5)
        self.filter_year_var.trace("w", lambda *a: self.refresh_table())

        ttk.Button(filter_frame, text="Сбросить", command=self.reset_filters).grid(row=0, column=4, padx=10)

        # --- Таблица ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")

        self.tree.column("title", width=300)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=70, anchor="center")
        self.tree.column("rating", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Удаление ---
        ttk.Button(self.root, text="Удалить выбранный фильм", command=self.delete_movie).pack(pady=5)

    def add_movie(self):
        try:
            self.library.add_movie(
                self.title_var.get(),
                self.genre_var.get(),
                self.year_var.get(),
                self.rating_var.get()
            )
            messagebox.showinfo("Успех", "Фильм добавлен!")
            self.title_var.set("")
            self.genre_var.set("")
            self.year_var.set("")
            self.rating_var.set("")
            self.update_genre_list()
            self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите фильм для удаления.")
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        # Ищем по точному совпадению всех полей
        for i, m in enumerate(self.library.movies):
            if (m.title == values[0] and m.genre == values[1] and
                str(m.year) == values[2] and str(m.rating) == values[3]):
                self.library.delete_movie(i)
                break
        self.update_genre_list()
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        genre = self.filter_genre_var.get()
        year = self.filter_year_var.get()
        movies = self.library.filter_movies(genre, year)
        for m in movies:
            self.tree.insert("", "end", values=(m.title, m.genre, m.year, m.rating))

    def update_genre_list(self):
        self.genre_combo["values"] = [""] + self.library.get_all_genres()

    def reset_filters(self):
        self.filter_genre_var.set("")
        self.filter_year_var.set("")
        self.refresh_table()
