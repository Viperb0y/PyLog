#written by Bernard Crnković

from datetime import time
from datetime import date
from datetime import datetime
from aes_implementation import AESCipher
from colors import Colors
import password
import sys

class JournalViewer():
    
    def __init__(self,notebook,entry_types,jw):
        self.reference_to_writer = jw
        self.notebook = [tuple(x.split('\t')) for x in notebook][1:]
        self.entry_types = entry_types
        #IN DEVELOPMENT.
        self.operations = {"TIME":self.time_filter,
                           "DATE":self.date_filter,
                           "TYPE":self.type_filter,
                           "REVERSE":self.reverse,
                           "SHOW":self.show,
                           "DELETE":self.delete_entry,
                           "DUMP":self.dump}
        #info
        #self.splash()
        self.console()

    def console(self):
        #console input
        try:
            ipt = [list(filter(lambda a: a!="",x.split(" "))) for x in input(Colors.RED+"[READING_MODE] > \033[39m").split(",")]
            if not ipt[0]:
                print(Colors.YELLOW+"Unknown command.")
                self.console()
            elif ipt[0][0] == "X":
                raise KeyboardInterrupt
            elif ipt[0][0] == "W":
                return
            elif ipt[0][0] == "R":
                self.console()
            elif ipt[0][0] == "H":
                self.splash()
            elif ipt[0][0] not in self.operations:
                print(Colors.YELLOW+"Unknown command.")
                self.console()
            else:
                for i in ipt:
                    if i[0] in self.operations:
                        z = i.pop(0)
                        cmd = i
                        self.operations[z](*cmd)
                self.console()
        except KeyboardInterrupt:
            self.reference_to_writer.write_notebook()
            print()
            sys.exit(0)
            
    def splash(self):
        print(Colors.BLUE+"Type 'W' to return to '[WRITING_MODE]'.")
        print("Type 'X' to exit.")
        print("Available commands are:")
        for key in self.operations:
            print("\t"+key)
    
    def type_filter(self,*args):
        if args[0] in self.entry_types:
            self.notebook = list(filter(lambda x: True if x[3] == self.entry_types[args[0]] else False, self.notebook))
        else:
            print(Colors.YELLOW+"Unknown type filter command.")
            
    def gettime(self,d):
        return time(*[int(t) for t in d.split(":")])
    
    def time_filter(self,*args):
        if len(args) == 2:
            b = self.gettime(args[0])
            e = self.gettime(args[1])
            self.notebook = list(filter(lambda x: True if self.gettime(x[2]) >= b and self.gettime(x[2]) <= e else False, self.notebook))
        elif len(args) == 1:
            if ":" in args[0]:
                self.notebook = list(filter(lambda x: True if self.gettime(x[2]) == self.gettime(args[0]) else False, self.notebook))
            else:
                self.notebook = list(filter(lambda x: True if self.gettime(x[2]).hour == self.gettime(args[0]).hour else False, self.notebook))
        else:
            print(Colors.YELLOW+"Unknown time filter command.")
    
    def getdate(self,d):
        return date(*[int(t) for t in d.split(".")[:-1][::-1]])
    
    def date_filter(self,*args):
        if len(args) == 2:
            b = self.getdate(args[0])
            e = self.getdate(args[1])
            self.notebook = list(filter(lambda x: True if self.getdate(x[1]) >= b and self.getdate(x[1]) <= e else False, self.notebook))
        elif len(args) == 1:
            self.notebook = list(filter(lambda x: True if self.getdate(x[1]) == self.getdate(args[0]) else False, self.notebook))
        else:
            print(Colors.YELLOW+"Unknown date filter command.")
    
    def reverse(self):
        self.notebook=self.notebook[::-1]
    
    def show(self):
        for i in self.notebook:
            for j in i:
                print("\033[35m"+j)
            print()

    def delete_entry(self,*args):
        if len(args) == 1:
            for i in range(len(self.reference_to_writer.logs)):
                if self.reference_to_writer.logs[i].split("\t")[0] == args[0]:
                    self.reference_to_writer.logs.pop(i)
                    break #CHECK IF IT WORKS
            print(Colors.BLUE+"Deleted entries will be gone forever upon re-entering this mode!")
    
        elif len(args) == 2:
            to_remove = []
            for i in range(1,len(self.reference_to_writer.logs)):
                current_id = int(self.reference_to_writer.logs[i].split("\t")[0])
                if current_id >= int(args[0]) and current_id <= int(args[1]):
                    to_remove.append(i) #CHECK IF IT WORKS
            self.reference_to_writer.logs[to_remove[0]:to_remove[-1]+1]=[]
            print(Colors.BLUE+"Deleted entries will be gone forever upon re-entering this mode!")
    
    def dump(self,*args):
        f = None
        if not args:
            f = open(datetime.now().strftime("%d.%m.%Y.-%H:%M:%S"),"wb")
        else:
            f = open(args[0],"wb")
        writestring = "<ID>\t<DATE>\t<TIME>\t<TYPE>\t<CONTENT>\n"
        for i in self.notebook:
            for j in i:
                writestring+=j+"\t"
            writestring+="\n"
        f.write(AESCipher(password.create_password()).encrypt(writestring))
        f.close()
