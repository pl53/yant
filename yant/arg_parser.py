import argparse


def parse(args):
    yant_desc = "YANT is a commanline notebook tool.\n" + \
                "Each notebook is a collection of unordered flashcards.\n" + \
                "Each flashcard has a unique title and unlimited notes.\n" + \
                "Each notebook can be attached with unlimited tags.\n" + \
                "User can add/remove flashcards and tags.\n" + \
                "User can also search and randomly review flashcards by book or tag."
    parser = argparse.ArgumentParser(prog="yant", description=yant_desc)
    subparsers = parser.add_subparsers(dest="sub_command")

    parser_create = subparsers.add_parser("create", help="Create a new book")
    help_msg = "Name of the new book"
    parser_create.add_argument("-b", "--book", required=True, help=help_msg)
    help_msg = "A list of tag of the new book, separated by semicolon."
    parser_create.add_argument("-t", "--tags", default="", help=help_msg)
    parser_create.add_argument("--desc", default="Yant book.", \
                               help="Book description")

    parser_destroy = subparsers.add_parser("destroy", help="Destroy a book")
    help_msg = "Name of the book"
    parser_destroy.add_argument("-b", "--book", required=True, help=help_msg)

    book_name_help_msg = "book name, use default 'scratchpad' if not specified"

    parser_add = subparsers.add_parser("add", help="Add a new flashcard")
    parser_add.add_argument("title", metavar="title", help="title of the new flashcard")
    parser_add.add_argument("--notes", help="notes separated by semicolons")
    parser_add.add_argument("-b", "--book", default="scratchpad", help=book_name_help_msg)
                             
    parser_append = subparsers.add_parser("append", help="Append new notes to an existing flashcard")
    key_title = parser_append.add_mutually_exclusive_group(required=True)
    key_title.add_argument("-k", dest='key', help="hashkey of the flashcard")
    key_title.add_argument("-t", dest='title', help="title of the flashcard")
    parser_append.add_argument("--notes", help="notes separated by semicolons")
    parser_append.add_argument("-b", "--book", default="scratchpad", help=book_name_help_msg)
                             
    parser_rm = subparsers.add_parser("remove", aliases=["rm", "delete", "del"], \
                           help="Remove flashcard from book")
    key_title = parser_rm.add_mutually_exclusive_group(required=True)
    key_title.add_argument("-k", dest='key', help="hashkey of the flashcard")
    key_title.add_argument("-t", dest='title', help="title of the flashcard")
    parser_rm.add_argument("-b", "--book", default="scratchpad", help=book_name_help_msg)

    parser_up = subparsers.add_parser("update", aliases=["up"], \
                                      help="Update a flashcard")
    key_title = parser_up.add_mutually_exclusive_group(required=True)
    key_title.add_argument("-k", dest='key', help="hashkey of the flashcard")
    key_title.add_argument("-t", dest='title', help="title of the flashcard")
    parser_up.add_argument("-b", "--book", default="scratchpad", help=book_name_help_msg)
    
    parser_tag = subparsers.add_parser("tag", help="Add or remove tags to/from a book")
    parser_tag.add_argument("-d", dest="delete_tags", action="store_true",
                            help="delete the tags if option is speficified")
    parser_tag.add_argument("tags", help="a list of tags separated by ';'")
    parser_tag.add_argument("-b", "--book", required=True, help="book name")

    parser_show = subparsers.add_parser("list", aliases=["lst", "show"],
                                        help="List books by name or tags")
    show_dest = parser_show.add_mutually_exclusive_group(required=False)
    show_dest.add_argument("-b", "--book", help="book name")
    show_dest.add_argument("-t", "--tag", default="all", help="tag name")
    
    parser_find = subparsers.add_parser("find", aliases=["search"], help="Find flashcards with the keyword")
    help_msg = "Select only those flashcards containing matches the whole word"
    parser_find.add_argument("-w", dest="whole_word", action="store_true", help=help_msg)
    parser_find.add_argument("keyword", help="keyword for search, support wild character")
    find_dest = parser_find.add_mutually_exclusive_group(required=False)
    find_dest.add_argument("-b", "--book", help="book name")
    find_dest.add_argument("-t", "--tag", default="all", help="tag name")
    parser_find.add_argument("--exec", help="command executed on each node, use {0} for flashcard title, \
                             {i} for note #i, {+} for all notes.")

    parser_review = subparsers.add_parser("review", help="Randomly review flashcards")
    review_dest = parser_review.add_mutually_exclusive_group(required=True)
    review_dest.add_argument("-b", "--book", help="book name")
    review_dest.add_argument("-t", "--tag", help="tag name")
    parser_review.add_argument("--exec", help="command executed on each node, use {0} for flashcard title, \
                             {i} for note #i, {+} for all notes.")

    parser_fortune = subparsers.add_parser("fortune", help="Fortune cookie")
    fortune_dest = parser_fortune.add_mutually_exclusive_group(required=False)
    fortune_dest.add_argument("-b", "--book", help="book name")
    fortune_dest.add_argument("-t", "--tag", default="all", help="tag name")

    parser_import = subparsers.add_parser("import", help="Import flashcards from a file")
    parser_import.add_argument("-b", "--book", required=True, help="book name")
    parser_import.add_argument("--file", required=True, help="file to import from")

    parser_export = subparsers.add_parser("export", help="Export flashcards to a file")
    parser_export.add_argument("-b", "--book", required=True, help="book name")
    parser_export.add_argument("--file", default="-", help="exporting file, stdout by default")

    return parser.parse_args(args)
