from abc import abstractmethod


# абстрактный класс Storage
class Storage:
    @abstractmethod
    def add(self, name, count):
        """ Метод увеличивает запас items"""
        pass

    @abstractmethod
    def remove(self, name, count):
        """ Метод увеличивает запас items"""
        pass

    @abstractmethod
    def get_free_space(self):
        """ Метод возвращает количество свободных мест"""
        pass

    @abstractmethod
    def get_items(self):
        """ Метод возвращает сожержание склада в словаре {товар: количество}"""
        pass

    @abstractmethod
    def get_unique_items_count(self):
        """ Метод возвращает количество уникальных товаров"""
        pass


class Store(Storage):
    def __init__(self):
        self.items = {}  # словарь название:количество
        self.capacity = 100  # по умолчанию равно 100

    def add(self, name, count):
        """ Метод увеличивает запас items с учетом лимита capacity"""
        is_found = False
        for key in self.items.keys():
            if name == key:
                self.items[key] = self.items[key] + count
                is_found = True
        if not is_found:
            self.items[name] = count
        print(f"Добавлен товар: {name} - {count} ед.")


    def remove(self, name, count):
        """ Метод уменьшает запас items, но не ниже 0"""
        for key in self.items.keys():
            if name == key:
                if self.items[key] - count >= 0:
                    self.items[key] = self.items[key] - count
                else:
                    shortage = count - self.items[key]
                    print(f"На складе хватает товара {name} на {shortage} едениц")
            else:
                print(f"{name.title()} - нет на складе")

    def get_free_space(self):
        """ Метод возвращает количество свободных мест"""
        return self.capacity - sum(self.items.values())

    def get_items(self):
        """Метод возвращает сожержание склада в словаре {товар: количество}"""
        return self.items

    def get_unique_items_count(self):
        """ Метод возвращает количество уникальных товаров"""
        return len(self.items.keys())


class Shop(Store):
    def __init__(self):
        super().__init__()
        self.capacity = 30
        self._limit = 5
        self.items = {}

    @property
    def get_item_limit(self):
        return self._limit

    def add(self, name, count):
        """ Метод увеличивает запас items с учетом лимита capacity,
        Shop не может быть наполнен,
        если свободное место закончилось или в нем уже есть 5 разных товаров"""
        if self.get_unique_items_count() < self._limit:
            super().add(name, count)
        else:
            print(f"Товар не может быть добавлен")


class Request:
    def __init__(self, str):
        lst = self.get_info(str)

        self.from_ = lst[4]  # откуда везем
        self.amount = int(lst[1])  # количество товара
        self.product = lst[2]  # товар
        self.to = lst[6]  # куда везем

    def get_info(self, str):
        return str.split(" ")

    def __repr__(self):
        return f'**Доставить** {self.amount} {self.product} **из** {self.from_} **в** {self.to}'
