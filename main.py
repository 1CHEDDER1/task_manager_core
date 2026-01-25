class Task:
    STATUS_NEW = "New"
    STATUS_DONE = "Done"

    def __init__(self, title):
        self.title = title 
        self._status = self.STATUS_NEW

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название задачи не может быть пустым")
        self._title = value

    def complete(self):
        if self._status == self.STATUS_DONE:
            print(f"Спокойно, задача '{self._title}' уже была выполнена.")
            return
        self._status = self.STATUS_DONE
        print(f"Задача '{self._title}' успешно выполнена!")

    def __str__(self):
        return f"[{self._status}] {self._title}"

if __name__ == "__main__":
    try:
        t = Task("Работать")
        print(t) 
        
    except ValueError as e:
        print(f"Ошибка: {e}")