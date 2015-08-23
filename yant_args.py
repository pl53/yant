import argparse

def parse(args):
    parser = argparse.ArgumentParser(prog="yant")
    subparsers = parser.add_subparsers(dest="sub_command")

    parser_create = subparsers.add_parser("create", help="create a book (with tags)")
    help_msg = "Name of the new book"
    parser_create.add_argument("-b", "--book", required=True, help=help_msg)
    help_msg = "A list of tag of the new book, separated by semicolon."
    parser_create.add_argument("-t", "--tags", default="", help=help_msg)
    parser_create.add_argument("--desc", default="Yant book.", \
                               help="Book description")

    parser_destroy = subparsers.add_parser("destroy", help="destroy a book")
    help_msg = "Name of the book"
    parser_destroy.add_argument("-b", "--book", required=True, help=help_msg)

    parser_add = subparsers.add_parser("add", help="Add a new note or command to book")
    parser_add.add_argument("note", metavar="note", help="title of the new note")
    parser_add.add_argument("-b", "--book", default="scratchpad", help="book name")
                             
    parser_rm = subparsers.add_parser("remove", aliases=["rm"], \
                           help="remove note from book")
    parser_rm.add_argument("-b", "--book", default="scratchpad", help="book name")
    parser_rm.add_argument("note", help="title of the new note")
    #parser_rm.add_argument("-c", "--cmd", metavar="command", help="command to be deleted")

    parser_up = subparsers.add_parser("update", aliases=["up"], \
                           help="update note, tags or command to book")
    parser_up.add_argument("-b", "--book", default="scratchpad", help="book name")
    parser_up.add_argument("note", help="update a note, if note contains @#, do replace")
    
    parser_tag = subparsers.add_parser("tag", help="Add or remove tags to/from a book")
    parser_tag.add_argument("-d", dest="delete_tags", action="store_true",
                            help="If true, delete the tags")
    parser_tag.add_argument("tags", help="A list of tags")
    parser_tag.add_argument("-b", "--book", required=True, help="book name")

    parser_show = subparsers.add_parser("list", aliases=["lst", "show"],
                                        help="list books by name or tags")
    show_dest = parser_show.add_mutually_exclusive_group(required=False)
    show_dest.add_argument("-b", "--book", help="book name")
    show_dest.add_argument("-t", "--tag", default="all", help="tag name")
    
    parser_find = subparsers.add_parser("find", aliases=["search"], help="find keywords in books")
    help_msg = "Select only those notes containing matches the whole word"
    parser_find.add_argument("-w", dest="whole_word", action="store_true", help=help_msg)
    parser_find.add_argument("keyword", help="keyword for search, support wild character")
    find_dest = parser_find.add_mutually_exclusive_group(required=False)
    find_dest.add_argument("-b", "--book", help="book name")
    find_dest.add_argument("-t", "--tag", default="all", help="tag name")
    parser_find.add_argument("--exec", help="Command executed on each note title")

    parser_review = subparsers.add_parser("review", help="randomly review notes")
    review_dest = parser_review.add_mutually_exclusive_group(required=True)
    review_dest.add_argument("-b", "--book", help="book name")
    review_dest.add_argument("-t", "--tag", help="tag name")
    parser_review.add_argument("--exec", help="Command executed on each note title")

    parser_fortune = subparsers.add_parser("fortune", help="fortune cookie")
    fortune_dest = parser_fortune.add_mutually_exclusive_group(required=False)
    fortune_dest.add_argument("-b", "--book", help="book name")
    fortune_dest.add_argument("-t", "--tag", help="tag name")

    parser_import = subparsers.add_parser("import", help="import notes from file")
    parser_import.add_argument("-b", "--book", required=True, help="book name")
    parser_import.add_argument("--file", required=True, help="file to import from")

    parser_export = subparsers.add_parser("export", help="export notes to file")
    parser_export.add_argument("-b", "--book", required=True, help="book name")
    parser_export.add_argument("--file", default="-", help="exporting file, stdout by default")

    return parser.parse_args(args)
