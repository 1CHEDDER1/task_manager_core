import json
from pathlib import Path

file_path = Path("storage.json").resolve()
SEARCHABLE_FIELDS = ['name', 'number']

def load_data(file_path: Path):    
    try:
        raw_data = file_path.read_text(encoding="utf-8")
        data = json.loads(raw_data)
        
        if not isinstance(data, list): 
            return []
        
        valid_contacts = []
        for entry in data:
            if isinstance(entry, dict) and 'name' in entry and 'number' in entry:
                valid_contacts.append(entry)
        return valid_contacts

    except json.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []
   
def save_data(value_contacts: list, file_path: Path):
    try:
        json_str = json.dumps(value_contacts, ensure_ascii=False, indent=4)
        file_path.write_text(json_str, encoding="utf-8")
    except PermissionError:
        print("Ошибка: Нет прав на запись в этот файл.")

def list_contacts(value_contacts: list):
    if not value_contacts:
        print("Список контактов пуст.")
        return
    print(f"{'ID':<4} | {'Имя':<20} | {'Номер':<15}")
    print("-" * 45)
    for index, contact in enumerate(value_contacts):
        name = contact['name']
        number = contact['number']
        print(f"{index:<4} | {name:<20} | {number:<15}")

def add_contact(value_contacts: list, file_path: Path):
    name = input("Введите Имя: ").strip()
    number = input("Введите Номер: ").strip()

    if not name:
        print("Ошибка: Имя не может быть пустым!")
        return

    if not number or not number.isdigit():
        print("Ошибка: Номер обязателен и должен содержать только цифры!")
        return
    
    new_contact = {
        "name": name, 
        "number": number
    }

    value_contacts.append(new_contact)
    save_data(value_contacts, file_path)
    print("Контакт сохранен.")

def find_contacts(value_contacts: list, search_arg=None): 
    if not value_contacts:
        print("Телефонная книга пуста. Искать негде.")
        return
    
    if not search_arg:
        search_arg = input("Поиск: ").strip()
    
    search = search_arg.lower()
    if not search:
        print("Пустой запрос.")
        return

    results = [
        contact for contact in value_contacts 
        if any(search in str(contact[key]).lower() for key in SEARCHABLE_FIELDS)
    ]

    if results:
        print(f"\nНайдено совпадений: {len(results)}")
        list_contacts(results)
    else:
        print("Ничего не найдено.")

def delete_contacts(value_contacts: list, file_path: Path, target_arg=None):
    if target_arg is None:
        raw_input = input("Введите ID контакта для удаления: ")
    else:
        raw_input = target_arg
    
    try:
        index = int(raw_input)
        if index < 0 or index >= len(value_contacts):
            print("Ошибка: Неверный ID.")
            return
        
        removed = value_contacts.pop(index)
        save_data(value_contacts, file_path)
        print(f"Контакт '{removed['name']}' удален.")

    except ValueError:
        print("Ошибка: ID должен быть числом!")

def update_contacts(value_contacts: list, file_path: Path, update_arg=None):
    if update_arg is None:
        upd_input = input("Введите ID контакта для изменения: ")
    else:
        upd_input = update_arg
    
    try:
        index = int(upd_input)
        if index < 0 or index >= len(value_contacts):
            print("Ошибка: Неверный ID.")
            return
        
        contact = value_contacts[index]
        print(f"Редактируем: {contact['name']} | {contact['number']}")

        new_name = input("Новое имя (Enter чтобы оставить): ").strip()
        new_number = input("Новый номер (Enter чтобы оставить): ").strip()
        
        changed = False

        if new_name:
            contact['name'] = new_name
            changed = True
        
        if new_number:
            if not new_number.isdigit():
                print("Ошибка: Номер должен содержать только цифры! Изменение отменено.")
                return
            contact['number'] = new_number
            changed = True
        
        if changed:
            save_data(value_contacts, file_path)
            print("Контакт успешно обновлен.")
        else:
            print("Изменений нет.")

    except ValueError:
        print("Ошибка: ID должен быть числом!")

def main(value_contacts: list, file_path: Path):
    print("\n=== ТЕЛЕФОННАЯ КНИГА ===")
    print("Команды:\n"
          "  add           - добавить контакт\n"
          "  list          - список всех\n"
          "  find <text>   - поиск\n"
          "  delete <id>   - удалить по ID\n"
          "  update <id>   - изменить по ID\n"
          "  exit          - выход")
    print("===============================\n")

    while True:
        try:
            user_input = input("\n> ").strip().split(maxsplit=1)
        except (EOFError, KeyboardInterrupt):
            print("\nВыход...")
            break
        
        if not user_input: 
            continue
            
        command = user_input[0].lower()
        args = user_input[1] if len(user_input) > 1 else None

        if command == "add":
            add_contact(value_contacts, file_path)
        elif command == "list":
            list_contacts(value_contacts)
        elif command == "find":
            find_contacts(value_contacts, args)
        elif command == "delete":
            delete_contacts(value_contacts, file_path, args)
        elif command == "update":
            update_contacts(value_contacts, file_path, args)
        elif command == "exit":
            print("Пока!")
            break
        else:
            print("Неизвестная команда.")

if __name__ == "__main__":
    initial_contacts = load_data(file_path)
    main(initial_contacts, file_path)