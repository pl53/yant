from yant.utils import colors
from yant.utils import utils, yant_utils
import subprocess
colored = colors.Colors.colored


class Flashcard:
    # basic flashcard type for memo notebook
    def __init__(self, key, note=[], weight=3, ask_user_input=False):
        try:
            self.key = key.strip() # "key" means "title" in user's language
            self.note = note[:]    # should have been the plural "notes"
            if ask_user_input:
                self.append()
        except:
            raise yant_utils.YantException("Title should be string and note should be list")
        if weight > 5 or weight < 1:
            raise yant_utils.YantException("Flashcard weight should be an integer in range [1, 5]")

        # weight assigned by the user, potential future use
        self.weight = weight 
  
    ''' Used to merge flashcards from different dictionaries
    '''
    def merge(self, flashcard):
        if self.key != flashcard.key:
            raise yant_utils.YantException("Cannot merge flashcards with different keys.")
        else:
            self.note += flashcard.note
            self.weight = (self.weight + flashcard.weight) // 2

    def delete(self, i):
        try:
            self.note.pop(i)
        except IndexError as e:
            raise yant_utils.YantException("flashcard doesn't exist.")

    def input(self):
        return input("Add a note for {} (press {} to finish): "\
                   .format(colored(self.key, "g"), colored("Enter", "c")))

    '''copy everything from the other flashcard'''
    def copy(self, other):
        self.key = other.key
        self.note = other.note[:]
        self.weight = other.weight

    def append(self, new_notes=[]):
        if new_notes:
            self.note += list(new_notes)
        else:
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

    '''the user remember the flashcard for this time
    '''
    def remember(self):
        if self.weight > 0:
            self.weight -= 1

    '''the user forget the flashcard for this time
    '''
    def forget(self):
        if self.weight < 5:
            self.weight += 1

    def mark_deletion(self):
        self.weight = 0

    def can_delete(self):
        return self.weight == 0

    def format_note(self):
        return '\n'.join(["#" + str(i+1) + ": " + utils.fstr(s) \
                          for i,s in enumerate(self.note)])

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

        expanded_commands = []
        # preprocessing commands to expand '{+}' 
        for cmd in commands:
            if '{+}' in cmd:
                if len(self.note) == 0:
                    new_cmd = cmd.replace('{+}', '')
                    expanded_commands.append(new_cmd)
                    continue
                for i in range(len(self.note)):
                    new_cmd = cmd.replace('{+}', '{'+str(i+1)+'}')
                    expanded_commands.append(new_cmd)
            else:
                expanded_commands.append(cmd)

        trans = {}
        trans['{}'] = yant_utils.quote_multi_words(self.key)
        trans['{0}'] = yant_utils.quote_multi_words(self.key)
        for i in range(len(self.note)):
             quoted_note = yant_utils.quote_multi_words(self.note[i])
             trans['{'+str(i+1)+'}'] = quoted_note

        cmd_list = []
        for cmd in expanded_commands:
            # replace space with newline to deal with keys that have space
            for f,t in trans.items():
                cmd = cmd.replace(f, t)
            cmd_list.append(cmd)

        for cmd in cmd_list:
            print(colored('Run ', "r") + colored(cmd, 'b'))
            subprocess.call(cmd, shell=True)

    def show_user_note(self):
        print(colored('Your notes:', 'r'))
        if self.note:
            print(self.format_note())
        else:
            print("<No note added>")

    def show_note(self, external_note_cmd=[]):
        self.show_external_note(external_note_cmd)
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
            return False # flashcard not modified

        return True # flashcard modified

    # return True if flashcard modified, else False
    def review(self, external_note_cmd=[]):
        print("Remember this flashcard? ===========> ", end="")
        self.show_key()
        cmd = input("Press {} to see the notes => ".\
                    format(colored("Enter", "c"))) # just to continue
        self.show_note(external_note_cmd)
        cmd = input(("Delete({0}), Update({1}), Quit({2}), or " + \
                     "Next(<{3}>)=> ").format(colored('d', 'y'), \
                     colored("u", "y"), colored('q', 'y'), \
                     colored('Enter', 'y'))) 
        return self.exec_cmd(cmd, parent_process_name="Review")
    
    def __str__(self):
       s = '\n'.join([self.key] + self.note)
       return s + "\n"
