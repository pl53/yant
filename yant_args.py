import argparse

def parse(args):
    parser = argparse.ArgumentParser(prog="yant")
    subparsers = parser.add_subparsers(dest="cmd")

    parser_create = subparsers.add_parser("create", help="create a book (with tags)")
    parser_create.add_argument("-b", "--book", metavar="book",
                               required=True, help="name of the new book")

    parser_add = subparsers.add_parser("add", help="add a new note, tag or command to book")
    parser_add.add_argument("-b", "--book", metavar="book", required=True, help="book name")
    group_add = parser_add.add_mutually_exclusive_group(required=True)
    group_add.add_argument("-n", metavar="note", \
                           help="note to be added, use @# as delimiter")
    group_add.add_argument("-t", metavar="tag", help="tag to be added")
    group_add.add_argument("-c", metavar="command", help="command to be added")
                             
    parser_del = subparsers.add_parser("delete", aliases=["del", "rm"], \
                           help="delete note, tag or command from book")
    parser_del.add_argument("-b", "--book", metavar="book", required=True, help="book name")
    group_del = parser_del.add_mutually_exclusive_group(required=True)
    group_del.add_argument("-n", metavar="note_title", \
                           help="title of the note to be deleted")
    group_del.add_argument("-t", metavar="tag", help="tag to be deleted")
    group_del.add_argument("-c", metavar="command", help="command to be deleted")

    parser_up = subparsers.add_parser("update", aliases=["up"], \
                           help="update note, tag or command to book")
    parser_up.add_argument("-b", "--book", metavar="book", required=True, help="book name")
    parser_up.add_argument("-n", metavar="note", \
                           help="update a note, if note contains @#, do replace")
    
    parser_show = subparsers.add_parser("list", help="list books by name or tag")
    group_show = parser_show.add_mutually_exclusive_group()
    group_show.add_argument("-b", "--book", metavar="book", help="book name")
    group_show.add_argument("-t", "--tag", metavar="tag", help="tag name")
    parser_show.add_argument("--detail", action="store_true", \
                             help="show details of book and/or tag")
    
    parser_find = subparsers.add_parser("find", help="find keywords in books")
    parser_find.add_argument("keyword", \
                             help="keyword for search, support wild character")
    group_find = parser_find.add_mutually_exclusive_group()
    group_find.add_argument("-b", "--book", metavar="book", help="book name")
    group_find.add_argument("-t", "--tag", metavar="tag", help="tag name")

    parser_review = subparsers.add_parser("review", help="randomly review notes")
    group_review = parser_review.add_mutually_exclusive_group()
    group_review.add_argument("-b", "--book", metavar="book", help="book name")
    group_review.add_argument("-t", "--tag", metavar="tag", help="tag name")

    parser_fortune = subparsers.add_parser("fortune", help="fortune cookie")
    group_fortune = parser_fortune.add_mutually_exclusive_group()
    group_fortune.add_argument("-b", "--book", metavar="book", help="book name")
    group_fortune.add_argument("-t", "--tag", metavar="tag", help="tag name")

    #parser_fortune = subparsers.add_parser("help", help="help message")
    return parser.parse_args(args)
