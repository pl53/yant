#!/usr/bin/python3
import os
import re
import sys
import random
import argparse
import operator
from itertools import accumulate
import entry
import book
from colors import colors
colored = colors.colored

meta_name = ".memo.meta"

def check_python_version():
    if sys.version_info.major < 3:
        print("Please use Python 3 or higher.")
        quit()

def get_data_path():
    note_path = os.getenv("YANOTE_PATH")
    #note_path = "./data"
    if note_path == None:
        note_path = os.path.join(os.getenv("HOME"), ".yanote")
    if not os.path.exists(note_path):
        os.makedirs(note_path)
    return note_path

def parse_arguments(args):
    parser = argparse.ArgumentParser(prog="python3 yanote.py")
    #group1 = parser.add_mutually_exclusive_group()
    group2 = parser.add_mutually_exclusive_group()
    #parser.add_argument("-g", "--debug", action="store_true", default=False, \
    #                    help="debug mode, print more information")
    group2.add_argument("-l", "--list", \
                        action="store_true", \
                        default=False, \
                        dest="lst", \
                        help="list notebooks matching given pattern")
    #parser.add_argument("-w", "--word", action="store_true", default=False,\
    #                    help="this is a word notebook")
    group2.add_argument("-c",\
                        "--create",\
                        action="store_true",\
                        default=False,\
                        help="create a notebook")
    group2.add_argument("-a", "--add",\
                        metavar="title",\
                        nargs='?',\
                        const='__MEMO_ADD__',\
                        help="add one note entry to the notebook")
    group2.add_argument("-d", "--delete",\
                        metavar="title",\
                        nargs='?',\
                        const='__MEMO_DELETE__',\
                        help="delete the note entry with given title")
    group2.add_argument("-u", "--update",\
                        metavar="title",\
                        nargs='?',\
                        const='__MEMO_UPDATE__', \
                        help="update the note entry with given title")
    group2.add_argument("-s", "--search",\
                        metavar="pattern", \
                        help="search notes with the given pattern")
    group2.add_argument("-r", "--review",\
                        action="store_true",\
                        default=False,\
                        help="review notebook to build knowledge")
    group2.add_argument("-i", "--import",\
                        metavar="input_file",\
                        nargs="?",\
                        const='__MEMO_IMPORT__',\
                        dest="import_book",\
                        help="import a notebook from the textfile")
    group2.add_argument("-o", "--export",\
                        metavar="output_file",\
                        nargs="?",\
                        const='__MEMO_EXPORT__',\
                        dest="export_book",\
                        help="export the notebook to a textfile")
    group2.add_argument("-e", "--desc",\
                        metavar="description",\
                        nargs='?',\
                        const='__MEMO_DESC__',\
                        help="update notebook description")
    group2.add_argument("-f", "--fortune",
                        action="store_true",\
                        default=False, \
                        help="I feel lucky :-)")
    parser.add_argument("book",\
                        metavar="book_name",\
                        help="name or pattern of book(s)")
    return parser.parse_args(args)

def get_booklist(note_path):
    # retrive current notebooks
    all_files = os.listdir(note_path)
    db_files = [f for f in all_files if f.endswith(".db")]
    current_books = [name[:-3] for name in db_files]
    return current_books

if __name__ == "__main__":

    check_python_version()
    args = parse_arguments(sys.argv[1:])
 
    #meta_file = os.path.join(note_path, args.book+".mt")
    #book_type = ""
    #book_list = get_booklist(note_path)
    #validate_metafile(note_path, book_file)
    note_path = get_data_path()
    all_books = get_booklist(note_path) # note_path guaranteed to be valid
    book_pattern = args.book.strip() # support regular expression
    try:
        matched_books = [b for b in all_books if re.match(book_pattern, b)]
    except:
        sys.stderr.write("Invalid regular expression " + book_pattern + "\n")
        sys.exit(1)
    entry_type = entry.Entry

    if args.lst:
        max_name_len = max([len(b) for b in matched_books])
        listed_per_line = 100 // (max_name_len+4)
        adjusted_names = [b+" "*(max_name_len+4-len(b)) for b in matched_books]
        print(colored("Current Notebooks:", "m"))
        while adjusted_names != []:
            line = "".join(adjusted_names[:listed_per_line])
            adjusted_names = adjusted_names[listed_per_line:]
            print(colored(line, "y"))
        sys.exit(0)

    # sanity check
    if not args.create:
        if matched_books == []:
            sys.stderr.write("No book found in your collection.\n")
            sys.stderr.write("Please use -c or --create to create one first.\n")
            sys.exit(1)
        elif (args.desc or args.add or args.update or \
                args.delete or args.import_book or args.export_book) and \
                len(matched_books) > 1:
            sys.stderr.write("More than one book found: " + "\t".join(matched_books))
            sys.stderr.write("The operation can be applied to only one book.\n")
            sys.exit(1)
        else:
            book_file_list = [os.path.join(note_path, b+".db") for b in matched_books]
            book_obj_list = [book.Notebook(b, entry_type) for b in book_file_list]
            book_obj = book_obj_list[0]

    if args.create:
        if not re.match("^[a-zA-Z][a-zA-Z0-9_-]*$", book_pattern): 
            sys.stderr.write("Illegal book name. Regular expression is " + \
                "not supported for creating or updating a notebook.\n")
        elif matched_books != []:
            sys.stderr.write("Notebook "+ args.book + " exists. No new notebook created.\n")
        else:
            desc = input("Enter a short description for the book: ")
            book_file = os.path.join(note_path, args.book+".db")
            book.Notebook(book_file, entry_type).create_book(desc)
    elif args.desc:
        if args.desc == '__MEMO_DESC__':
            args.desc = input("Enter a short description for the book: ")
        book_obj.update_desc(args.desc)
    elif args.add:
        if args.add == "__MEMO_ADD__":
            while True:
                key = input("Please input an entry (press {} to finish): ".\
                        format(colored("Enter", "c")))
                if key == "":
                    break
                book_obj.add_entry(key, entry_type)
        else:
            book_obj.add_entry(args.add, entry_type)
    elif args.update:
        if args.update == '__MEMO_UPDATE__':
            args.update = input("Please input the item to update: ")
        book_obj.update_entry(args.update)
    elif args.delete:
        if args.delete == '__MEMO_DELETE__':
            args.delete = input("Please input the item to delete: ")
        book_obj.delete_entry(args.delete)
    elif args.import_book:
        book_obj.import_book(args.import_book)
    elif args.export_book:
        book_obj.export_book(args.export_book)
    elif args.search:
        matched_entry_cnt, matched_book_cnt = 0, 0
        for i,bo in enumerate(book_obj_list):
            matches = bo.search_entries(args.search)
            if matches:
                matched_book_cnt += 1
                for k,entry in enumerate(matches):
                    matched_entry_cnt += 1
                    print("==Match #" + str(matched_entry_cnt) + "==")
                    print("BOOK:", colored(matched_books[i], "y"), end=", ")
                    print("TITLE:", end=' ')
                    entry.show_key()
                    entry.show_note()
        print("{0} matched record(s) found in {1} book(s).".format(\
              colored(str(matched_entry_cnt), "r"), \
              colored(str(matched_book_cnt), "r")))
    elif args.review:
        review_seq = []
        note_cnt = [bo.get_entry_count() for bo in book_obj_list]
        for i in range(len(matched_books)):
            new_reviews = [(matched_books[i], book_obj_list[i], k) \
                           for k in range(note_cnt[i])]
            review_seq += new_reviews
        random.shuffle(review_seq)
        for i, r in enumerate(review_seq):
            print("BOOK:", colored(r[0], "y"))
            rval = r[1].random_review([r[2]])
            if rval != 0:
                break
        print(colored(("\nYou have finished reviewing {} of {} records,"+\
              " keep going!").format(i+1, len(review_seq)), 'b'))
        #for bo in book_obj_list:
        #    bo.random_review()
    elif args.fortune:
        note_cnt = [bo.get_entry_count() for bo in book_obj_list]
        accumulated_cnt = list(accumulate(note_cnt, operator.add))
        if accumulated_cnt[-1] == 0:
            print("None entry in selected books.")
            sys.exit(0)
        cdf = [cnt*1.0/accumulated_cnt[-1] for cnt in accumulated_cnt]
        r = random.random()
        for i in range(len(cdf)):
            if r <= cdf[i]: 
                break
        random_entry = book_obj_list[i].pick_random_entry()
        print("BOOK:", colored(matched_books[i], "y"))
        random_entry.show_key()
        random_entry.show_note()
           
#        raw_entries = [bo.pick_random_entry() for bo in book_obj_list]
#        entries = [(matched_books[i], raw_entries[i]) \
#                   for i in range(len(raw_entries)) if raw_entries[i] != None]
#        if entries != []:
#            book_name, entry = random.choice(entries)
#            print("BOOK:", colored(book_name, "y"))
#            entry.show_key()
#            entry.show_note()
#        else:
#            print("None entry in selected books.")
