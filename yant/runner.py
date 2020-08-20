#!/usr/bin/env python3

import os
import sys
import logging

from yant.model.flashcard import Flashcard
from yant import arg_parser
from yant.utils import utils, yant_utils
from yant.model.yant import Yant
from yant.utils import colors
colored = colors.Colors.colored


def main(argv):

    utils.require_python_version(3) # major version should be 3
    args = arg_parser.parse(argv[1:])
    if not args.sub_command:
        raise Exception("No command provided. Use '-h' to see available commands.")
    log_file = os.path.join(yant_utils.get_data_path(), "yant.log")
    logging.basicConfig(filename=log_file, level=logging.INFO)
    logger = logging.getLogger("Yant")
    logger.debug("Yant starts.")

    # valid_name_pattern =  "^[a-zA-Z][a-zA-Z0-9_-]*$"

    yant_obj = Yant(Flashcard)
    logger.setLevel(logging.ERROR)
    if not yant_obj.exist_book("scratchpad"):
        yant_obj.create_book(
            book = "scratchpad",\
            tags=["all"],\
            description="The default notebook used when a book is not specified")
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
        if args.tags:
            tags = args.tags.split(';')
        else:
            tags = []
        yant_obj.create_book(args.book, tags, args.desc)
        print("Book " + colored(args.book, "b") + " created.")

    elif args.sub_command == "destroy":
        print("Warning: your are deleting book '" + colored(args.book, "b") +\
              "', which is unrecoverable!")
        confirm = input("Are your sure? (Y/N): ")
        if confirm in "Yy":
            yant_obj.destroy_book(args.book)     
        print("Book '" + colored(args.book, "b") + " deleted.")

    elif args.sub_command == "add":
        if args.notes:
            notes = args.notes.split(';');
            need_prompted_notes = False
        else:
            notes = []
            need_prompted_notes = True
        key = yant_obj.add_flashcard(args.book, args.title, notes, need_prompted_notes)
        print("Flashcard added to book '" + args.book + "'. Key is " + key + '.')

    elif args.sub_command == "append":
        if args.notes:
            notes = args.notes.split(';');
        else:
            notes = []
        if args.key:
            yant_obj.append_flashcard_by_key(args.book, args.key, args.notes)
        else:
            yant_obj.append_flashcard_by_title(args.book, args.title, args.notes)
        print("Flashcard appended.")

    elif args.sub_command in ["update", "up"]:
        if args.key:
            yant_obj.update_flashcard_by_key(args.book, args.key)
        else:
            yant_obj.update_flashcard_by_title(args.book, args.title)

    elif args.sub_command in ["remove", "rm", "delete", "del"]:
        if args.key:
            yant_obj.remove_flashcard_by_key(args.book, args.key)
        else:
            yant_obj.remove_flashcard_by_title(args.book, args.title)

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
        if args.book:
            yant_obj.fortune(args.book, "book")
        else:
            yant_obj.fortune(args.tag, "tag")


if __name__ == "__main__":
    main(sys.argv)
