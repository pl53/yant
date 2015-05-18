from colors import colors
import utils
import subprocess
colored = colors.colored

class EntryExcept(Exception):
    def __init__(self, s):
        self.value = s
    def __str__(self):
        return str(self.value)

class Entry:
    ''' basic entry type for memo notebook '''
    def __init__(self, key, note=[], weight=3):
        try:
            self.key = key.strip()
            self.note = note[:]
        except:
            print("The key should be a string and note should be a list")
            sys.exit(1)
        if weight > 5 or weight < 1:
            raise Exception("Weight for the entry should be an integer in [1, 5]")
        self.weight = weight # how many times the user remember the entry
  
    def merge(self, entry):
        if self.key != entry.key:
            print("Cannot merge entries with different keys.")
        else:
            self.note += entry.note
            self.weight = (self.weight + entry.weight) // 2

    def del_note(self, i):
        try:
            self.note.pop(i)
        except IndexError as e:
            print("Cannot remove a non-existent note.")

    def input_note(self):
        note = input("Add a note for {} (press {} to finish): ".\
                   format(colored(self.key, "g"), colored("Enter", "c")))
        return utils.fstr(note)

    def append_notes(self):
        #print("Multiple notes can be added for the item.")
        while True:
            new_note = self.input_note()
            if new_note == "":
                break
            self.note.append(new_note)

    def update_notes(self):
        return utils.update_list(self.note, self.input_note, "note")

    def update_n_append(self):
        self.update_notes()
        self.append_notes()

    def remember(self):
        '''the user remember the entry for this time'''
        if self.weight > 1:
            self.weight -= 1
            

    def forget(self):
        '''the user forget the entry for this time'''
        if self.weight < 5:
            self.weight += 1

    def mark_deletion(self):
        self.weight = 0

    #def dump_value(self):
    #    '''dump the list of values as a string'''
    #    tagged_values = ["# " + v for v in self.value]
    #    return "\n".join(tagged_values)
     
    def format_note(self):
        formatted_notes = ["#"+ str(i+1) + ": " + self.note[i] \
                           for i in range(len(self.note))]
        return formatted_notes

    def show_key(self):
        '''first step of a three-step process'''
        print(colored(self.key, "green"))

   
    def show_external_note(self):
        '''show note from external sources'''
        pass

    def show_user_note(self):
        if self.note:
            utils.paged_print(self.format_note())
        else:
            utils.paged_print(["<No user note>"])

    def show_note(self):
        self.show_external_note()
        self.show_user_note()

    def exec_cmd(self, cmd):
        if len(cmd) > 2:
            return
        CMD = cmd.upper()
        if "Y" in CMD:
            self.remember()
        elif "D" in CMD:
            self.mark_deletion()
        else: # N or other
            self.forget()
        if 'U' in CMD:
            self.update_notes()
        if 'A' in CMD:
            self.append_notes()
        if "Q" in CMD:
            raise EntryExcept("review ends.")
    
    def __str__(self):
       s = '\n'.join([self.key] + self.note)
       return s + "\n"

class wordEntry(Entry):
   
    #def show_hint(self):
    #    '''print word and example sentences'''
    #    print(colored(self.key, "green"))
    #    if self.dump_note() != "":
    #        hl_key = colored(self.key, "yellow")
    #        print(self.dump_note().replace(self.key, hl_key))

    def show_external_note(self):
        '''show word explanation from sdcv and pronounce word with forvo'''
        try:
            PIPE = subprocess.PIPE
            process = subprocess.Popen(["sdcv", self.key], \
                                      stdin=PIPE, stdout=PIPE) 
            sdcv_out_bytes, err = process.communicate()
            sdcv_out = str(sdcv_out_bytes, encoding='utf-8')
            if "Your choice[-1 to abort]:" not in sdcv_out and \
               "Nothing similar to " not in sdcv_out:
                utils.paged_print(sdcv_out.replace(self.key, \
                                  colored(self.key, "g")).splitlines())                
        except Exception as e:
            print("sdcv not installed?")
        
        utils.SysCall(["forvo.py", self.key.replace(" ", "_")]) #pronouce the word
    
    #def cleanup(self, cmd):
    #    super().cleanup(cmd)
    #    if len(self.key) <= 4:
    #        return
    #    while "N" in cmd.upper() and " " not in self.key: # ignore phrases
    #        recite = input("Type the word again for memorization: ")
    #        if recite.strip().upper() == self.key.strip().upper():
    #            break
