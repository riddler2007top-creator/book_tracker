import tkinter as tk
from tkinter import ttk, messagebox
import json

FILENAME = "books.json"

def load_data():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    try:
        pages = int(pages)
        if pages <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Количество страниц должно быть положительным целым числом!")
        return

    book = {"title": title, "author": author, "genre": genre, "pages": pages}
    data.append(book)
    save_data(data)
    update_table()
    clear_inputs()

def update_table():
    for i in treeview.get_children():
        treeview.delete(i)
    for book in data:
        treeview.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

def filter_books():
    genre = entry_filter_genre.get().strip().lower()
    pages_str = entry_filter_pages.get().strip()
    
    try:
        min_pages = int(pages_str) if pages_str else None
    except ValueError:
        messagebox.showerror("Ошибка", "В фильтре по страницам должно быть число!")
        return

    for i in treeview.get_children():
        treeview.delete(i)
        
    for book in data:
        genre_match = not genre or genre in book["genre"].lower()
        pages_match = (min_pages is None) or (book["pages"] > min_pages)
        
        if genre_match and pages_match:
            treeview.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

def clear_inputs():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

# Загрузка данных при старте
data = load_data()

# Создание окна
root = tk.Tk()
root.title("Трекер прочитанных книг")
root.geometry("800x500")

# Вкладки: Добавление и Просмотр/Фильтр
tab_control = ttk.Notebook(root)
tab_add = ttk.Frame(tab_control)
tab_view = ttk.Frame(tab_control)
tab_control.add(tab_add, text="Добавить книгу")
tab_control.add(tab_view, text="Список и фильтр")
tab_control.pack(expand=1, fill="both")

# Вкладка "Добавить книгу"
tk.Label(tab_add, text="Название:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_title = tk.Entry(tab_add, width=35)
entry_title.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

tk.Label(tab_add, text="Автор:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_author = tk.Entry(tab_add, width=35)
entry_author.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

tk.Label(tab_add, text="Жанр:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_genre = tk.Entry(tab_add, width=35)
entry_genre.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

tk.Label(tab_add, text="Страниц:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_pages = tk.Entry(tab_add, width=10)
entry_pages.grid(row=3, column=1, padx=10, pady=5)

btn_add = tk.Button(tab_add, text="Добавить книгу", command=add_book)
btn_add.grid(row=3, column=2, padx=10)

# Вкладка "Список и фильтр"
tk.Label(tab_view, text="Фильтр по жанру:").grid(row=0, column=0, padx=10, pady=5)
entry_filter_genre = tk.Entry(tab_view, width=20)
entry_filter_genre.grid(row=0, column=1, padx=10)

tk.Label(tab_view, text="Фильтр по страницам (>):").grid(row=0, column=2, padx=10)
entry_filter_pages = tk.Entry(tab_view, width=10)
entry_filter_pages.grid(row=0, column=3)

btn_filter = tk.Button(tab_view, text="Применить фильтр", command=filter_books)
btn_filter.grid(row=0, column=4, padx=10)

# Таблица книг
treeview = ttk.Treeview(tab_view,
                        columns=("Название", "Автор", "Жанр", "Страниц"),
                        show="headings")
treeview.heading("Название", text="Название")
treeview.heading("Автор", text="Автор")
treeview.heading("Жанр", text="Жанр")
treeview.heading("Страниц", text="Страниц")
treeview.column("Название", width=250)
treeview.column("Автор", width=150)
treeview.column("Жанр", width=120)
treeview.column("Страниц", width=80)
treeview.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

# Заполнение таблицы при запуске
update_table()

root.mainloop()
