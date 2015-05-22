import argparse

def parse(args):
    parser = argparse.ArgumentParser(prog="yant")
    subparsers = parser.add_subparsers(dest="cmd")

    parser_create = subparsers.add_parser("create", help="create a book or tag")
    group_create = parser_create.add_mutually_exclusive_group(required=True)
    group_create.add_argument("-b", "--book", help="name of the new book")
    group_create.add_argument("-t", "--tag", help="new of the new tag")

    parser_add = subparsers.add_parser("add", \
                    help="add a new note, tag or command to book")
    parser_add.add_argument("book_name", metavar="book", \
                            help="name of the book")
    group_add = parser_add.add_mutually_exclusive_group(required=True)
    group_add.add_argument("-n", metavar="note", \
                           help="add a new note, use @# as delimiter")
    group_add.add_argument("-t", metavar="tags", nargs="+", help="add new tags")
    group_add.add_argument("-c", metavar="command", help="add a new command")
                             
    parser_del = subparsers.add_parser("delete", aliases=["del", "rm"], \
                           help="delete note, tag or command from book")
    parser_del.add_argument("book_name", metavar="book", \
                           help="name of the book")
    group_del = parser_del.add_mutually_exclusive_group(required=True)
    group_del.add_argument("-n", metavar="note_title", \
                           help="delete a note according to title")
    group_del.add_argument("-t", metavar="tags", nargs="+", \
                           help="delete tags")
    group_del.add_argument("-c", metavar="command", help="delete a command")

    parser_up = subparsers.add_parser("update", aliases=["up"], \
                           help="update note, tag or command to book")
    parser_up.add_argument("book_name", metavar="book", help="name of the book")
    parser_up.add_argument("-n", metavar="note", \
                           help="update a note, if note contains @#, do replace")
    
    parser_show = subparsers.add_parser("show", help="show books or tags")
    group_show = parser_show.add_mutually_exclusive_group()
    group_show.add_argument("-b", "--book", help="name of the book")
    group_show.add_argument("-t", "--tag", help="new of the tag")
    parser_show.add_argument("--detail", action="store_true", \
                        help="show details of book and/or tag")
    
    parser_find = subparsers.add_parser("find", help="find keywords in books")
    parser_find.add_argument("keyword", help="support wild character")
    group_find = parser_find.add_mutually_exclusive_group()
    group_find.add_argument("-b", "--book", help="name of the book")
    group_find.add_argument("-t", "--tag", help="new of the tag")

    parser_review = subparsers.add_parser("review", help="randomly review notes")
    group_review = parser_review.add_mutually_exclusive_group()
    group_review.add_argument("-b", "--book", help="name of the book")
    group_review.add_argument("-t", "--tag", help="new of the tag")

    parser_fortune = subparsers.add_parser("fortune", help="fortune cookie")
    group_fortune = parser_fortune.add_mutually_exclusive_group()
    group_fortune.add_argument("-b", "--book", help="name of the book")
    group_fortune.add_argument("-t", "--tag", help="new of the tag")
