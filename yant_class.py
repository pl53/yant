import random
import logging

from yant_utils import list_all_books
from entry import Entry
from book import Notebook
from tag import TagManager
from colors import colors
colored = colors.colored

class Yant:
    def __init__(self, note_class):
        self.tag_manager = TagManager()
        self.note_class = note_class
        self.all_books = list_all_books()
        self.opened_books = {}
        self.logger = logging.getLogger("Yant")

    def exist_book(self, book):
        return book in self.all_books

    # create book object and apply tags
    def create_book(self, book, tags=[], description="No description"):
        if self.exist_book(book):
            self.logger.warn("Book " + book + " already exists.")
        else:
            new_book_obj = Notebook(book, self.note_class)
            if "all" not in tags: # default tag for all books
                tags.append("all")
            new_book_obj.create_book(tags, description)
            for tag in tags:
                self.tag_manager.tag_book(tag, book)

    def use_book(self, book):
        if not self.exist_book(book):
            raise Exception("No data for book '{}' found.".format(book))
        self.opened_books[book] = Notebook(book, self.note_class) 

    def use_tag(self, tag):
        books = self.tag_manager.get_books(tag)
        for b in books:
            if not self.exist_book(b):
                # if a booking is missing here, it should be a warning
                self.logger.warn("No data for book '{}' found.".format(b))
            else:
                self.opened_books[b] = Notebook(b, self.note_class)

    def add_note(self, book, note_title):
        self.use_book(book)
        note_obj = Entry(note_title, ask_user_input=True)
        self.opened_books[book].add_note(note_obj)

    def add_tags(self, book, tags):
        self.use_book(book)
        for tag in tags:
            self.opened_books[book].add_tag(tag)
            self.tag_manager.tag_book(tag, book)

    def update_note(self, book, note_title):
        self.use_book(book)
        self.opened_books[book].update_note(note_title)

    def delete_note(self, book, note_title):
        self.use_book(book)
        self.opened_books[book].delete_note(note_title)

    def delete_tag(self, book, tags):
        self.use_book(book)
        for tag in tags:
            self.opened_books[book].delete_tag(tag)
            self.tag_manager.untag_book(tag, book)

    def get_books_by_tag(self, tag):
        return self.tag_manager.get_books(tag)

    def get_book_obj(self, book):
        return self.opened_books[book]    

    def import_book(self, book, source):
        self.use_book(book)
        self.opened_books[book].import_book(source)

    def export_book(self, book, source):
        self.use_book(book)
        self.opened_books[book].export_book(source)

    def fetch_books(self, target, category):
        if category == "tag":
            tags = target.split(",")
            for tag in tags:
                self.use_tag(tag)
        elif category == "book":
            self.use_book(target)
        else:
            raise Exception("Fetch books: unsupported category " + category)

    def find(self, keyword, target, category):
        self.fetch_books(target, category)
        matched_entry_cnt, matched_book_cnt = 0, 0
        for b in self.opened_books:
            bo = self.opened_books[b]
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
        self.fetch_books(target, category)   
        review_seq = []
        for b in self.opened_books:
            # reivew_seq will be ["book1", "book1", "book2", ...]
            weight = self.opened_books[b].get_note_count()
            review_seq += [b] * weight
            self.opened_books[b].start_review()

        random.shuffle(review_seq)
        for b in review_seq:
            print("BOOK:", colored(b, "y"))
            try:
                self.opened_books[b].review_one_note()
            except KeyboardInterrupt:
                break

        for b in self.opened_books:
            self.opened_books[b].end_review()

    def fortune(self, target, category):
        self.fetch_books(target, category)
        book_seq = [] 
        for b in self.opened_books:
            book_seq += [b]*self.opened_books[b].get_note_count()
        random_book = random.choice(book_seq)
        note = self.opened_books[random_book].fortune()
        print("BOOK:", colored(random_book, "y"), end=", ")
        print("TITLE:", end=' ')
        note.show_key()
        note.show_note()
