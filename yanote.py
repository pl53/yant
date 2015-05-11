#!/usr/bin/python3

import os
import sys
import argparse
import re
import random
import json
import entry
import book
from colors import colors
colored = colors.colored

meta_name = ".memo.meta"
#book_type_list = {"word": note_entry.wordEntry, \
#                  "general": note_entry.generalEntry}

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
    group1 = parser.add_mutually_exclusive_group()
    group2 = parser.add_mutually_exclusive_group()
    parser.add_argument("-g", "--debug", action="store_true", default=False, \
                        help="debug mode, print more information")
    group1.add_argument("-l", "--lst",\
                        action="store_true",\
                        default=False,\
                        help="list all notebooks")
    group1.add_argument("-b", "--book",\
                        metavar="book_name")
    #parser.add_argument("-w", "--word", action="store_true", default=False,\
    #                    help="this is a word notebook")
    group2.add_argument("-r", "--review",\
                        action="store_true",\
                        default=False,\
                        help="review notebook to build knowledge")
    group2.add_argument("-i", "--import_book",\
                        metavar="input_file",\
                        nargs="?",\
                        const='__MEMO_IMPORT__',\
                        help="import the notebook from a textfile")
    group2.add_argument("-o", "--export_book",\
                        metavar="output_file",\
                        nargs="?",\
                        const='__MEMO_EXPORT__',\
                        help="export the notebook to a textfile")
    group2.add_argument("-e", "--desc",\
                        metavar="description",\
                        nargs='?',\
                        const='__MEMO_DESC__',\
                        help="update notebook description")
    group2.add_argument("-c",\
                        "--create",\
                        action="store_true",\
                        default=False,\
                        help="create a notebook")
    group2.add_argument("-a",\
                        "--add",\
                        metavar="new_key",\
                        nargs='?',\
                        const='__MEMO_ADD__',\
                        help="add one entry to the notebook")
    group2.add_argument("-d", "--delete",\
                        metavar="old_key",\
                        nargs='?',\
                        const='__MEMO_DELETE__',\
                        help="delete one entry from the notebook")
    group2.add_argument("-u", "--update",\
                        metavar="old_key",\
                        nargs='?',\
                        const='__MEMO_UPDATE__', \
                        help="update notes for an entry")
    group2.add_argument("-s", "--search",\
                        metavar="keyword", \
                        help="search note with the given keyword, currently only one keyword supported")
    group2.add_argument("-f", "--fortune",
                        action="store_true",\
                        default=False, \
                        help="fortune cookie with the notebook")
    return parser.parse_args(args)

def get_booklist(note_path):
    # retrive current notebooks
    all_files = os.listdir(note_path)
    db_files = [f for f in all_files if f.endswith(".db")]
    current_books = [name[:-3] for name in db_files]
    return current_books

if __name__ == "__main__":

    check_python_version()
    note_path = get_data_path()
    args = parse_arguments(sys.argv[1:])
    if args.debug:
        print(args)
 
    #meta_file = os.path.join(note_path, args.book+".mt")
    #book_type = ""
    #book_list = get_booklist(note_path)
    #validate_metafile(note_path, book_file)
    all_books = get_booklist(note_path)
    if args.lst:
        print(colored("Current Notebooks:", "m"))
        tab_list = "\t".join(all_books)
        print(colored(tab_list, "y"))
        print('For software usage, use "yanote -h"')
        sys.exit(0)
    else:
        book_pattern = args.book.strip() # support regular expression

    #if args.word:
    #    entry_type = entry.wordEntry
    #else:
    #    entry_type = entry.Entry
    entry_type = entry.Entry

    # sanity check
    if args.create or args.desc or args.add or args.update or \
            args.delete or args.import_book or args.export_book:
        if not re.match("^[a-zA-Z][a-zA-Z0-9_-]*$", book_pattern):
            print ("Illegal book name. Regular expression is not supported for creating \
                    or updating a notebook.")
            sys.exit(1)
        elif args.create and matched_books != []: 
            print("Notebook "+ args.book + " exists. No new notebook created.")
            sys.exit(1)
        elif not args.create and matched_books == []:
            print("No book found in your collection.")
            print("Please use -c or --create to create one first.")
            sys.exit(1)
        else:
            book_file = os.path.join(note_path, args.book_pattern+".db")
            book_obj = book.Notebook(book_file, entry_type)
    else: # use regular expression to match multiple books
        matched_books = [b for b in all_books if re.match(book_pattern, b)]
        book_file_list = [os.path.join(note_path, b+".db") for b in matched_books]
        book_obj_list = [book.Notebook(b, entry_type) for b in book_file_list]

    if args.create:
        desc = input("Enter a short description for the book: ")
        book_obj.create_book(desc)

    if args.desc:
        if args.desc == '__MEMO_DESC__':
            args.desc = input("Enter a short description for the book: ")
        book_obj.update_desc(args.desc)

    if args.add:
        if args.add == "__MEMO_ADD__":
            while True:
                key = input("Please input an entry (press {} to finish): ".\
                        format(colored("Enter", "c")))
                if key == "":
                    break
                book_obj.add_entry(key, entry_type)
        else:
            book_obj.add_entry(args.add, entry_type)
   
    if args.update:
        if args.update == '__MEMO_UPDATE__':
            args.update = input("Please input the item to update: ")
        book_obj.update_entry(args.update)

    if args.delete:
        if args.delete == '__MEMO_DELETE__':
            args.delete = input("Please input the item to delete: ")
        book_obj.delete_entry(args.delete)

    if args.import_book:
        book_obj.import_book(args.import_book)

    if args.export_book:
        book_obj.export_book(args.export_book)


    if args.search:
        for bo in book_obj_list:
            bo.search_entries(args.search)


    if args.fortune:
        raw_entries = [bo.pick_random_entry() for bo in book_obj_list]
        entries = [(matched_books[i], raw_entries[i]) \
                   for i in range(len(raw_entries)) if raw_entries[i] != None]
        if entries != []:
            book_name, entry = random.choice(entries)
            print("BOOK:", colored(book_name, "y"))
            entry.show_key()
            entry.show_note()
        else:
            print("None entry in selected books.")

    if args.review:
        for bo in book_obj_list:
            bo.random_review()
    #book.close()
