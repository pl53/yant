import entry
import pickle
import sys
import re
import subprocess
import random
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
def read_book(func):
    def inner(obj, *args):
        with open(obj.filename, "rb") as fp:
            #obj.desc, obj.entries = pickle.load(fp)
            obj.data = pickle.load(fp)
        val = func(obj, *args)
        return val
    return inner

''' notebook of English entries
'''
class Notebook:
    # used for import/export
    attr_delim = "+" * 20 + "\n" # delimitter of book attributes
    entry_delim = "-" * 20 + "\n"
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

    def __init__(self, file_name, entry_type):
        self.filename = file_name
        self.entry_type = entry_type
        self.book_name = self.filename.split("/")[-1][:-3]
        if not re.match("[a-zA-Z0-9_-]+", self.book_name):
            raise Exception("Illegal book name "+self.book_name + "Book name " +
                "should consist of only letters, numbers, dash, and underscore.") 

    def create_book(self, desc, tags=["all"]):
        with open(self.filename, "wb") as fp:
            data = {}
            current_time = time.ctime()
            data["name"] = self.book_name
            data["tags"] = tags
            data["desc"] = desc
            data["ctime"] = current_time # create time
            data["mtime"] = current_time # modifited time
            data["reserved_property_1"] = "None"
            data["reserved_property_2"] = "None"
            data["entries"] = {}
            pickle.dump(data, fp)

    def add_tag(self, new_tag):    
        if not re.match("[a-zA-Z0-9_-]+", new_tag):
            raise Exception("Book tag could be only letters, numbers, -, and _.") 
        with open_book(self):
            if new_tag.lower() in self.data["tags"]:
                print("Tag", new_tag, "already exists.")
            else:
                self.data["tags"].append(new_tag.lower())

    def delete_tag(self, tag):
        if not re.match("[a-zA-Z0-9_-]+", new_tag):
            raise Exception("Book tag could be only letters, numbers, -, and _.") 
        with open_book(self):
            try:
                self.data["tags"].remove(tag.lower())
            except ValueError:
                print("Tag", tag, "doesn't exist.")

    def update_desc(self, desc):
        with open_book(self):
            self.data["desc"] = desc

    def add_entry(self, raw_key, entry_type):
        key = raw_key.strip()
        with open_book(self):
            if key not in self.data["entries"]:
                self.data["entries"][key] = entry_type(key)
            self.data["entries"][key].append_notes()
            print("One record added/updated.")

    def update_entry(self, raw_key):
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

    def delete_entry(self, raw_key):
        key = raw_key.strip()
        with open_book(self):
            try:
                del self.data["entries"][key]
                print("Record deleted.")
            except KeyError as e:
                print("Nonexistent keyword " + key + ", skip.")
    @read_book
    def description(self):
        print(self.data["desc"])

    @read_book
    def get_entry_count(self):
        return len(self.data["entries"])

    @read_book
    def search_entries(self, pattern):
        pattern = pattern.lower().strip()
        result = []
        prog = re.compile(pattern)
        with open_book(self):
            for e in self.data["entries"]:
                for w in self.data["entries"][e].__str__().split():
                    if prog.match(w.strip("\"\'")): # match found
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
                    review_cnt += 1
                    print("Remember this note? ===========> ", end="")
                    e.show_key()
                    cmd = input("Press {} to see the notes => ".\
                                format(colored("Enter", "c"))) # just to continue
                    e.show_note()
                    cmd = input(("Delete({0}), Update({1}), Quit({2}), or " + \
                                 "Next(<{3}>)=> ").format(colored('d', 'y'), \
                                 colored("u", "y"), colored('q', 'y'), \
                                 colored('Enter', 'y'))) 
                    e.exec_cmd(cmd)
                except (KeyboardInterrupt, entry.EntryExcept, IndexError) as e:
                    print("Review interrupted by", e)
                    rval = 1
                    break
            else:
                rval = 0
        return rval   
 
    @read_book
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
                    fp.write(attr_desc + ": see all entries below.\n")
                    fp.write(self.entry_delim)
                    for e in self.data[attr]:
                        fp.write(str(self.data[attr][e]))
                        fp.write(self.entry_delim)
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
                attr_lines = attr.split(self.entry_delim)
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
                             new_entry = self.entry_type(note[0], note[1:])
                             # note[0] is key
                             self.data["entries"][note[0]] = new_entry 
                    except:
                        sys.stderr.write("Error during importing process.\n")
                elif attr == "tags":
                    self.data[attr] = attr_value.split(",")
                else:
                    self.data[attr] = attr_value 

    @read_book
    def pick_random_entry(self):
        key_list = list(self.data["entries"].keys())
        if key_list != []:
            random_key = random.choice(key_list)
            return self.data["entries"][random_key]
        else:
            return None

    @read_book
    def randomize_entries(self):
        random.shuffle(self.data["entries"])
        return self.data["entries"]

    @read_book
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


#    def open(self):
#        if self.opened == True:
#            return
#        try:
#            with open(self.filename, "rb") as fp:
#                self.data["entries"] = pickle.load(fp)
#                #self.keys = list(self.data["entries"].keys())
#                #random.seed()
#                #random.shuffle(self.keys)
#                #return self.data["entries"]
#        except pickle.PickleError as e:
#            print("unable to read notebook")
#        self.opened = True
#
#    def close(self):
#        if self.opened == False:
#            # add exception later
#            print("Error: notebook not opened.")
#            return
#        try:
#            with open(self.filename, "wb") as fp:
#                #pickle.dump((self.data["entries"]), fp)
#                return pickle.dump(self.data["entries"], fp)
#        except pickle.PickleError as e:
#            print("unable to store entries to notebook")
#        self.opened = False
