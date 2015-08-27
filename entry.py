from colors import colors
from yant_utils import YantException
import utils
import subprocess
colored = colors.colored

class Entry:
    ''' basic entry type for memo notebook '''
    def __init__(self, key, note=[], weight=3, ask_user_input=False):
        try:
            self.key = key.strip()
            self.note = note[:]
            if ask_user_input:
                self.append()
        except:
            raise YantException("Key should be string and note should be list")
        if weight > 5 or weight < 1:
            raise YantException("Entry weight should be an integer in [1, 5]")

        # weight assigned by the user, potential future use
        self.weight = weight 
  
    ''' Used to merge entries from different dictionaries
    '''
    def merge(self, entry):
        if self.key != entry.key:
            raise YantException("Cannot merge entries with different keys.")
        else:
            self.note += entry.note
            self.weight = (self.weight + entry.weight) // 2

    def delete(self, i):
        try:
            self.note.pop(i)
        except IndexError as e:
            raise YantException("Note doesn't exist.")

    def input(self):
        return input("Add a note for {} (press {} to finish): "\
                   .format(colored(self.key, "g"), colored("Enter", "c")))

    def append(self):
        while True:
            new_note = self.input()
            if new_note == "":
                break
            self.note.append(new_note)

    def update(self):
        return utils.update_list(self.note, self.input, "note")

    def update_n_append(self):
        self.update()
        self.append()

    '''the user remember the entry for this time
    '''
    def remember(self):
        if self.weight > 0:
            self.weight -= 1

    '''the user forget the entry for this time
    '''
    def forget(self):
        if self.weight < 5:
            self.weight += 1

    def mark_deletion(self):
        self.weight = 0

    def can_delete(self):
        return self.weight == 0

    def format_note(self):
        return ["#"+ str(i+1) + ": " + utils.fstr(s) \
                    for i,s in enumerate(self.note)]

    ''' TODO: make "green" configurable
    '''
    def get_key(self):
        return self.key

    def show_key(self):
        '''first step of a three-step process'''
        print(colored(self.key, "green"))
   
    def show_external_note(self, commands):
        '''show note from external sources'''
        if commands == []:
            return

        if len(self.key.split()) > 1:
            # key contains white space
            param = '"' + self.key + '"'
        else:
            param = self.key

        for cmd in commands:
            listed_cmd = cmd.replace("{}", param).split()
            print(colored("Executing " + listed_cmd[0], "r"))
            subprocess.call(listed_cmd)

    def show_user_note(self):
        if self.note:
            utils.paged_print(self.format_note())
        else:
            utils.paged_print(["<No user note>"])

    def show_note(self, exec_cmd=[]):
        self.show_external_note(exec_cmd)
        self.show_user_note()

    def exec_cmd(self, cmd, parent_process_name="Process"):
        CMD = cmd.strip().upper()
        if "" == CMD:
            return False # nothing to do
        elif "Y" == CMD:
            self.remember()
        elif "N" == CMD: 
            self.forget()
        elif 'D' == CMD:
            self.mark_deletion()
        elif 'U' == CMD:
            self.update()
        elif "Q" == CMD:
            raise KeyboardInterrupt(parent_process_name + " ends.")
        else:
            print("Unkown command. Skip.")
            return False # note not modified

        return True # note modified

    # return True if note modified, else False
    def review(self, exec_cmd):
        print("Remember this note? ===========> ", end="")
        self.show_key()
        cmd = input("Press {} to see the notes => ".\
                    format(colored("Enter", "c"))) # just to continue
        self.show_note(exec_cmd)
        cmd = input(("Delete({0}), Update({1}), Quit({2}), or " + \
                     "Next(<{3}>)=> ").format(colored('d', 'y'), \
                     colored("u", "y"), colored('q', 'y'), \
                     colored('Enter', 'y'))) 
        return self.exec_cmd(cmd, parent_process_name="Review")
    
    def __str__(self):
       s = '\n'.join([self.key] + self.note)
       return s + "\n"
