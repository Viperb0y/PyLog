#!/usr/bin/python3
#written by Bernard Crnković

import datetime
import password
import os
import sys
from journalreader import JournalViewer
from aes_implementation import AESCipher
from colors import Colors

class JournalWriter:

    def __init__(self):
        #Initializing types dict
        self.types = {}
        #Initializing notebook entry list (will be used after decryption)
        self.logs = []
        #New cipher object
        self.cipher = None
        #Read from "types" file
        self.load_types()
        #loads notebook contents into
        self.get_notebook()
        #calls console manager for input
        print(Colors.BLUE+"Type 'H' for help.")
        self.console()
        #encrypts and writes to notebook again. <- NO DECRYPTED CONTENT ON HDD at any point.
        self.write_notebook()
        #holds current entry index value
        self.current_entry_index = 0
    
    def load_types(self):
        with open("types") as f:
            type_list = f.readlines()
            for logtype in type_list:
                self.types[logtype.split('\t')[0]] = logtype.split('\t')[1][:-1]

    def splash(self):
        types_list = []
        print(Colors.BLUE+"Type 'V' to enter '[READING_MODE]'.")
        print("Type 'X' to exit.")
        print("Input types:")
        for x in self.types:
            types_list.append("\t{} -> {}".format(x,self.types[x]))
        print('\n'.join(sorted(types_list)))

    def get_notebook(self):
        if not os.path.isfile(sys.argv[1]):
            self.cipher = AESCipher(password.create_password())
            with open(sys.argv[1],"wb") as f:
                f.write(self.cipher.encrypt("<ID>\t<DATE>\t<TIME>\t<TYPE>\t<CONTENT>"))
                f.close()
        with open(sys.argv[1],"rb") as notebook:
                try:
                    self.cipher = AESCipher(password.input_password())
                    self.logs = self.cipher.decrypt(notebook.read()).split("\n")
                #This checks if file was decrypted properly.
                    if self.logs[0] == "<ID>\t<DATE>\t<TIME>\t<TYPE>\t<CONTENT>":
                        print(Colors.GREEN+"Correct password.")
                        #listing type options
                        #self.splash()
                    else:
                        print(Colors.YELLOW+"Wrong password.")
                        sys.exit(0)
                except Exception:
                    print(Colors.YELLOW+"Wrong password.")
                    sys.exit(0)

    def get_moment(self):
        return datetime.datetime.now().strftime("%d.%m.%Y.\t%H:%M\t")
    
    def console(self):
        try:
            i = input(Colors.RED+"[WRITING_MODE] > \033[39m")
            if i == 'X':
                self.write_notebook()
                sys.exit(0)
            elif i == 'R':
                #print("Entered '[READING_MODE]'.")
                JournalViewer(self.logs, self.types,self)
            elif i == "H":
                self.splash()
            elif i in self.types:
                self.get_index()
                entry_block = str(self.current_entry_index)+"\t"
                entry_block += self.get_moment()
                entry_body = input(Colors.RED+"{} > {}".format(self.types[i],Colors.WHITE))
                if entry_body == 'x':
                    self.console()
                else:
                    self.logs.append(entry_block+"{}\t".format(self.types[i])+entry_body)
                    self.write_index()
            elif i == "W":
                pass
            else:
                print(Colors.YELLOW+"Unknown command.")
            self.console()
        except KeyboardInterrupt:
            self.write_notebook()
            print()
            sys.exit(0)
            
    def get_index(self):
        with open("counter_id","r") as f:
            self.current_entry_index = int(f.readlines()[0])
    
    def write_index(self):
        with open("counter_id","w") as f:
            f.write(str(self.current_entry_index+1))
    
    def write_notebook(self):
        with open(sys.argv[1],"wb") as notebook:
            notebook.write(self.cipher.encrypt('\n'.join(self.logs)))
        
if __name__ == "__main__":
    JournalWriter()
