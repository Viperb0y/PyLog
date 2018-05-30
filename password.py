#written by Bernard Crnković

from getpass import getpass

def create_password():
    first = "1"
    second = "2"
    while first!=second:
        if first!="1":
            print("Passwords don't match")
        first = getpass(prompt="\033[95mChoose password: ")
        second = getpass(prompt="Repeat password: ")
    return first
    
def input_password():
    return getpass(prompt="\033[92mEnter password:\033[39m ")
