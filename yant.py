#!/usr/bin/python3
import os
import re
import sys
import logging
import random
import argparse
import operator
from itertools import accumulate

from entry import Entry
import book
import yant_args
import utils
import yant_utils
from yant_class import Yant
from colors import colors
colored = colors.colored

def main(argv):

    utils.require_python_version(3) # major version should be 3
    args = yant_args.parse(argv[1:])
    if args.cmd == None:
        raise Exception("No command provided. Use '-h' to see available commands.")

    log = logging.getLogger("yant")
    valid_name_pattern =  "^[a-zA-Z][a-zA-Z0-9_-]*$"

    entry_type = Entry
    yant_obj = Yant(entry_type)
    '''
    if args.book:
        yant_utils.validate_name(valid_name_pattern, args.book)
    if args.cmd not in ["import", "export", "update"] and args.tag:
        yant_utils.validate_name(valid_name_pattern, args.tag)
    '''    
    all_books = yant_utils.list_all_books() 
   
    if args.cmd == "list":
        if args.book:
            if args.book in all_books:
                yant_obj.use_book(args.book)
                yant_obj.get_book_obj(args.book).show_detail()
            else:
                print(colored(args.book + " doesn't exist.", "r"))
                return
        else: # use tag
            matched_books = yant_obj.get_books_by_tag(args.tag)
            if matched_books == []:
                print(colored("No book found for the tag.", "r"))
                return
            max_name_len = max([len(b) for b in matched_books])
            listed_per_line = 100 // (max_name_len+4)
            adjusted_names = [b+" "*(max_name_len+4-len(b)) for b in matched_books]
            print(colored("Books with tag '" + args.tag + "':", "m"))
            while adjusted_names != []:
                line = "".join(adjusted_names[:listed_per_line])
                adjusted_names = adjusted_names[listed_per_line:]
                print(colored(line, "y"))
            return

    elif args.cmd == "create":
        if args.book in all_books:
            sys.stderr.write("Notebook "+ args.book + " exists. ")
            sys.stderr.write("No new notebook created.\n")
        else:
            desc = input("Enter a short description for the book: ")
            yant_obj.create_book(args.book, args.tag, desc)
        return

    elif args.cmd == "add":
        if args.note: # add a note
            yant_obj.add_note(args.book, args.note)
        else: # add a tag
            yant_obj.add_tag(args.book, args.tag)

    elif args.cmd == "update":
        yant_obj.update_note(args.book, args.note)

    elif args.cmd == "delete":
        if args.note:
            yant_obj.delete_note(args.book, args.note)
        else:
            yant_obj.delete_tag(args.book, args.tag)

    elif args.cmd == "import":
        yant_obj.import_book(args.book, args.file)

    elif args.cmd == "export":
        yant_obj.export_book(args.book, args.file)

    elif args.cmd == "find":
        if args.book:
            yant_obj.find(args.keyword, args.book, "book")
        else:
            yant_obj.find(args.keyword, args.tag, "tag")
    elif args.cmd == "review":
        if args.book:
            yant_obj.review(args.book, "book")
        else:
            yant_obj.review(args.tag, "tag")

    elif args.cmd == "fortune":
        if args.book:
            yant_obj.fortune(args.book, "book")
        else:
            yant_obj.fortune(args.tag, "tag")
        '''
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
        '''
if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print("Error:", e)
