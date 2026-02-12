import os
from abc import ABC, abstractmethod


class Person(ABC):
    """Абстрактный класс человека"""
    def __init__(self, name):
        self._name = name 

    @property
    def name(self):
        return self._name

    @abstractmethod
    def get_info(self):
        """Абстрактный метод для полиморфизма"""
        pass


class Librarian(Person):
    """Класс Библиотекарь (Наследование)"""
    def get_info(self):
       
        return f"Сотрудник библиотеки: {self.name}"


class User(Person):
    """Класс Пользователь (Наследование)"""
    def __init__(self, name):
        super().__init__(name)
    
        self.__borrowed_books = []

    def get_info(self):
        
        books_str = ", ".join(self.__borrowed_books) if self.__borrowed_books else "нет книг"
        return f"Читатель: {self.name} | Взятые книги: [{books_str}]"

    def get_borrowed_books(self):
        return self.__borrowed_books

    def add_book_to_list(self, title):
        self.__borrowed_books.append(title)

    def remove_book_from_list(self, title):
        if title in self.__borrowed_books:
            self.__borrowed_books.remove(title)



class Book:
    def __init__(self, title, author, status="Доступна"):
        self.title = title
        self.author = author
        self.status = status

    def __str__(self):
        return f"'{self.title}' ({self.author}) — Статус: {self.status}"


class LibraryManager:
    def __init__(self):
        self.books = []
        self.users = []
        self.books_file = "books.txt"
        self.users_file = "users.txt"
        self.load_data()

    def load_data(self):
        """Загрузка данных из файлов"""
    
        if os.path.exists(self.books_file):
            with open(self.books_file, "r", encoding="utf-8") as f:
                for line in f:
                    t, a, s = line.strip().split("|")
                    self.books.append(Book(t, a, s))

        
        if os.path.exists(self.users_file):
            with open(self.users_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    u_name = parts[0]
                    u_books = parts[1].split(",") if parts[1] else []
                    new_user = User(u_name)
                    for b in u_books:
                        new_user.add_book_to_list(b)
                    self.users.append(new_user)

    def save_data(self):
        """Сохранение данных в файлы"""
     
        with open(self.books_file, "w", encoding="utf-8") as f:
            for b in self.books:
                f.write(f"{b.title}|{b.author}|{b.status}\n")
        
        with open(self.users_file, "w", encoding="utf-8") as f:
            for u in self.users:
                books_str = ",".join(u.get_borrowed_books())
                f.write(f"{u.name}|{books_str}\n")

    def find_book(self, title):
        for b in self.books:
            if b.title.lower() == title.lower():
                return b
        return None

    def find_user(self, name):
        for u in self.users:
            if u.name.lower() == name.lower():
                return u
        return None

def run():
    manager = LibraryManager()
    
    print("--- ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ БИБЛИОТЕКИ ---")
    print("1. Библиотекарь")
    print("2. Читатель (Пользователь)")
    role = input("Выберите роль (1/2): ")

    if role == "1":
       
        lib_name = input("Введите ваше имя: ")
        librarian = Librarian(lib_name)
        print(f"\nАвторизован: {librarian.get_info()}")

        while True:
            print("\nМеню Библиотекаря:")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Зарегистрировать пользователя")
            print("4. Список всех пользователей")
            print("5. Список всех книг")
            print("0. Выход")
            
            cmd = input("-> ")
            if cmd == "1":
                t = input("Название: ")
                a = input("Автор: ")
                manager.books.append(Book(t, a))
                print("Книга добавлена.")
            elif cmd == "2":
                t = input("Введите название книги для удаления: ")
                book = manager.find_book(t)
                if book:
                    manager.books.remove(book)
                    print("Книга удалена.")
                else: print("Книга не найдена.")
            elif cmd == "3":
                n = input("Имя нового пользователя: ")
                if not manager.find_user(n):
                    manager.users.append(User(n))
                    print("Пользователь зарегистрирован.")
                else: print("Такой пользователь уже есть.")
            elif cmd == "4":
                print("\nСписок читателей:")
                for u in manager.users:
                    print(u.get_info())
            elif cmd == "5":
                print("\nИнвентарь книг:")
                for b in manager.books:
                    print(b)
            elif cmd == "0":
                break

    elif role == "2":
        
        u_name = input("Введите ваше имя: ")
        current_user = manager.find_user(u_name)

        if not current_user:
            print("Пользователь не найден. Обратитесь к библиотекарю для регистрации.")
        else:
            print(f"\nПриветствуем, {current_user.name}!")
            while True:
                print("\nМеню Пользователя:")
                print("1. Просмотреть доступные книги")
                print("2. Взять книгу")
                print("3. Вернуть книгу")
                print("4. Мои книги")
                print("0. Выход")
                
                cmd = input("-> ")
                if cmd == "1":
                    available = [b for b in manager.books if b.status == "Доступна"]
                    if not available: print("Сейчас нет доступных книг.")
                    for b in available: print(b)
                elif cmd == "2":
                    t = input("Какую книгу хотите взять? ")
                    book = manager.find_book(t)
                    if book:
                        if book.status == "Доступна":
                            book.status = "Выдана"
                            current_user.add_book_to_list(book.title)
                            print(f"Вы успешно взяли '{book.title}'")
                        else:
                            print("Увы, книга уже выдана другому читателю.")
                    else: print("Книги с таким названием нет.")
                elif cmd == "3":
                    t = input("Введите название возвращаемой книги: ")
                    if t in current_user.get_borrowed_books():
                        book = manager.find_book(t)
                        if book:
                            book.status = "Доступна"
                            current_user.remove_book_from_list(t)
                            print("Книга успешно возвращена.")
                    else: print("У вас нет этой книги.")
                elif cmd == "4":
                    print(current_user.get_info())
                elif cmd == "0":
                    break

    manager.save_data()
    print("Данные успешно сохранены. До свидания!")

if __name__ == "__main__":
    run()