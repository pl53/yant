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
        with open(obj.filename, "rb") as fp:
            data = pickle.load(fp)
            obj.desc, obj.entries = data
        yield
        with open(obj.filename, "wb") as fp:
            pickle.dump((obj.desc, obj.entries), fp) 
    except IOError:
        sys.stderr.write("Cannot open notebook, already in use?\n")
    #except:
    #    sys.stderr.write("Something wrong happens, that's embarrassing...\n")

# no write back
def load_book(func):
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
    @load_book
    def description(self):
        print(self.desc)

    @load_book
    def search_entries(self, pattern):
        pattern = pattern.lower().strip()
        match_cnt = 0
        print("Search book " + colored(self.book_name, "y") + " ..")
        prog = re.compile(pattern)
        with open_book(self):
            for e in self.entries:
                result = prog.match(self.entries[e].__str__())
                if result:
                    match_cnt += 1
                    print("==Match #" + str(match_cnt) + "==")
                    print("Key:", end=' ')
                    self.entries[e].show_key()
                    self.entries[e].show_note()
        if match_cnt == 0:
            print("No matched record found.")

    def random_review(self):
        review_cnt = 0 
        with open_book(self):
            random_index = [i for i in range(len(self.entries))]
            random.shuffle(random_index)
            keys = list(self.entries.keys())
            for ri in random_index:
                e = self.entries[keys[ri]]
                try:
                    review_cnt += 1
                    print("Remember this? ===========> ", end="")
                    e.show_key()
                    cmd = input("Press {} to reveal it => ".\
                                format(colored("Enter", "c"))) # just to continue
                    e.show_note()
                    #cmd = input(("Know({0}), Forget({1}), Delete({2}), " +\
                    #        "Update({3}), Append({4}), or Quit({5})\n" +\
                    #        "Enter ({0}{1}{2}|{3}|{4}|{5}) ==> ")\
                    #        .format(colored('y', "y"), colored('n', "y"), \
                    #        colored('d', 'y'), colored("u", "y"), \
                    #        colored("a", 'y'), colored('q', 'y')))
                    cmd = input(("Delete({0}), Update({1}), Append({2}), Quit({3}), or Next <{4}>\n" +\
                            "Enter ({0}|{1}|{2}|{3}|<{4}>) ==> ")\
                            .format(colored('d', 'y'), colored("u", "y"), \
                            colored("a", 'y'), colored('q', 'y'), colored('Enter', 'y')))

                    e.exec_cmd(cmd)
                except (KeyboardInterrupt, entry.EntryExcept) as e:
                    break
            total_cnt = len(keys)
            for k in keys:
                if self.entries[k].rmb_cnt >= 1000:
                     del self.entries[k]
            print(colored(("\nYou have finished reviewing {} of {} records,"+\
                  " keep going!").format(review_cnt, total_cnt), 'b'))
 
    @load_book
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

    @load_book
    def pick_random_entry(self):
        key_list = list(self.entries.keys())
        if key_list != []:
            random_key = random.choice(key_list)
            return self.entries[random_key]
        else:
            return None

    @load_book
    def random_entries(self):
        random.shuffle(self.entries)
        return self.entries

    @load_book
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
