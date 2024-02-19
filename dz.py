import os
from datetime import datetime
DB_PATH = 'db.csv'

class Note:
    def __init__(self, id, dtime, header, txt):
        self.id = id
        self.dtime = dtime
        self.header = header
        self.txt = txt

    def header_preview(self, length):
        return self.header[:length] + '...' if len(self.header) > length else self.header.ljust(length + 3)

    def txt_preview(self, length):
        preview = self.txt[:length] + '...' if len(self.txt) > length else self.txt.ljust(length + 3)
        return preview.replace("\n", " ").replace("\r", "").replace("\t", " ")

def read_file():
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                arr = line.replace('\\n', '\n').split(';')
                notes.append(Note(arr[0], arr[1], arr[2], arr[3]))
    except:
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            f.write(" ")

def save_file():
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        for note in notes:
            print(note.id + ';' + \
                note.dtime + ';' + \
                note.header + ';' + \
                note.txt.replace('\n', '\\n') + ';', file=f)

def sort_notes(type, reverse=False):
    if type == 'by_id':
        return sorted(notes, key=lambda note: note.id, reverse=reverse)
    elif type == 'by_date':
        return sorted(notes, key=lambda note: datetime.strptime(note.dtime, "%d.%m.%y %H:%M:%S"), reverse=reverse)

def find_by_str(str):
    result = []
    for note in notes:
        if str.lower() in note.header.lower() or str.lower() in note.txt.lower():
            result.append(note)
    return result

def find_by_date(start_date, end_date):
    result = []
    for note in notes:
        if datetime.strptime(start_date, "%d.%m.%y %H:%M:%S") < datetime.strptime(note.dtime, "%d.%m.%y %H:%M:%S") < datetime.strptime(end_date, "%d.%m.%y %H:%M:%S"):
            result.append(note)
    return result

def next_id():
    id = 1
    while True:
        is_free = True
        for note in notes:
            if int(note.id) == id:
                is_free = False
                break
        if is_free: return id
        id += 1

def print_notes(notes):
    os.system('cls')
    print(grey('0. Назад...'))
    for i, note in enumerate(notes):
        print(grey(f'{i + 1}. ') + f'#{note.id} {note.dtime} {note.header_preview(40)} {note.txt_preview(80)}')

def edit_note(note):
    os.system('cls')
    print(grey('Старый заголовок: ') + f'{note.header}')
    note.header = input(grey('Новый заголовок: '))
    print(grey('Старый текст:\n') + f'{note.txt}')
    note.txt = multi_input(grey('Новый текст (Ctrl-Z для завершения ввода): '))
    note.dtime = datetime.now().strftime('%d.%m.%y %H:%M:%S')

def new_note():
    os.system('cls')
    id = str(next_id()).zfill(3)
    header = input(grey('Заголовок: '))
    txt = multi_input(grey('Текст (Ctrl-Z для завершения ввода): '))
    dtime = datetime.now().strftime('%d.%m.%y %H:%M:%S')
    notes.append(Note(id, dtime, header, txt))

def grey(str):
    ANSI_RESET = '\u001B[0m'
    ANSI_GREY = '\u001b[30;1m'
    return ANSI_GREY + str + ANSI_RESET

def multi_input(str):
    print(str)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        lines.append(line)
    return '\n'.join(lines)

# Основное меню
def main_menu():
    MENU_TXT = \
        '1. Вывести заметки \n' + \
        '   1.1 Новые вначале \n' + \
        '   1.2 Старые вначале \n' + \
        '2 Поиск \n' + \
        '   2.1 По тексту \n' + \
        '   2.2 По дате \n' + \
        '3. Новая заметка \n' + \
        '0. Выход \n' + \
        'Выберите пункт меню: '

    while True:
        os.system('cls')
        input_num = input(grey(MENU_TXT))
        if input_num == '1.1':  # Вывести сначала новые
            sorted_notes=sort_notes('by_date', reverse=True) 
            print_notes(sorted_notes)
            i = int(input(grey('Выберите заметку: ')))
            if 0 < i <= len(sorted_notes):
                note_menu(sorted_notes[i - 1])
        elif input_num == '1.2':  # Вывести сначала старые
            sorted_notes=sort_notes('by_date') 
            print_notes(sorted_notes)
            i = int(input(grey('Выберите заметку: ')))
            if 0 < i <= len(sorted_notes):
                note_menu(sorted_notes[i - 1])
        elif input_num == '2.1':  # Найти по тексту
            os.system('cls')
            str = input(grey('Строка для поиска: '))
            finded_notes=find_by_str(str) 
            print_notes(finded_notes)
            i = int(input(grey('Выберите заметку: ')))
            if 0 < i <= len(finded_notes):
                note_menu(finded_notes[i - 1])
        elif input_num == '2.2':  # Найти по дате
            os.system('cls')
            start_date = input(grey('Дата начала интервала (дд.мм.гг чч:мм:сс): '))
            end_date = input(grey('Дата окончания интервала (дд.мм.гг чч:мм:сс): '))
            finded_notes=find_by_date(start_date, end_date) 
            print_notes(finded_notes)
            i = int(input(grey('Выберите заметку: ')))
            if 0 < i <= len(finded_notes):
                note_menu(finded_notes[i - 1])
        elif input_num == '3':  # Новая заметка
            new_note()
            save_file()
        elif input_num == '0':  # Назад
            break    
        # input('Нажмите Enter для продолжения...')

# Меню заметки
def note_menu(note):
    MENU_TXT = \
        '1. Редактировать \n' + \
        '2. Удалить \n' + \
        '0. Назад \n' + \
        'Выберите пункт меню: '

    while True:
        os.system('cls')
        print(grey('ID: ') + f'#{note.id}\n' + \
            grey('Дата: ') + f'{note.dtime}\n' + \
            grey('Заголовок ') + f'{note.header}\n' + \
            grey('Текст: ') + f'{note.txt}')
        input_num = input(grey(MENU_TXT))
        if input_num == '1':  # Редактировать
            edit_note(note)
            save_file()
            break
        elif input_num == '2':  # Удалить
            notes.remove(note)
            save_file()
            break
        elif input_num == '0':  # Назад
            break
notes = []

if __name__ == "__main__":
    read_file() 
    main_menu()
