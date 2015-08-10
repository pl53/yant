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
    if args.sub_command == None:
        raise Exception("No command provided. Use '-h' to see available commands.")
    log_file = os.path.join(yant_utils.get_data_path(), "yant.log")
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logger = logging.getLogger("Yant")
    logger.info("Yant starts.")

    valid_name_pattern =  "^[a-zA-Z][a-zA-Z0-9_-]*$"

    yant_obj = Yant(Entry)
    logger.setLevel(logging.ERROR)
    if not yant_obj.exist_book("scratchpad"):
        yant_obj.create_book(
            book = "scratchpad",\
            tags=["all"],\
            description="The default notebook used when a book is not specified")
    logger.setLevel(logging.WARNING)
    '''
    if args.book:
        yant_utils.validate_name(valid_name_pattern, args.book)
    if args.sub_command not in ["import", "export", "update"] and args.tag:
        yant_utils.validate_name(valid_name_pattern, args.tag)
    '''    
   
    if args.sub_command in ["list", "lst", "show"]:
        if args.use_tag:
            tags = args.target.split(',')
            matched_books = []
            for t in tags:
                matched_books = yant_obj.get_books_by_tag(t)
            if matched_books == []:
                print(colored("No book found for the tag(s).", "r"))
            else:
                max_name_len = max([len(b) for b in matched_books])
                listed_per_line = 100 // (max_name_len+4)
                adjusted_names = [b+" "*(max_name_len+4-len(b)) for b in matched_books]
                print("Books with tag(s) '" + colored(args.target, "m") + "':")
                while adjusted_names != []:
                    line = "".join(adjusted_names[:listed_per_line])
                    adjusted_names = adjusted_names[listed_per_line:]
                    print(colored(line, "y"))
        else: # show details of the specified book 
            if yant_obj.exist_book(args.target):
                yant_obj.use_book(args.target)
                yant_obj.get_book_obj(args.target).show_detail()
            else:
                print(colored(args.target + " doesn't exist.", "r"))

    elif args.sub_command == "create":
        if yant_obj.exist_book(args.args.book):
            logger.warning("Notebook "+ args.book + " exists. ")
            logger.warning("No new notebook created.")
        else:
            desc = input("Enter a short description for the book: ")
            tags = args.tags.split(',')
            yant_obj.create_book(args.book, tags, desc)
        return

    elif args.sub_command == "add":
        yant_obj.add_note(args.book, args.note)

    elif args.sub_command in ["update", "up"]:
        yant_obj.update_note(args.book, args.note)

    elif args.sub_command in ["delete", "del", "rm"]:
        yant_obj.delete_note(args.book, args.note)

    elif args.sub_command == "tag":
        tags = args.tags.split(',')
        if args.delete_tags:
            yant_obj.delete_tag(args.book, tags)
        else:
            yant_obj.add_tags(args.book, tags)

    elif args.sub_command == "import":
        yant_obj.import_book(args.book, args.file)

    elif args.sub_command == "export":
        yant_obj.export_book(args.book, args.file)

    elif args.sub_command in ["find", "search"]:
        if args.use_tag:
            yant_obj.find(args.keyword, args.target, "tag")
        else:
            yant_obj.find(args.keyword, args.target, "book")
    elif args.sub_command == "review":
        if args.use_tag:
            yant_obj.review(args.target, "tag")
        else:
            yant_obj.review(args.target, "book")

    elif args.sub_command == "fortune":
        if args.use_tag:
            yant_obj.fortune(args.target, "tag")
        else:
            yant_obj.fortune(args.target, "book")

if __name__ == "__main__":
#    try:
        main(sys.argv)
#    except Exception as e:
#        print("Error:", e)
