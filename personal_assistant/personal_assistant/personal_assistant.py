import json
import os
from datetime import datetime
import pandas as pd

NOTES_FILE = 'notes.json'
TASKS_FILE = 'tasks.json'

if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w') as f:
        json.dump([], f)

def main_menu():
    while True:
        print("Добро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            notes_menu()
        elif choice == '2':
            tasks_menu()
        elif choice == '3':
            break
        elif choice == '4':
            break
        elif choice == '5':
            break
        elif choice == '6':
            break
        else:
            print("Некорректный ввод, попробуйте снова.")

def notes_menu():
    while True:
        print("\n--- Меню управления заметками ---")
        print("1. Создать новую заметку")
        print("2. Просмотреть список заметок")
        print("3. Просмотреть подробности заметки")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Экспорт заметок в CSV")
        print("7. Импорт заметок из CSV")
        print("8. Назад")

        choice = input("Введите номер действия: ")

        if choice == '1':
            create_note()
        elif choice == '2':
            view_notes()
        elif choice == '3':
            view_note_details()
        elif choice == '4':
            edit_note()
        elif choice == '5':
            delete_note()
        elif choice == '6':
            export_notes_to_csv()
        elif choice == '7':
            import_notes_from_csv()
        elif choice == '8':
            break
        else:
            print("Некорректный ввод, попробуйте снова.")

def tasks_menu():
    while True:
        print("\n--- Меню управления задачами ---")
        print("1. Добавить новую задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Экспорт задач в CSV")
        print("7. Импорт задач из CSV")
        print("8. Назад")

        choice = input("Введите номер действия: ")

        if choice == '1':
            create_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            mark_task_as_done()
        elif choice == '4':
            edit_task()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            export_tasks_to_csv()
        elif choice == '7':
            import_tasks_from_csv()
        elif choice == '8':
            break
        else:
            print("Некорректный ввод, попробуйте снова.")

class Note:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def create_note():
    title = input("Введите заголовок заметки: ")
    content = input("Введите содержимое заметки: ")

    notes = load_notes()
    note_id = len(notes) + 1
    new_note = Note(note_id, title, content)

    notes.append(new_note.__dict__)
    save_notes(notes)
    print("Заметка успешно создана.")

def view_notes():
    notes = load_notes()
    if not notes:
        print("Нет доступных заметок.")
    else:
        for note in notes:
            print(f"{note['id']}: {note['title']} - {note['timestamp']}")

def view_note_details():
    note_id = int(input("Введите ID заметки для просмотра: "))
    notes = load_notes()
    for note in notes:
        if note['id'] == note_id:
            print(f"Заголовок: {note['title']}")
            print(f"Содержимое: {note['content']}")
            print(f"Дата создания: {note['timestamp']}")
            return
    print("Заметка не найдена.")

def edit_note():
    note_id = int(input("Введите ID заметки для редактирования: "))
    notes = load_notes()
    for note in notes:
        if note['id'] == note_id:
            new_title = input(f"Введите новый заголовок (текущий: {note['title']}): ")
            new_content = input(f"Введите новое содержимое (текущее: {note['content']}): ")
            note['title'] = new_title or note['title']
            note['content'] = new_content or note['content']
            note['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            save_notes(notes)
            print("Заметка успешно отредактирована.")
            return
    print("Заметка не найдена.")

def delete_note():
    note_id = int(input("Введите ID заметки для удаления: "))
    notes = load_notes()
    notes = [note for note in notes if note['id'] != note_id]
    save_notes(notes)
    print(f"Заметка с ID {note_id} успешно удалена.")

def export_notes_to_csv():
    notes = load_notes()
    df = pd.DataFrame(notes)
    df.to_csv('notes.csv', index=False)
    print("Заметки успешно экспортированы в notes.csv.")

def import_notes_from_csv():
    try:
        df = pd.read_csv('notes.csv')
        notes = load_notes()

        for _, row in df.iterrows():
            note_id = len(notes) + 1
            new_note = Note(note_id, row['title'], row['content'])
            notes.append(new_note.__dict__)

        save_notes(notes)
        print("Заметки успешно импортированы из notes.csv.")
    except FileNotFoundError:
        print("Файл notes.csv не найден.")

def load_notes():
    with open(NOTES_FILE, 'r') as f:
        return json.load(f)

def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=4)

class Task:
    def __init__(self, id, title, description, priority, due_date):
        self.id = id
        self.title = title
        self.description = description
        self.done = False
        self.priority = priority
        self.due_date = due_date

def create_task():
    title = input("Введите краткое описание задачи: ")
    description = input("Введите подробное описание задачи: ")
    priority = input("Введите приоритет задачи (Высокий/Средний/Низкий): ")
    due_date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")

    tasks = load_tasks()
    task_id = len(tasks) + 1
    new_task = Task(task_id, title, description, priority, due_date)

    tasks.append(new_task.__dict__)
    save_tasks(tasks)
    print("Задача успешно добавлена.")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Нет доступных задач.")
    else:
        for task in tasks:
            status = "Выполнена" if task['done'] else "Не выполнена"
            print(f"{task['id']}: {task['title']} - {status} (Приоритет: {task['priority']}, Срок: {task['due_date']})")

def mark_task_as_done():
    task_id = int(input("Введите ID задачи для отметки как выполненной: "))
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            task['done'] = True
            save_tasks(tasks)
            print(f"Задача с ID {task_id} отмечена как выполненная.")
            return
    print("Задача не найдена.")

def edit_task():
    task_id = int(input("Введите ID задачи для редактирования: "))
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            new_title = input(f"Введите новое название (текущее: {task['title']}): ")
            new_description = input(f"Введите новое описание (текущее: {task['description']}): ")
            new_priority = input(f"Введите новый приоритет (текущий: {task['priority']}): ")
            new_due_date = input(f"Введите новую дату выполнения (текущая: {task['due_date']}): ")

            task['title'] = new_title or task['title']
            task['description'] = new_description or task['description']
            task['priority'] = new_priority or task['priority']
            task['due_date'] = new_due_date or task['due_date']

            save_tasks(tasks)
            print(f"Задача с ID {task_id} успешно отредактирована.")
            return

    print("Задача не найдена.")

def delete_task():
    task_id = int(input("Введите ID задачи для удаления: "))
    tasks = load_tasks()

    tasks = [task for task in tasks if task['id'] != task_id]

    save_tasks(tasks)
    print(f"Задача с ID {task_id} успешно удалена.")

def export_tasks_to_csv():
    tasks = load_tasks()
    df = pd.DataFrame(tasks)
    df.to_csv('tasks.csv', index=False)
    print("Задачи успешно экспортированы в tasks.csv.")

def import_tasks_from_csv():
    try:
        df = pd.read_csv('tasks.csv')

        tasks = load_tasks()

        for _, row in df.iterrows():
            task_id = len(tasks) + 1
            new_task = Task(task_id, row['title'], row['description'], row['priority'], row['due_date'])
            tasks.append(new_task.__dict__)

        save_tasks(tasks)
        print("Задачи успешно импортированы из tasks.csv.")

    except FileNotFoundError:
        print("Файл tasks.csv не найден.")

def load_tasks():
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

if __name__ == "__main__":
    main_menu()