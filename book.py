import time
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
        self.book_name = book_name
        self.note_class = note_class
        self.data = {}
        self.data_file = os.path.join(
                             yant_utils.get_data_path(),
                             book_name+".db")
        self.is_data_loaded = False

    def create_book(self, tag="", desc="No description"):
        with open(self.data_file, "wb") as fp:
            data = {}
            current_time = time.ctime()
            data["name"] = self.book_name
            data["tags"] = ["all"]
            data["desc"] = desc
            data["ctime"] = current_time # create time
            data["mtime"] = current_time # modifited time
            data["reserved_property_1"] = None
            data["reserved_property_2"] = None
            data["entries"] = {}

            if tag != "" and tag != "all":
                data["tags"].append(tag)

            pickle.dump(data, fp)

    def load_book(self):
        if self.is_data_loaded:
            return
        with open(self.data_file, "rb") as fp:
            self.data = pickle.load(fp)
        self.is_data_loaded = True

    def save_book(self):
        if not self.is_data_loaded:
            raise Exception("Cannot save book: data not loaded.")
        with open(self.data_file, "wb") as fp:
            pickle.dump(self.data, fp)

    def show_detail(self):
        self.load_book()
        print("Name:", self.data["name"])
        print("Tags:", ", ".join(self.data["tags"]))
        print("Description:", self.data["desc"]) 
        print("Creation Time:", self.data["ctime"])
        print("Last Update:", self.data["mtime"]) 
        #print("Other info.:", self.data["reserved_property_1"])
        #print("Other info.:", self.data["reserved_property_2"])
        print("Total notes:", len(self.data["entries"]))

    def update_desc(self, desc):
        self.load_book()
        self.data["desc"] = desc
        self.update_mtime()
        self.save_book()

    '''Note related'''
    def get_note(self, key):
        return self.data["entries"].get(key, None)

    def get_note_count(self):
        return len(self.data["entries"])
            
    #TODO
    ''' Update the notebook with given note object
        Do a merge if title already in the book, otherwise do an add
    @note_obj: note object
    '''
    def add_note(self, note_obj):
        key = note_obj.key
        self.load_book()
        if key in self.data["entries"]:
            self.data["entries"][key].merge(note_obj)
        else:
            self.data["entries"][key] = note_obj
        self.update_mtime()
        print("One record added/updated.")
        self.save_book()

    def update_note(self, raw_key):
        key = raw_key.strip()
        self.load_book()
        if key in self.data["entries"]:
            rv = self.data["entries"][key].update()
            if rv == 0:
                print("Updated user notes:") 
                self.data["entries"][key].show_note()
            else:
                print("Note not updated.")
            self.update_mtime()
        else:
            print("Warning: {} not in the book".format(key))
        self.save_book()

    def delete_note(self, raw_key):
        key = raw_key.strip()
        self.load_book()
        try:
            self.data["entries"].pop(key)
            self.update_mtime()
            self.save_book()
            print("Note deleted.")
        except KeyError as e:
            print("Note title " + key +  "doesn't exist, skip.")

    def get_description(self):
        self.load_book()
        return self.data["desc"]

    def set_description(self, desc=None):
        self.load_book()
        return self.data["desc"]

    def get_note_count(self):
        self.load_book()
        return len(self.data["entries"])

    ''' tag related'''
    def add_tag(self, tag):    
        #new_tag = tag.strip()
        new_tag = tag
        self.load_book()
        if new_tag in self.data["tags"]:
            print("Tag {0} already exists.".format(new_tag))
        else:
            self.data["tags"].append(new_tag)
            print("Tag {0} added.".format(new_tag))
        self.update_mtime()
        self.save_book()

    def delete_tag(self, tag):
        self.load_book()
        try:
            self.data["tags"].remove(tag.lower())
            self.update_mtime()
            print("Tag {0} deleted from book.".format(tag))
        except ValueError:
            print("Book", self.book_name, "doesn't have tag", tag+".")
        self.save_book()

    def get_tags(self):
        self.load_book()
        return self.data["tags"]

    ''' time related'''
    def update_mtime(self):
        try:
            self.data["mtime"] = time.ctime()
        except:
            print("Unable to update mtime. Book not loaded?")

    def search_notes(self, pattern):
        pattern = pattern.strip()
        result = []
        prog = re.compile(pattern, re.IGNORECASE)
        self.load_book()
        for e in self.data["entries"]:
            # 'search' instead of 'match' to find anywhere in string
            if prog.search(self.data["entries"][e].__str__()):
                result.append(self.data["entries"][e])
        return result

    # review a given note
    def start_review(self):
        self.load_book()
        self.old_mtime = self.data["mtime"]
        self.__iter__()
        self.review_cnt = 0

    def review_one_note(self):
        try:
            self.review_cnt += 1
            note = self.__next__()
            note_changed = note.review()
            if note_changed:
                self.data["mtime"] = time.ctime()
            if note.can_delete():
                self.data["entries"].pop(note.get_key(), None)
        except AttributeError as e:
            print(e, "forgot to call start_review before reviewing?")
        except StopIteration as e:
            print("Error: no more note for review.")

    def end_review(self):
        try:
            if self.data["mtime"] != self.old_mtime:
                self.save_book()
            if self.review_cnt != 0:
                msg = ("{} of {} records in {} have been reviewed.\n").format(
                       self.review_cnt,
                       self.get_note_count(),
                       self.book_name)
                print(colored(msg, 'b'))
            return self.review_cnt
        except AttributeError as e:
            print(e, "forgot to call start_review before ending review?")

    '''
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
                    e.review()
                    if e.can_delete():
                        self.data["entries"].pop(keys[ri], None)
                    review_cnt += 1
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print("Review interrupted by", e)
                    raise
        return review_cnt
    '''
    def export_book(self, raw_data_file):
        dump_file = raw_data_file.strip()
        if raw_data_file == "-" or raw_data_file == "":
            fp = sys.stdout;
        else:
            print("Export the notebook to " + dump_file)
            fp = open(dump_file, "w")
        self.load_book()
        for idx, attr in enumerate(self.attr_keys):
            attr_desc = self.attr_desc[idx]
            if attr not in self.data or not self.data[attr]:
                #print("Warning:", "no", attr_desc, "in notebook.")
                continue
            if attr == "entries":
                fp.write(attr_desc + ": " + "see all entries below\n")
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
        self.load_book()
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
        self.save_book()

    def fortune(self):
        self.load_book()
        key_list = list(self.data["entries"].keys())
        if key_list != []:
            random_key = random.choice(key_list)
            return self.data["entries"][random_key]
        else:
            return None

    '''
    def randomize_notes(self):
        self.load_book()
        random.shuffle(self.data["entries"])
        return self.data["entries"]
    '''

    def __iter__(self):
        self.load_book()
        self.index = -1
        self.keys = list(self.data["entries"].keys())
        random.shuffle(self.keys)
        return self

    def __next__(self):
        try:
            self.index += 1
            key = self.keys[self.index]
            return self.data["entries"][key]
        except IndexError as e:
            self.save_book()
            raise StopIteration
