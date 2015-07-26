from book import Notebook
from tag import TagManager

class Yant:
    def __init__(self, note_class):
        self.tag_manager = TagManager()
        self.note_class = note_class

    def use_book(self, book):
        self.books = {book:Notebook(book, self.note_class)}       

    def use_tag(self, tag):
        books = self.tag_manager.get_books(tag)
        self.books = {b:Notebook(b, self.note_class) for b in books}       

    def get_books_by_tag(self, tag):
        return self.tag_manager.get_books(tag)

    def get_book_obj(self, book):
        return self.books[book]           
