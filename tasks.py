import tkinter as tk
from datetime import datetime
import json
import shutil
import sys


# Определение функций
def add_task(event=None):
    task = task_entry.get()  # Получаем текст из поля ввода
    if task:
        task_count = task_listBox.size()
        task_listBox.insert(tk.END,
                            f"{task_count + 1}. {task} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")  # Вставляем текст в конец списка с датой и временем
        task_entry.delete(0, tk.END)  # Очищаем поле ввода
        save_tasks()  # Сохраняем текущие задачи


def mark_task():
    selected_task = task_listBox.curselection()
    if selected_task:
        # Получаем текст выбранной задачи
        task = task_listBox.get(selected_task[0])

        # Добавляем зачеркивающий символ перед каждым символом строки
        striked_task = ''.join([char + '\u0336' for char in task])

        # Обновляем текст в списке
        task_listBox.delete(selected_task[0])  # Удаляем старую строку
        task_listBox.insert(selected_task[0], striked_task)  # Вставляем новую строку с зачеркиванием


def delete_task():
    selected_task = task_listBox.curselection()  # Получаем индекс выбранного элемента
    if selected_task:
        task_listBox.delete(selected_task)  # Удаляем выбранный элемент


def edit_task():
    selected_task = task_listBox.curselection()
    if selected_task:
        top = tk.Toplevel(win)
        top.title("Редактировать задачу")
        top.geometry("400x200")

        old_task = task_listBox.get(selected_task[0]).split('|')[0].strip()
        new_task_entry = tk.Entry(top, width=40)
        new_task_entry.insert(0, old_task)
        new_task_entry.grid(row=0, column=0, pady=10)

        def update_task():
            updated_task = new_task_entry.get()
            if updated_task:
                task_listBox.delete(selected_task[0])
                task_listBox.insert(selected_task[0],
                                    f"{updated_task.strip()} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                save_tasks()
                top.destroy()

        update_button = tk.Button(top, text="Обновить задачу", command=update_task)
        update_button.grid(row=1, column=0, pady=10)


def filter_completed_tasks():
    filtered_tasks = []
    for i in range(task_listBox.size()):
        task = task_listBox.get(i)
        if not any(char == '\u0336' for char in task):
            filtered_tasks.append(task)

    task_listBox.delete(0, tk.END)
    for task in filtered_tasks:
        task_listBox.insert(tk.END, task)


#def backup_data():
    #now = datetime.now().strftime("%Y%m%d_%H%M%S")
    #backup_file = f'tasks_backup_{now}.json'
    #shutil.copyfile('tasks.json', backup_file)


def show_all_tasks():
    try:
        with open('tasks.json', 'r') as file:
            saved_tasks = json.load(file)

            task_listBox.delete(0, tk.END)  # Очистим текущий список
            for task in saved_tasks:
                task_listBox.insert(tk.END, task)  # Восстановим все задачи
    except FileNotFoundError:
        pass  # Файл отсутствует, ничего не делаем


def on_closing():
    save_tasks()  # Сохраняем задачи перед закрытием
    win.destroy()  # Закрываем окно
    sys.exit(0)  # Завершаем программу


# Функция сохранения задач
def save_tasks():
    tasks = []
    for i in range(task_listBox.size()):
        tasks.append(task_listBox.get(i))

    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)


# Инициализация главного окна
win = tk.Tk()
win.title("Менеджер задач")
win.configure(background="black")
win.geometry("1200x600+350+250")  # Увеличили размер окна для лучшего размещения элементов

# Создание виджетов
task_text = tk.Label(win, text="Введите Вашу задачу:",
                     font=("Times New Roman", 20, "bold"),
                     fg="chartreuse",
                     bg="black")
task_text.grid(row=0, column=0, padx=(30, 0), pady=10)

task_entry = tk.Entry(win,
                      width=37,
                      font=("Times New Roman", 14, "italic"),
                      fg="chartreuse",
                      bg="black",
                      justify="center",
                      highlightbackground="chartreuse",
                      highlightthickness=2)
task_entry.grid(row=1, column=0, padx=(30, 0), pady=(0, 10))
task_entry.bind('<Return>', add_task)  # Связывание нажатия Enter с функцией добавления задачи

mark_button = tk.Button(win, text="Задача выполнена",
                        width=25,
                        font=("Times New Roman", 20),
                        fg="yellow",
                        highlightbackground="yellow",
                        bg="black",
                        command=mark_task)
mark_button.grid(row=2, column=0, sticky='W', padx=(30, 0))

edit_button = tk.Button(win, text="Редактировать задачу",
                        width=25,
                        font=("Times New Roman", 20),
                        fg="blue",
                        highlightbackground="blue",
                        bg="black",
                        command=edit_task)
edit_button.grid(row=3, column=0, sticky='W', padx=(30, 0))

filter_button = tk.Button(win, text="Скрыть выполненные задачи",
                          width=25,
                          font=("Times New Roman", 20),
                          fg="green",
                          highlightbackground="green",
                          bg="black",
                          command=filter_completed_tasks)
filter_button.grid(row=4, column=0, sticky='W', padx=(30, 0))

show_all_button = tk.Button(win, text="Показать все задачи",
                            width=25,
                            font=("Times New Roman", 20),
                            fg="cyan",
                            highlightbackground="cyan",
                            bg="black",
                            command=show_all_tasks)
show_all_button.grid(row=5, column=0, sticky='W', padx=(30, 0))

delete_button = tk.Button(win, text="Удалить задачу",
                          width=25,
                          font=("Times New Roman", 20),
                          fg="red3",
                          highlightbackground="chartreuse",
                          bg="black",
                          command=delete_task)
delete_button.grid(row=6, column=0, sticky='W', padx=(30, 0))

#backup_button = tk.Button(win, text="Создать резервную копию",
                          #width=25,
                          #font=("Times New Roman", 20),
                          #fg="orange",
                          #highlightbackground="orange",
                          #bg="black",
                          #command=backup_data)
#backup_button.grid(row=7, column=0, sticky='W', padx=(30, 0))

task_label1 = tk.Label(win, text="ВАШ СПИСОК ЗАДАЧ",
                       font=("Times New Roman", 20, "bold italic"),
                       fg="yellow",
                       bg="black")
task_label1.grid(row=0, column=1, padx=(160, 0), pady=10)

task_listBox = tk.Listbox(win,
                          height=24,
                          width=65,
                          font=("Times New Roman", 14),
                          fg="yellow",
                          highlightbackground="yellow",
                          highlightthickness=2,
                          bg="black")
task_listBox.grid(row=1, column=1, rowspan=7, padx=(160, 0))

# Привязываем событие закрытия окна
win.protocol("WM_DELETE_WINDOW", on_closing)

# Загрузка задач из файла
try:
    with open('tasks.json', 'r') as file:
        saved_tasks = json.load(file)

        for task in saved_tasks:
            task_listBox.insert(tk.END, task)
except FileNotFoundError:
    pass  # Файл отсутствует, ничего не делаем

# Запуск главного цикла обработки событий
win.mainloop()