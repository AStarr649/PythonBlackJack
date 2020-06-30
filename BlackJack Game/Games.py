# Games Module

class Player(object):
    def __init__(self, name, bank = 1000):
        self.name = name
        self.bank = bank

    def __str__(self):
        rep = self.name + "\t" + str(self.bank)
        return rep

def ante(self, num):
    self.bank = self.bank - num        

def ask_yes_no(question):
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response

def ask_number(question, low, high):
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response

if __name__ == "__main__":
    print("You ran this module directly (and did not 'import' it).")
    input("\n\nPress the enter key to exit.")
