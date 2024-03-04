import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


# окно создания новой заметки
def create():
    global title_entry, body_entry, windowCreate
    windowCreate = tk.Tk()
    windowCreate.geometry("400x400")
    title_label = tk.Label(windowCreate, font=15, text="Заголовок заметки:")
    title_label.pack()
    title_entry = tk.Entry(windowCreate, font=15)
    title_entry.pack()
    body_label = tk.Label(windowCreate, font=15, text="Текст заметки:")
    body_label.pack()
    body_entry = tk.Entry(windowCreate, font=15)
    body_entry.pack()
    create_button2 = tk.Button(
        windowCreate, font=50, text="Создать заметку", command=create_note
    )
    create_button2.place(x=100, y=150, width=200, height=50)


# Функция создания заметки
def create_note():
    notes = load_notes()
    new_note = {}
    new_note["id"] = len(notes) + 1
    new_note["title"] = title_entry.get()
    new_note["body"] = body_entry.get()
    new_note["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notes.append(new_note)
    save_notes(notes)
    messagebox.showinfo("Создание заметки", "Заметка успешно создана!")
    windowCreate.destroy()


# окно удаления заметки
def delete():
    global windowDelete, del_entry
    windowDelete = tk.Tk()
    windowDelete.geometry("300x200")
    del_label = tk.Label(windowDelete, text="Введите id заметки для удаления")
    del_label.pack()
    del_entry = tk.Entry(windowDelete)
    del_entry.pack(padx=10, pady=20)
    del_button2 = tk.Button(
        windowDelete,
        text = "Удалить заметку",
        command = delete_note
    )
    del_button2.pack(padx=10, pady=10)


# Функция для удаления заметки
def delete_note():
    notes = load_notes()
    note_id = del_entry.get()
    new_note = []

    for note in notes:
        new_note.append(note["id"])

    if int(note_id) not in new_note:
        messagebox.showerror("Ошибка", "Заметка с таким id не найдена")
        
    for note in notes:
        if note["id"] == int(note_id):
            notes.remove(note)    
            messagebox.showinfo("Удаление заметки", "Заметка успешно удалена!")
    
    for note in notes:
        if note['id'] > int(note_id):
            note['id'] = note['id'] - 1
    
    save_notes(notes)  
    windowDelete.destroy()
    
# Функция для загрузки списка заметок
def load_notes():
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as file:
            notes = json.load(file)
        return notes
    else:
        return []


# Функция для сохранения списка заметок
def save_notes(notess):
    with open("notes.json", "w") as file:
        json.dump(notess, file, indent=4)


# Функция для вывода списка всех заметок
def list_notes():
    notes = load_notes()
    if not notes:
        messagebox.showinfo("Список заметок", "Заметок нет.")
    else:
        new_window = tk.Tk()
        new_window.title("Список заметок")
        new_window.geometry("800x600")
        for note in notes:
            label = tk.Label(
                new_window,
                font=8,
                text=f"{note['id']}. {note['title']}({note['date']}) : \n{note['body']}",
            )
            label.pack()
        new_window.mainloop()
# окно для поиска заметки
def edit():
    global windowEdit, edit_entry
    windowEdit = tk.Tk()
    windowEdit.geometry("300x200")
    edit_label = tk.Label(windowEdit, text="Введите id заметки для изменения")
    edit_label.pack()
    edit_entry = tk.Entry(windowEdit)
    edit_entry.pack(padx=10, pady=20)
    edit_button2 = tk.Button(
        windowEdit,
        text = "Изменить",
        command = edit_window
    )
    edit_button2.pack(padx=10, pady=10)

# окно для редактирования заметки    
def edit_window():
    global new_window, edit_title, edit_body
    notes = load_notes()
    note_id = edit_entry.get()
    new_note = []

    for note in notes:
        new_note.append(note["id"])

    if int(note_id) not in new_note:
        messagebox.showerror("Ошибка", "Заметка с таким id не найдена")
        windowEdit.destroy()
    else:
        new_window = tk.Tk()
        new_window.geometry("400x400")
        new_window.title("Изменение заметки")
        title_label = tk.Label(new_window, font=15, text="Заголовок заметки:")
        title_label.pack()
        edit_title = tk.Entry(new_window, font=15)
        edit_title.pack()
        body_label = tk.Label(new_window, font=15, text="Текст заметки:")
        body_label.pack()
        edit_body = tk.Entry(new_window, font=15)
        edit_body.pack()
        edit_button2 = tk.Button(new_window, text = "Изменить заметку", command = edit_note)
        edit_button2.pack(padx=10, pady=10)
    

# Функция для редактирования заметки
def edit_note():
    notes = load_notes()
    note_id = edit_entry.get()
    for note in notes:
        if note["id"] == int(note_id):
            note["title"] = edit_title.get()
            note["body"] = edit_body.get()
            note["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes(notes)

    messagebox.showinfo("Редактирование заметки", "Заметка успешно отредактирована!")
    windowEdit.destroy()
    new_window.destroy()



root = tk.Tk()
root.title("Заметки")
root.geometry("300x500")

create_button = tk.Button(root, text="Создать заметку", command=create)
create_button.place(x=50, y=100, width=200, height=50)

list_button = tk.Button(root, text="Список заметок", command=list_notes)
list_button.place(x=50, y=170, width=200, height=50)

delete_button = tk.Button(root, text="Удалить заметку", command=delete)
delete_button.place(x=50, y=240, width=200, height=50)

edit_button = tk.Button(root, text="Изменить заметку", command=edit)
edit_button.place(x=50, y=310, width=200, height=50)

root.mainloop()
