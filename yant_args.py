import argparse

def parse(args):
    parser = argparse.ArgumentParser(prog="yant")
    subparsers = parser.add_subparsers(dest="sub_command")

    parser_create = subparsers.add_parser("create", help="create a book (with tags)")
    help_msg = "Name of the new book"
    parser_create.add_argument("-b", "--book", required=True, help=help_msg)
    help_msg = "A list of tag of the new book, separated by comma"
    parser_create.add_argument("-t", "--tags", default="", help=help_msg)

    parser_add = subparsers.add_parser("add", help="Add a new note or command to book")
    parser_add.add_argument("note", metavar="note", help="title of the new note")
    parser_add.add_argument("-b", "--book", default="scratchpad", help="book name")
    parser_add.add_argument("-c", "--cmd", metavar="command",
                           help="command to be added (not implemented yet)")
                             
    parser_del = subparsers.add_parser("delete", aliases=["del", "rm"], \
                           help="delete note, tags or command from book")
    parser_del.add_argument("-b", "--book", default="scratchpad", help="book name")
    parser_del.add_argument("note", help="title of the new note")
    parser_del.add_argument("-c", "--cmd", metavar="command", help="command to be deleted")

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
    help_msg = "list by book name if True, otherwise list by tag names"
    parser_show.add_argument("-b", dest="use_tag", action="store_false", help=help_msg)
    parser_show.add_argument("target", nargs="?", default="all", help="name(s) of the book of tags")
    
    parser_find = subparsers.add_parser("find", aliases=["search"], help="find keywords in books")
    parser_find.add_argument("keyword", help="keyword for search, support wild character")
    help_msg = "find by book name if True, otherwise find by tag names"
    parser_find.add_argument("-b", dest="use_tag", action="store_false", help=help_msg)
    parser_find.add_argument("target", nargs="?", default="all", help="name(s) of the book of tags")

    parser_review = subparsers.add_parser("review", help="randomly review notes")
    help_msg = "review by book name if True, otherwise review by tag names"
    parser_review.add_argument("-b", dest="use_tag", action="store_false", help=help_msg)
    parser_review.add_argument("target", nargs="?", default="all", help="name(s) of the book of tags")

    parser_fortune = subparsers.add_parser("fortune", help="fortune cookie")
    help_msg = "fortune by book name if True, otherwise fortune by tag names"
    parser_fortune.add_argument("-b", dest="use_tag", action="store_false", help=help_msg)
    parser_fortune.add_argument("target", nargs="?", default="all", help="name(s) of the book of tags")

    parser_import = subparsers.add_parser("import", help="import notes from file")
    parser_import.add_argument("-b", "--book", required=True, help="book name")
    parser_import.add_argument("--file", required=True, help="file to import from")

    parser_export = subparsers.add_parser("export", help="export notes to file")
    parser_export.add_argument("-b", "--book", required=True, help="book name")
    parser_export.add_argument("--file", default="-", help="exporting file, stdout by default")

    return parser.parse_args(args)
