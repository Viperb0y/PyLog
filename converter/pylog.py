#!/usr/bin/python3

import base64
import hashlib
import datetime
import getpass
import os
import sys
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw.encode("utf-8"))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode("utf-8")

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

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
        self.read_notebook()
        #calls console manager for input
        self.console()
        #encrypts and writes to notebook again. <- NO DECRYPTED CONTENT ON HDD at any point.
        self.write_notebook()
    
    def load_types(self):
        with open("types") as f:
            type_list = f.readlines()
            for logtype in type_list:
                self.types[logtype.split('\t')[0]] = logtype.split('\t')[1][:-1]

    def splash(self):
        print("Input type:")
        types_list = []
        for x in self.types:
            types_list.append("\t{} -> {}".format(x,self.types[x]))
        print('\n'.join(sorted(types_list)))
    def read_notebook(self):
        if not os.path.isfile("notebook"):
            p1 = "+"
            p2 = "-"
            while p1 != p2:
                print("Choose")
                p1 = getpass.getpass()
                print("Repeat")
                p2 = getpass.getpass()
                if p1 != p2:
                    print("Mismatch!")
            self.cipher = AESCipher(p1)
            f = open("notebook","wb")
            f.write(self.cipher.encrypt("<CONTROL>\t\t\t"))
            f.close()
            sys.exit(0)
        with open("notebook","rb") as notebook:
                try:
                    self.cipher = AESCipher(getpass.getpass())
                    self.logs = self.cipher.decrypt(notebook.read()).split("\n")
                #This checks if file was decrypted properly.
                    if self.logs[0] == "<CONTROL>\t\t\t":
                        print("Correct password.")
                        #listing type options
                        self.splash()
                    else:
                        print("Wrong password.")
                        sys.exit(0)
                except Exception:
                    print("Wrong password.")
                    sys.exit(0)

    def get_moment(self):
        return datetime.datetime.now().strftime("%d.%m.%Y.\t%H:%M\t")
    
    def console(self):
        try:
            i = input("> ")
            if i == 'x':
                return
            elif i == 'v':
                print("You entered notebook viewing mode.")
                JournalViewer(self.logs,self.types)
            elif i in self.types:
                entry_head = self.get_moment()
                entry_body = input("{} > ".format(self.types[i]))
                if entry_body == 'x':
                    self.console()
                self.logs.append(entry_head+"[{}]".format(self.types[i])+entry_body)
            else:
                print("Invalid option.")
            self.console()
        except KeyboardInterrupt:
            self.write_notebook()
            sys.exit(0)
        
    def write_notebook(self):
        with open("notebook","wb") as notebook:
            notebook.write(self.cipher.encrypt('\n'.join(self.logs)))
            notebook.close()

class JournalViewer():
    
    def __init__(self,notebook,entry_types):
        self.notebook = [tuple(x.split('\t')) for x in notebook]
        self.entry_types = entry_types
        #IN DEVELOPMENT.
        self.operations = {"options":self.splash,
                           "time":self.time_filter,
                           "date":self.date_filter,
                           "type":self.type_filter,
                           "search":self.search,
                           "reverse":self.reverse,
                           "dump": self.dump,
                           "show":self.show()}
        #info
        self.splash()
        
    def console(self):
        try:
            #console input
            i = input("v > ").replace(" ","")
            if i == "x":
                return
            if i.split(",")[0] in self.operations:
                self.operations[i.split(" ")[0]]
    def splash(self,notebook):
        print("Available commands are:")
        for key,value in self.operations:
            print("\t"+key)
    def type_filter(self,entry_type):
        self.notebook = list(filter(lambda x: True if x[2] == entry_type else False, self.notebook))
    def time_filter(self,notebook,hour = 0, hour_range = (0,0),):
        pass
    def date_filter(self,date):
        pass
    def search(self,regex):
        pass
    def reverse(self):
        pass
    def dump(self,filename):
        pass
    def show(self,)
        pass

if __name__ == "__main__":
    JournalWriter()
