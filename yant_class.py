import random

from entry import Entry
from book import Notebook
from tag import TagManager
from colors import colors
colored = colors.colored

class Yant:
    def __init__(self, note_class):
        self.tag_manager = TagManager()
        self.note_class = note_class

    # create book object and apply tags
    def create_book(self, book, tag="", description="No description"):
        new_book_obj = Notebook(book, self.note_class)
        new_book_obj.create_book(tag, description)
        self.tag_manager.tag_book("all", book)
        if tag != "" and tag!= "all":
            self.tag_manager.tag_book(tag, book)

    def use_book(self, book):
        self.books = {book: Notebook(book, self.note_class)}       

    def use_tag(self, tag):
        books = self.tag_manager.get_books(tag)
        self.books = {b : Notebook(b, self.note_class) for b in books}       

    def add_note(self, book, note_title):
        self.use_book(book)
        note_obj = Entry(note_title, ask_user_input=True)
        self.books[book].add_note(note_obj)

    def add_tag(self, book, tag):
        self.use_book(book)
        self.books[book].add_tag(tag)
        self.tag_manager.tag_book(tag, book)

    def update_note(self, book, note_title):
        self.use_book(book)
        self.books[book].update_note(note_title)

    def delete_note(self, book, note_title):
        self.use_book(book)
        self.books[book].delete_note(note_title)

    def delete_tag(self, book, tag):
        self.use_book(book)
        self.books[book].delete_tag(tag)
        self.tag_manager.untag_book(tag, book)

    def get_books_by_tag(self, tag):
        return self.tag_manager.get_books(tag)

    def get_book_obj(self, book):
        return self.books[book]    

    def import_book(self, book, source):
        self.use_book(book)
        self.books[book].import_book(source)

    def export_book(self, book, source):
        self.use_book(book)
        self.books[book].export_book(source)

    def prepare_books(self, target, category):
        if category == "tag":
            self.use_tag(target)
        elif category == "book":
            self.use_book(target)
        else:
            raise Exception("Prepare books: unsupported category " + category)

    def find(self, keyword, target, category):
        self.prepare_books(target, category)
        matched_entry_cnt, matched_book_cnt = 0, 0
        for b in self.books:
            bo = self.books[b]
            matches = bo.search_notes(keyword)
            if matches != []:
                matched_book_cnt += 1
                for k,entry in enumerate(matches):
                    matched_entry_cnt += 1
                    print("==Match #" + str(matched_entry_cnt) + "==")
                    print("BOOK:", colored(b, "y"), end=", ")
                    print("TITLE:", end=' ')
                    entry.show_key()
                    entry.show_note()
        print("{0} matched record(s) found in {1} book(s).".format(\
              colored(str(matched_entry_cnt), "r"), \
              colored(str(matched_book_cnt), "r")))
        
    def review(self, target, category):
        self.prepare_books(target, category)   
        review_seq = []
        for b in self.books:
            # reivew_seq will be ["book1", "book1", "book2", ...]
            review_seq += [b]*self.books[b].get_note_count()
            self.books[b].start_review()

        random.shuffle(review_seq)
        for b in review_seq:
            print("BOOK:", colored(b, "y"))
            try:
                self.books[b].review_one_note()
            except KeyboardInterrupt:
                break

        for b in self.books:
            self.books[b].end_review()

    def fortune(self, target, category):
        self.prepare_books(target, category)
        book_seq = [] 
        for b in self.books:
            book_seq += [b]*self.books[b].get_note_count()
        random_book = random.choice(book_seq)
        note = self.books[random_book].fortune()
        print("BOOK:", colored(random_book, "y"), end=", ")
        print("TITLE:", end=' ')
        note.show_key()
        note.show_note()
