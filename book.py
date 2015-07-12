import entry
import pickle
import sys
import re
import subprocess
import random
import yant_utils
from contextlib import contextmanager
from colors import colors
colored = colors.colored

@contextmanager
def open_book(obj):
    try: 
        with open(obj.filename, "rb") as fp: # "with" cannot handle excpetion here
            data = pickle.load(fp)
            obj.data = data
    except (OSError, IOError) as e:
        sys.stderr.write("Notebook not found.\n")
        sys.exit(1)
    except pickle.PickleError as e:
        sys.stderr.write("Couldn't load notebook data. \
                          Please make sure data in correct format.\n")
        sys.exit(1)

    yield

    try: 
        with open(obj.filename, "wb") as fp:
            pickle.dump(obj.data, fp) 
    except pickle.PicklingError as e:
        sys.stderr.write("Unable to store data.\n")

# no write back
def _read_data(func):
    def inner(obj, *args):
        with open(obj.filename, "rb") as fp:
            obj.data = pickle.load(fp)
        val = func(obj, *args)
        return val
    return inner

def store_data(data, filename):
    with open(filename, "wb") as fp:
        pickle.dump(data, fp)

''' notebook of English notes
'''
class Notebook:
    # used for import/export
    attr_delim = "+" * 20 + "\n" # delimitter of book attributes
    note_delim = "-" * 20 + "\n"
    sdelim = ": "
    attr_keys = ["name", "tags", "desc", "ctime", "mtime", \
                 "reserved_property_1", "reserved_property_2", "entries"]
    attr_desc = ["Notebook name", \
                 "Tags", \
                 "Notebook description", \
                 "Created time", \
                 "Last updated time", \
                 "Reserved property 1", \
                 "Reserved property 2", \
                 "Note entries"]

    def __init__(self, file_name, note_class):
        self.filename = file_name
        self.note_class = note_class
        self.book_name = self.filename.split("/")[-1][:-3]
        if not re.match("[a-zA-Z0-9_-]+", self.book_name):
            raise Exception("Illegal book name "+self.book_name + "Book name " +
                "should consist of only letters, numbers, dash, and underscore.") 

    def create_book(self, desc="No description", tags=["all"]):
        with open(self.filename, "wb") as fp:
            data = {}
            current_time = time.ctime()
            data["name"] = self.book_name
            data["tags"] = tags
            data["desc"] = desc
            data["ctime"] = current_time # create time
            data["mtime"] = current_time # modifited time
            data["reserved_property_1"] = None
            data["reserved_property_2"] = None
            data["entries"] = {}
            pickle.dump(data, fp)

    def save_book(self):
        store_data(self.data, self.filename)

    def add_tag(self, new_tag):    
        if not re.match("[a-zA-Z0-9_-]+", new_tag):
            raise Exception("Book tag could be only letters, numbers, -, and _.") 
        with open_book(self):
            if new_tag in self.data["tags"]:
                print("Tag", new_tag, "already exists.")
            else:
                self.data["tags"].append(new_tag)

    def delete_tag(self, tag):
        with open_book(self):
            try:
                self.data["tags"].remove(tag.lower())
            except ValueError:
                print("Tag", tag, "doesn't exist.")

    def update_desc(self, desc):
        with open_book(self):
            self.data["desc"] = desc

    def add_note(self, raw_key, note_class):
        key = raw_key.strip()
        with open_book(self):
            if key not in self.data["entries"]:
                self.data["entries"][key] = note_class(key)
            self.data["entries"][key].append_notes()
            print("One record added/updated.")

    def update_note(self, raw_key):
        key = raw_key.strip()
        with open_book(self):
            if key in self.data["entries"]:
                rv = self.data["entries"][key].update_notes()
                if rv == 0:
                    print("Record updated, updated user notes:") 
                    self.data["entries"][key].show_note()
                else:
                    print("Record not updated.")
            else:
                print("Warning: {} not in the book".format(key))

    def delete_note(self, raw_key):
        key = raw_key.strip()
        with open_book(self):
            try:
                del self.data["entries"][key]
                print("Record deleted.")
            except KeyError as e:
                print("Nonexistent keyword " + key + ", skip.")
    @_read_data
    def get_description(self):
        return self.data["desc"]

    @_read_data
    def set_description(self, desc=None):
        return self.data["desc"]

    @_read_data
    def get_note_count(self):
        return len(self.data["entries"])

    @_read_data
    def get_tags(self):
        return self.data["tags"]

    def add_tag(self, tag):
        with open_book(self):
            if tag in self.data["tags"]:
                self.logger.warn("tag already exists. skip.")
            else:
                self.data["tags"].append(tag)
                self.logger.info("tag {0} added.".format(tag))

    def delelte_tag(self, tag):
        with open_book(self):
            if tag in self.data["tags"]:
                self.logger.warn("tag already exists. skip.")
            else:
                self.data["tags"].remove(tag)
                self.logger.info("tag {0} deleted.".format(tag))

    @_read_data
    def search_notes(self, pattern):
        pattern = pattern.lower().strip()
        result = []
        prog = re.compile(pattern)
        with open_book(self):
            for e in self.data["entries"]:
                for w in self.data["entries"][e].__str__().split():
                     # 'search' instead of 'match' to find anywhere in string
                    if prog.search(w):
                        result.append(self.data["entries"][e])
                        break
        return result

    def random_review(self, random_indices=[]):
        review_cnt = 0 
        with open_book(self):
            if random_indices == []: # review all entries
                random_indices = list(range(len(self.data["entries"])))
                random.shuffle(random_indices)
            keys = list(self.data["entries"].keys())
            total_cnt = len(keys)
            for ri in random_indices:
                try:
                    e = self.data["entries"][keys[ri]]
                    print("Remember this note? ===========> ", end="")
                    e.show_key()
                    cmd = input("Press {} to see the notes => ".\
                                format(colored("Enter", "c"))) # just to continue
                    e.show_note()
                    cmd = input(("Delete({0}), Update({1}), Quit({2}), or " + \
                                 "Next(<{3}>)=> ").format(colored('d', 'y'), \
                                 colored("u", "y"), colored('q', 'y'), \
                                 colored('Enter', 'y'))) 
                    if cmd in "dD":
                        del self.data["entries"][keys[ri]]
                    else:
                        e.exec_cmd(cmd)
                    review_cnt += 1
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print("Review interrupted by", e)
                    raise

        #store_data(self.data, self.filename)
        return review_cnt
 
    @_read_data
    def export_book(self, raw_filename):
        dump_file = raw_filename.strip()
        print("Export the notebook to " + dump_file)
        with open(dump_file, "w") as fp:
            for idx, attr in enumerate(self.attr_keys):
                attr_desc = self.attr_desc[idx]
                if attr not in self.data:
                    print("Warning:", "no", attr_desc, "in data.")
                    continue
                if attr == "entries":
                    fp.write(attr_desc + ":", "see all entries below\n")
                    fp.write(self.note_delim)
                    for e in self.data[attr]:
                        fp.write(str(self.data[attr][e]))
                        fp.write(self.note_delim)
                elif attr == "tags":
                    fp.write(attr_desc + self.sdelim + ",".join(self.data[attr]))
                    fp.write("\n"+self.attr_delim)
                else:
                    fp.write(attr_desc + self.sdelim + self.data[attr])
                    fp.write("\n"+self.attr_delim)

    def import_book(self, raw_filename):
        src_file = raw_filename.strip()
        print("import notebook from " + src_file)
        with open_book(self): 
            with open(src_file, "r") as fp:
                raw_book = fp.read().split(self.attr_delim)
            for attr in raw_book:
                attr_lines = attr.split(self.note_delim)
                attr_desc, attr_value = attr_lines[0].split(self.sdelim)
                try:
                    attr = self.attr_keys[self.attr_desc.index(attr_desc)]
                except:
                    print("Warning: illegal book attribute", attr_desc, "ignore.")
                    continue
                if attr == "entries":
                    if attr not in self.data:
                        self.data[attr] = {}
                    try:
                        raw_notes = attr_lines[1:]
                        for note_str in raw_notes:
                             if note_str == '':
                                 continue
                             note = note_str.strip().split('\n')
                             new_note = self.note_class(note[0], note[1:])
                             # note[0] is key
                             self.data["entries"][note[0]] = new_note 
                    except:
                        sys.stderr.write("Error during importing process.\n")
                elif attr == "tags":
                    self.data[attr] = attr_value.split(",")
                else:
                    self.data[attr] = attr_value 

    @_read_data
    def pick_random_note(self):
        key_list = list(self.data["entries"].keys())
        if key_list != []:
            random_key = random.choice(key_list)
            return self.data["entries"][random_key]
        else:
            return None

    @_read_data
    def randomize_notes(self):
        random.shuffle(self.data["entries"])
        return self.data["entries"]

    @_read_data
    def __iter__(self):
            self.index = -1
            return self

    def __next__(self):
        try:
            self.index += 1
            key = self.keys[self.index]
            return self.data["entries"][key]
        except IndexError as e:
            with open(self.filename, "wb") as fp:
                pickle.dump(self.data, fp)
            raise StopIteration

#TODO: make this a singleton
class TagManager:
        
    def __init__(self):
        data_path = yant_utils.get_data_path()
        self.filename = os.path.join(note_path, "tag.data")
        self.logger = logging.getLogger(self)
        try:
            self.load_tag()
        except:
            self.logger.warn("Cannot load tags, will create a new tag file")
            all_books = yant_utils.get_booklist(data_path)
            self.data = {"all":all_books}
            self.dump_tag()

    def __str__(self):
        return "TagManager"

    def load_tag(self):
        with open(self.filename, "rb") as tag_fp: 
            self.data = pickle.load(tag_fp)

    def dump_tag(self):
        with open(self.filename, "wb") as tag_fp:
            pickle.dump(self.data, tag_fp)

    def get_tags(self):
        return list(self.data.keys())

    def get_books(self, tag):
        if tag not in self.data:
            self.logger.warn("tag {0} doesn't exist.".format(tag))
            return []
        else:
            return self.data[tag]

    def get_mapping(self):
        return self.data

    def add_tag(self, tag, book):
        try:
            if tag not in self.data:
                self.data[tag] = [book]
                self.dump_tag()
            elif book not in self.data:
                self.data[tag].append(book)
                self.dump_tag()
            else:
                self.logger.error(book + " already has tag " + tag + ". skip.")
        except:
             self.logger.error("attaching tag to book failed.")

    def delete_tag(self, tag, book):
        try:
            if tag not in self.data:
                self.logger.error("tag {0} doesn't exist.".format(tag))
            elif book not in self.data[tag]:
                self.logger.error(book + " doesn't have the tag " + tag + ".")
            else:
                self.data[tag].remove(book)
                self.dump_tag()
        except:
            self.logger.error("deleting tag from book failed.")
