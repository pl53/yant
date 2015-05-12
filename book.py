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
            obj.desc, obj.entries = data
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
            pickle.dump((obj.desc, obj.entries), fp) 
    except pickle.PicklingError as e:
        sys.stderr.write("Unable to store data.\n")

# no write back
def read_book(func):
    def inner(obj, *args):
        with open(obj.filename, "rb") as fp:
            obj.desc, obj.entries = pickle.load(fp)
        val = func(obj, *args)
        return val
    return inner

class Notebook:
    entry_delim = ".X.X.X.X.X.X.X.X.X.\n"
    ''' notebook of English entries
    '''
    def __init__(self, book_name, entry_type):
        self.filename = book_name.strip()
        self.entry_type = entry_type
        self.book_name = self.filename.split("/")[-1][:-3]

    def create_book(self, desc):
        with open(self.filename, "wb") as fp:
            pickle.dump((desc, {}), fp)

    def update_desc(self, desc):
        with open_book(self):
            self.desc = desc

    def add_entry(self, raw_key, entry_type):
        key = raw_key.strip()
        with open_book(self):
            if key not in self.entries:
                self.entries[key] = entry_type(key)
            self.entries[key].append_notes()
            print("One record added/updated.")

    def update_entry(self, raw_key):
        key = raw_key.strip()
        with open_book(self):
            if key in self.entries:
                rv = self.entries[key].update_notes()
                if rv == 0:
                    print("Record updated, updated user notes:") 
                    self.entries[key].show_note()
                else:
                    print("Record not updated.")
            else:
                print("Warning: {} not in the book".format(key))

    def delete_entry(self, raw_key):
        key = raw_key.strip()
        with open_book(self):
            try:
                del self.entries[key]
                print("Record deleted.")
            except KeyError as e:
                print("Nonexistent keyword " + key + ", skip.")
    @read_book
    def description(self):
        print(self.desc)

    @read_book
    def get_entry_count(self):
        return len(self.entries)

    @read_book
    def search_entries(self, pattern):
        pattern = pattern.lower().strip()
        result = []
        prog = re.compile(pattern)
        with open_book(self):
            for e in self.entries:
                for w in self.entries[e].__str__().split():
                    if prog.match(w.strip("\"\'")): # match found
                        result.append(self.entries[e])
                        break
        return result

    def random_review(self, random_indices=[]):
        review_cnt = 0 
        with open_book(self):
            if random_indices == []: # review all entries
                random_indices = list(range(len(self.entries)))
                random.shuffle(random_indices)
            keys = list(self.entries.keys())
            total_cnt = len(keys)
            for ri in random_indices:
                try:
                    e = self.entries[keys[ri]]
                    review_cnt += 1
                    print("Remember this? ===========> ", end="")
                    e.show_key()
                    cmd = input("Press {} to reveal it => ".\
                                format(colored("Enter", "c"))) # just to continue
                    e.show_note()
                    cmd = input("Delete({0}), Update({1}), Quit({2}), or Next(<{3}>)=> ".format( \
                                colored('d', 'y'), colored("u", "y"), colored('q', 'y'), colored('Enter', 'y')))
                    e.exec_cmd(cmd)
                except (KeyboardInterrupt, entry.EntryExcept, IndexError) as e:
                    print("Review interrupted by", e)
                    rval = 1
                    break
            else:
                rval = 0
            #for k in keys:
            #    if self.entries[k].rmb_cnt >= 1000:
            #         del self.entries[k]
            #print(colored(("\nYou have finished reviewing {} of {} records,"+\
            #      " keep going!").format(review_cnt, total_cnt), 'b'))
        return rval   
 
    @read_book
    def export_book(self, raw_filename):
        dump_file = raw_filename.strip()
        print("Export the notebook to " + dump_file)
        with open(dump_file, "w") as fp:
            if hasattr(self, "desc"):
                fp.write(self.desc+'\n')
            else:
                fp.write("No notebook description.\n")
            fp.write(self.entry_delim)
            for e in self.entries:
                fp.write(str(self.entries[e]))
                fp.write(self.entry_delim)

    def import_book(self, raw_filename):
        src_file = raw_filename.strip()
        print("import notebook from " + src_file)
        with open_book(self): 
            with open(src_file, "r") as fp:
                raw_notes = fp.read().split(self.entry_delim)
                try:
                     self.desc = raw_notes[0]
                     for note_str in raw_notes[1:]:
                         if note_str == '':
                             continue
                         note = note_str.strip().split('\n')
                         new_entry = self.entry_type(note[0], note[1:])
                         self.entries[note[0]] = new_entry # note[0] is key
                except:
                     sys.stderr.write("Oops... error during importing process.\n")

    @read_book
    def pick_random_entry(self):
        key_list = list(self.entries.keys())
        if key_list != []:
            random_key = random.choice(key_list)
            return self.entries[random_key]
        else:
            return None

    @read_book
    def randomize_entries(self):
        random.shuffle(self.entries)
        return self.entries

    @read_book
    def __iter__(self):
            self.index = -1
            return self

    def __next__(self):
        try:
            self.index += 1
            key = self.keys[self.index]
            return self.entries[key]
        except IndexError as e:
            with open(self.filename, "wb") as fp:
                pickle.dump((self.desc, self.entries), fp)
            raise StopIteration


#    def open(self):
#        if self.opened == True:
#            return
#        try:
#            with open(self.filename, "rb") as fp:
#                self.entries = pickle.load(fp)
#                #self.keys = list(self.entries.keys())
#                #random.seed()
#                #random.shuffle(self.keys)
#                #return self.entries
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
#                #pickle.dump((self.entries), fp)
#                return pickle.dump(self.entries, fp)
#        except pickle.PickleError as e:
#            print("unable to store entries to notebook")
#        self.opened = False
