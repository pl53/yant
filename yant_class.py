import random
import logging

from yant_utils import list_all_books
from flashcard import Flashcard
from book import Notebook
from tag import TagManager
from colors import colors
colored = colors.colored

class Yant:
    def __init__(self, flashcard_class):
        self.tag_manager = TagManager()
        self.flashcard_class = flashcard_class
        self.all_books = list_all_books()
        self.opened_books = {}
        self.logger = logging.getLogger("Yant")

    def exist_book(self, book):
        return book in self.all_books

    # create book object and apply tags
    def create_book(self, book, tags=[], description="Yant book"):
        # set need_description to false for unittest
        self.logger.info("Create book " + book + \
                         " with tags: " + ",".join(tags) + ".")

        if self.exist_book(book):
            raise Exception("Book '" + book + "' already exists.")
        else:
            if "all" not in tags: # default tag for all books
                tags.append("all")
            new_book_obj = Notebook(book, self.flashcard_class)
            new_book_obj.create(tags, description)
            for tag in tags:
                self.tag_manager.tag_book(tag, book)

    def destroy_book(self, book):
        self.use_book(book)
        for tag in self.opened_books[book].get_tags():
            self.tag_manager.untag_book(tag, book)
        self.get_book_obj(book).destroy()

    def use_book(self, book):
        if not self.exist_book(book):
            raise Exception("Book " + colored(book, "b") + " doesn't exist.")
        self.opened_books[book] = Notebook(book, self.flashcard_class) 

    def use_tag(self, tag):
        books = self.tag_manager.get_books(tag)
        for b in books:
            if not self.exist_book(b):
                # if a booking is missing here, it should be a warning
                self.logger.warn("No data for book '{}' found.".format(b))
            else:
                self.opened_books[b] = Notebook(b, self.flashcard_class)

    def show_book_by_name(self, book):
        self.use_book(book)
        self.get_book_obj(book).show_detail()

    def show_book_by_tag(self, tag):
        matched_books = self.get_books_by_tag(tag)
        if matched_books == []:
            print(colored("No book found for the tag(s).", "r"))
        else:
            max_name_len = max([len(b) for b in matched_books])
            listed_per_line = 100 // (max_name_len+4)
            adjusted_names = [b+" "*(max_name_len+4-len(b)) for b in matched_books]
            print("Books with tag '" + colored(tag, "m") + "':")
            while adjusted_names != []:
                line = "".join(adjusted_names[:listed_per_line])
                adjusted_names = adjusted_names[listed_per_line:]
                print(colored(line, "b"))

    def add_flashcard(self, book, flashcard_title):
        self.use_book(book)
        flashcard_obj = Flashcard(flashcard_title, ask_user_input=True)
        self.opened_books[book].add_flashcard(flashcard_obj)

    def append_flashcard(self, book, flashcard_title, raw_notes, use_hashkey):
        '''
        self.use_book(book)
        note_list = raw_notes.split('&&')
        if use_hashkey:
            self.opened_books[book].append_flashcard_by_hashkey(flashcard_title, note_list)
        else:
            self.opened_books[book].append_flashcard_by_title(flashcard_title, note_list)
        '''
        print("Sorry, this feature hasn't been implemented. Please use 'add' or 'update' instead")

    def add_tags(self, book, tags):
        self.use_book(book)
        for tag in tags:
            self.opened_books[book].add_tag(tag)
            self.tag_manager.tag_book(tag, book)

    def update_flashcard(self, book, flashcard_title):
        self.use_book(book)
        self.opened_books[book].update_flashcard(flashcard_title)

    def remove_flashcard(self, book, flashcard_title):
        self.use_book(book)
        self.opened_books[book].delete_flashcard(flashcard_title)

    def remove_tag(self, book, tags):
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
        self.opened_books[book].import_(source)

    def export_book(self, book, source):
        self.use_book(book)
        self.opened_books[book].export(source)

    def fetch_books(self, target, category):
        if category == "tag":
            tags = target.split(";")
            for tag in tags:
                self.use_tag(tag)
        elif category == "book":
            self.use_book(target)
        else:
            self.logger.error("Fetch books: unsupported category " + category)
            raise Exception("Internal error when fetching books.")

    def find(self, keyword, target, category, whole_word, exec_cmd):
        self.fetch_books(target, category)
        matched_flashcard_cnt, matched_book_cnt = 0, 0
        for b in self.opened_books:
            bo = self.opened_books[b]
            matches = bo.search_flashcards(keyword, whole_word)
            if matches != []:
                matched_book_cnt += 1
                for k,flashcard in enumerate(matches):
                    matched_flashcard_cnt += 1
                    print("==Match #" + str(matched_flashcard_cnt) + "==")
                    print("BOOK:", colored(b, "y"), end=", ")
                    print("TITLE:", end=' ')
                    flashcard.show_key()
                    flashcard.show_note(exec_cmd)
        print("{0} matched record(s) found in {1} book(s).".format(\
              colored(str(matched_flashcard_cnt), "r"), \
              colored(str(matched_book_cnt), "r")))
        
    def review(self, target, category, exec_cmd):
        self.fetch_books(target, category)   
        review_seq = []
        for b in self.opened_books:
            # reivew_seq will be ["book1", "book1", "book2", ...]
            weight = self.opened_books[b].get_flashcard_count()
            review_seq += [b] * weight
            self.opened_books[b].start_review()

        random.shuffle(review_seq)
        for b in review_seq:
            print("BOOK:", colored(b, "y"))
            try:
                self.opened_books[b].review_one_flashcard(exec_cmd)
            except KeyboardInterrupt:
                break

        for b in self.opened_books:
            self.opened_books[b].end_review()

    def fortune(self, target, category):
        self.fetch_books(target, category)
        book_seq = [] 
        for b in self.opened_books:
            book_seq += [b]*self.opened_books[b].get_flashcard_count()
        random_book = random.choice(book_seq)
        flashcard = self.opened_books[random_book].fortune()
        print("BOOK:", colored(random_book, "y"), end=", ")
        print("TITLE:", end=' ')
        flashcard.show_key()
        flashcard.show_note()
