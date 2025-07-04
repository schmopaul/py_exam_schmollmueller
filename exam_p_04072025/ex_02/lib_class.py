from abc import ABC, abstractmethod
import copy

class Item(ABC):
    def __init__(self,id:int,title:str):
        self.id = id
        self.title = title

    @abstractmethod
    def get_info(self) -> str:
        pass

class Book(Item):
    def __init__(self,id:int,title:str, author:str, pages:int, isbn:str):
        super().__init__(id,title)
        self.author = author
        self.pages = pages
        self.isbn = isbn
    
    def get_info(self) -> str:
        return f"Title: {self.title}, Author: {self.author}, Pages: {self.pages}"
    
    @staticmethod
    def is_valid_isbn(isbn:str) -> bool:
        return (len(isbn) == 10 or len(isbn) == 13) and isbn.isdigit()
    
    @classmethod
    def from_dict(cls, data:dict) -> 'Book':
        return cls(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            pages=data["pages"],
            isbn=data["isbn"]
        )
    
class Magazin(Item):
    def __init__(self, id:int, title:str, issue:int, month:str):
        super().__init__(id, title)
        self.issue = issue
        self.month = month

    def get_info(self) ->str:
        return f"Title: {self.title}, Issue: {self.issue}, Month: {self.month}"

    @classmethod
    def from_dict(cls, data:dict) -> 'Magazin':
        return cls(
            id=data["id"],
            title=data["title"],
            issue=data["issue"],
            month=data["month"]
        )
    

class Library():
    def __init__(self):
        self.items: list[Item] = []
    
    def add_item(self, Item:Item) -> None:
        self.items.append(Item)

    def remove_item(self, id:int) -> bool:
        for i, item in enumerate(self.items):
            if item.id == id:
                del self.items[i]
                return True
        return False
        
    def find_by_title(self, keyword: str) -> list[Item]:
        result = []
        for item in self.items:
            if keyword.lower() in item.title.lower():
                result.append(item)
        return result

    def list_by_type(self, cls: type[Item]) -> list[Item]:
        result = []
        for item in self.items:
            if isinstance(item, cls):
                result.append(item)
        return result

    
    def shallow_clone(self) -> 'Library':
        new_library = Library()
        new_library.items = self.items
        return new_library
    
    def deep_clone(self) -> 'Library':
        new_library = Library()
        new_library.items = copy.deepcopy(self.items)
        return new_library
    

if __name__ == "__main__":
    book_data1 = {
        "id": 1,
        "title": "Book1",
        "author": "Max Mustermann",
        "pages": 250,
        "isbn": "1234567890"
    }

    book_data2 = {
        "id": 2,
        "title": "Book2",
        "author": "Max Musterfrau",
        "pages": 400,
        "isbn": "9876543210"
    }

    mag_data1 = {
        "id": 3,
        "title": "Magazin1",
        "issue": 45,
        "month": "May"
    }

    mag_data2 = {
        "id": 4,
        "title": "Magazin2",
        "issue": 12,
        "month": "June"
    }

    book1 = Book.from_dict(book_data1)
    book2 = Book.from_dict(book_data2)
    mag1 = Magazin.from_dict(mag_data1)
    mag2 = Magazin.from_dict(mag_data2)

    lib = Library()
    lib.add_item(book1)
    lib.add_item(book2)
    lib.add_item(mag1)
    lib.add_item(mag2)

    print("All Items in Library:")
    for item in lib.items:
        print(item.get_info())

    keyword = "Book1"
    found = lib.find_by_title(keyword)
    print(f"\n Searching for Title with keyword: '{keyword}':")
    for item in found:
        print(item.get_info())

    print("\nAll Books in Library:")
    books = lib.list_by_type(Book)
    for b in books:
        print(b.get_info())

    shallow = lib.shallow_clone()
    print("\nShallow Clone created.")

    deep = lib.deep_clone()
    print("Deep Clone created.")

    shallow.items[0].title = "Shallow Clone Title Changed"
    print("\nAfter Change of Shallow Clone:")
    print(f"Original Library Item 0 Title: {lib.items[0].title}")
    print(f"Shallow Clone Item 0 Title:{shallow.items[0].title}")

    # Reset Title of lib -> not needed but just for clarity
    lib.items[0].title = "Old Title"
    
    deep.items[0].title = "Deep Clone Title Changed"
    print("\nAfter Change of Deep Clone:")
    print(f"Original Library Item 0 Title:{ lib.items[0].title}")
    print(f"Deep Clone Item 0 Title: {deep.items[0].title}")
