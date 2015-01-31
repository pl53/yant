#!/usr/bin/python3

import os
import sys
import argparse
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
    parser.add_argument("book_name", nargs="?", default="__list__")
    parser.add_argument("-w", "--word", action="store_true", default=False,\
                        help="this is a word notebook")
    group1.add_argument("-r", "--review", action="store_true",default=False,\
                        help="review notebook to build knowledge")
    group1.add_argument("-i", "--import_book", metavar="input_file", nargs="?",\
                        const='__MEMO_IMPORT__', help="import the notebook from a textfile")
    group1.add_argument("-o", "--export_book", metavar="output_file", nargs="?",\
                        const='__MEMO_EXPORT__', help="export the notebook to a textfile")
    group1.add_argument("-e", "--desc", metavar="description", nargs='?',\
                        const='__MEMO_DESC__', help="update notebook description")
    group1.add_argument("-c", "--create", action="store_true", default=False,\
                        help="create a notebook")
    group1.add_argument("-g", "--debug", action="store_true", default=False, \
                        help="debug mode, print more information")
    group2.add_argument("-a", "--add", metavar="new_key", nargs='?', const='__MEMO_ADD__', \
                        help="add one entry to the notebook")
    group2.add_argument("-d", "--delete", metavar="old_key", nargs='?', const='__MEMO_DELETE__',\
                        help="delete one entry from the notebook")
    group2.add_argument("-u", "--update", metavar="old_key", nargs='?', const='__MEMO_UPDATE__', \
                        help="update notes for an entry")
    group2.add_argument("-s", "--search", metavar="keyword", \
                        help="search note with the given keyword, currently only one keyword supported")
    group2.add_argument("-f", "--fortune",action="store_true",default=False, \
                        help="fortune cookie with the notebook")
    return parser.parse_args(args)

''' unfinished '''
def get_booklist(note_path):
    # retrive current notebooks
    all_files = os.listdir(note_path)
    # e.g. ".word.db" -> ["", "word", "db"]
    split_names = [s.split(".") for s in all_files] 
    current_books = [name[-2] for name in split_names \
                   if len(name) > 1 and name[-1] == "db"]
    return current_books

'''unfinished'''
def validate_metafile(note_path):
    meta_file = os.path.join(note_path, meta_name)
    all_files = os.listdir(note_path)
    try:
        book_files = all_files.remove(meta_file)
    except:
        pass # ignore if metafile not in it
    split_names = [s.split(".") for s in book_files] 
    

if __name__ == "__main__":

    check_python_version()
    note_path = get_data_path()
    args = parse_arguments(sys.argv[1:])
    if args.debug:
        print(args)
 
    meta_file = os.path.join(note_path, args.book_name+".mt")
    book_file = os.path.join(note_path, args.book_name+".db")
    #book_type = ""
    #book_list = get_booklist(note_path)
    #validate_metafile(note_path, book_file)
    if args.book_name == "__list__":
       print(colored("Current Notebooks:", "m"))
       tab_list = "\t".join(get_booklist(note_path))
       print(colored(tab_list,"y"))
       print('For software usage, use "yanote -h"')
       quit()
    else:
       book_name = args.book_name.strip()


    if args.word:
        entry_type = entry.wordEntry
    else:
        entry_type = entry.Entry

    book = book.Notebook(book_file, entry_type)

    if args.create:
        if book_name in get_booklist(note_path):
            print("Notebook "+book_name+" exists. No new notebook created.")
        else:
            desc = input("Enter a short description for the book: ")
            book.create_book(desc)
    else:
        if book_name not in get_booklist(note_path):
            print("Notebook "+book_name+" does not exist.") 
            print("Please use -c or --create to create one first.")
            quit()

    if args.desc != None:
        if args.desc == '__MEMO_DESC__':
            args.desc = input("Enter a short description for the book: ")
        book.update_desc(args.desc)

    if args.word and len(sys.argv) == 3 or len(sys.argv) == 2: # no action specified, print book
        book.description()

    if args.import_book != None:
        if args.import_book == "__MEMO_IMPORT__":
            print("No book name or invalid book name")
            quit()
        book.import_book(args.import_book)

    if args.export_book != None:
        if args.export_book == "__MEMO_EXPORT__":
            print("No book name or invalid book name")
            quit()
        book.export_book(args.export_book)

    if args.add != None:
        if args.add == "__MEMO_ADD__":
            while True:
                key = input("Please input an entry (press {} to finish): ".\
                        format(colored("Enter", "c")))
                if key == "":
                    break
                book.add_entry(key, entry_type)
        else:
            book.add_entry(args.add, entry_type)
   
    if args.update != None:
        if args.update == '__MEMO_UPDATE__':
            args.update = input("Please input the item to update: ")
        book.update_entry(args.update)

    if args.delete != None:
        if args.delete == '__MEMO_DELETE__':
            args.delete = input("Please input the item to delete: ")
        book.delete_entry(args.delete)

    if args.search != None:
        book.search_entries(args.search)


    if args.fortune:
        entry = book.pick_random_entry()
        entry.show_key()
        entry.show_note()
       

    if args.review:
        book.random_review()
    #book.close()
