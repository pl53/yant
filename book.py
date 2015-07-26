import pickle
import os
import sys
import re
import subprocess
import random
from contextlib import contextmanager

import entry
import yant_utils
from colors import colors
colored = colors.colored

''' A decorator for read/write data;
    @data must be mutable.
'''
@contextmanager
def open_book(data_file, data):
    try: 
        with open(data_file, "rb") as fp: # "with" cannot handle excpetion here
            data = pickle.load(fp)
    except (OSError, IOError) as e:
        sys.stderr.write("File not found.\n")
        sys.exit(1)
    except pickle.PickleError as e:
        sys.stderr.write("Cannot load data.\n")
        sys.exit(1)

    yield

    try: 
        with open(data_file, "wb") as fp:
            pickle.dump(data, fp) 
    except pickle.PicklingError as e:
        sys.stderr.write("Cannot store data.\n")

''' 
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

    def __init__(self, book_name, note_class):
        self.data_file = os.path.join(yant_utils.get_data_path(),
                                     book_name+".db")
        self.note_class = note_class
        #self.book_name = self.data_file.split("/")[-1][:-3]
        self.book_name = book_name

    def create_book(self, desc="No description", tags=["all"]):
        with open(self.data_file, "wb") as fp:
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

    def load_book(self):
        with open(self.data_file, "rb") as fp:
            self.data = pickle.load(fp)

    def save_book(self):
        with open(self.data_file, "wb") as fp:
            pickle.dump(self.data, fp)

    def show_detail(self):
        self.load_book()
        print("Name:", self.data["name"])
        print("Tags:", ", ".join(self.data["tags"]))
        print("Description:", self.data["desc"]) 
        print("Creation Time:", self.data["ctime"])
        print("Last Update:", self.data["mtime"]) 
        print("Other info.:", self.data["reserved_property_1"])
        print("Other info.:", self.data["reserved_property_2"])
        print("Total notes:", len(self.data["entries"]))

    def add_tag(self, new_tag):    
        with open_book(self.data_file, self.data):
            if new_tag in self.data["tags"]:
                print("Tag", new_tag, "already exists.")
            else:
                self.data["tags"].append(new_tag)

    def delete_tag(self, tag):
        with open_book(self.data_file, self.data):
            try:
                self.data["tags"].remove(tag.lower())
            except ValueError:
                print("Tag", tag, "doesn't exist.")

    def update_desc(self, desc):
        with open_book(self.data_file, self.data):
            self.data["desc"] = desc

    #TODO
    ''' Update the notebook with given note object and operation
    @note_obj: note object
    @op: r -- replace or add, m -- merge with existing note
    '''
    def update_note(self, note_obj, op="r"):
        key = note_obj.key
        with open_book(self.data_file, self.data):
            if op == 'r':
                self.data["entries"][key] = note_obj
            elif op == 'm':
                if key in self.data["entries"]:
                    self.data["entries"][key].merge(note_obj)
                else:
                    pass ##TODO       
            else:
                raise Exception("Unkown note update operation")
            print("One record added/updated.")

    def update_note(self, raw_key):
        key = raw_key.strip()
        with open_book(self.name, self.data):
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
        with open_book(self.data_file, self.data):
            try:
                del self.data["entries"][key]
                print("Record deleted.")
            except KeyError as e:
                print("Nonexistent keyword " + key + ", skip.")

    def get_description(self):
        self.load_book()
        return self.data["desc"]

    def set_description(self, desc=None):
        self.load_book()
        return self.data["desc"]

    def get_note_count(self):
        self.load_book()
        return len(self.data["entries"])

    def get_tags(self):
        self.load_book()
        return self.data["tags"]

    def add_tag(self, tag):
        with open_book(self.data_file, self.data):
            if tag in self.data["tags"]:
                self.logger.warn("tag already exists. skip.")
            else:
                self.data["tags"].append(tag)
                self.logger.info("tag {0} added.".format(tag))

    def delelte_tag(self, tag):
        with open_book(self.data_file, self.data):
            if tag in self.data["tags"]:
                self.logger.warn("tag already exists. skip.")
            else:
                self.data["tags"].remove(tag)
                self.logger.info("tag {0} deleted.".format(tag))

    def search_notes(self, pattern):
        pattern = pattern.lower().strip()
        result = []
        prog = re.compile(pattern)
        with open_book(self.data_file, self.data):
            for e in self.data["entries"]:
                for w in self.data["entries"][e].__str__().split():
                    # 'search' instead of 'match' to find anywhere in string
                    if prog.search(w):
                        result.append(self.data["entries"][e])
                        break
        return result

    def random_review(self, random_indices=[]):
        review_cnt = 0 
        with open_book(self.data_file, self.data):
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

        #store_data(self.data, self.data_file)
        return review_cnt
 
    def export_book(self, raw_data_file):
        dump_file = raw_data_file.strip()
        print("Export the notebook to " + dump_file)
        self.load_book()
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

    def import_book(self, raw_data_file):
        src_file = raw_data_file.strip()
        print("import notebook from " + src_file)
        with open_book(self.data_file, self.data):
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

    def pick_random_note(self):
        self.load_book()
        key_list = list(self.data["entries"].keys())
        if key_list != []:
            random_key = random.choice(key_list)
            return self.data["entries"][random_key]
        else:
            return None

    def randomize_notes(self):
        self.load_book()
        random.shuffle(self.data["entries"])
        return self.data["entries"]

    def __iter__(self):
        self.load_book()
        self.index = -1
        return self

    def __next__(self):
        try:
            self.index += 1
            key = self.keys[self.index]
            return self.data["entries"][key]
        except IndexError as e:
            with open(self.data_file, "wb") as fp:
                pickle.dump(self.data, fp)
            raise StopIteration

