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
    logger.setLevel(logging.INFO)
    '''
    if args.book:
        yant_utils.validate_name(valid_name_pattern, args.book)
    if args.sub_command not in ["import", "export", "update"] and args.tag:
        yant_utils.validate_name(valid_name_pattern, args.tag)
    '''    
   
    if args.sub_command in ["list", "lst", "show"]:
        if args.book: # show details of the specified book 
            yant_obj.show_book_by_name(args.book)
        else:
            yant_obj.show_book_by_tag(args.tag)

    elif args.sub_command == "create":
        tags = args.tags.split(';')
        yant_obj.create_book(args.book, tags, args.desc)
        print("Book'" + colored(book, "b") + " created.")

    elif args.sub_command == "destroy":
        print("Warning: your are deleting book '" + colored(book, "b") +\
              "', which is unrecoverable!")
        confirm = input("Are your sure? (Y/N): ")
        if confirm in "Yy":
            yant_obj.destroy_book(args.book)     
        print("Book'" + colored(book, "b") + " deleted.")

    elif args.sub_command == "add":
        yant_obj.add_note(args.book, args.note)
        print("Record added/updated to book '" + args.book + "'.")

    elif args.sub_command in ["update", "up"]:
        yant_obj.update_note(args.book, args.note)

    elif args.sub_command in ["remove", "rm"]:
        yant_obj.remove_note(args.book, args.note)

    elif args.sub_command == "tag":
        tags = args.tags.split(';')
        if args.delete_tags:
            yant_obj.remove_tag(args.book, tags)
        else:
            yant_obj.add_tags(args.book, tags)

    elif args.sub_command == "import":
        yant_obj.import_book(args.book, args.file)

    elif args.sub_command == "export":
        yant_obj.export_book(args.book, args.file)

    elif args.sub_command in ["find", "search"]:
        exec_cmd = []
        if args.exec:
            exec_cmd = args.exec.split(";")
        if args.book:
            yant_obj.find(args.keyword, args.book, 
                          "book", args.whole_word, exec_cmd)
        else:
            # if no -b/-t provided, use "-t all"
            yant_obj.find(args.keyword, args.tag, 
                          "tag", args.whole_word, exec_cmd)

    elif args.sub_command == "review":
        exec_cmd = []
        if args.exec:
            exec_cmd = args.exec.split(";")
        if args.tag:
            yant_obj.review(args.tag, "tag", exec_cmd)
        else:
            yant_obj.review(args.book, "book", exec_cmd)

    elif args.sub_command == "fortune":
        if args.tag:
            yant_obj.fortune(args.tag, "tag")
        else:
            yant_obj.fortune(args.book, "book")

if __name__ == "__main__":
    main(sys.argv)
    #try:
    #    main(sys.argv)
    #except Exception as e:
    #    print("Error:", e)
