#This is a simple text generating program that uses a Markov Chain on "blocks" of characters, and generates new text using it.
#_________________________________________SETTINGS______________________________________________
inputpath = "../Desktop/example.txt"     #What file should it look at?
outputpath = "../Desktop/NEW_STUFF.txt"   #Where should it output to?
backlength = 3        #How many past "blocks" should it look at for context?
outputlength = 50000     #How long should the generated text be?
timeLimit = 0      #The program automatically stops after *timeLimit* minutes. Set it to 0 to disable.
alertrate = 5      #The program prints its status every *alertrate* seconds.

def breaklogic(x): #The input is a character. This is used to break up the string into "blocks" for the Markov Chain to use.
    #Examples:
    #return True #Separate individual characters
    return x in ["\n", " "] #Separate by words
    #return x in [".",",","?","!",";",":","(",")","\n","\t","\r","[","]",'"',"'"] #Separate by phrases?
#_______________________________________END OF SETTINGS___________________________________________
    
import time as t

import random as r

class chain:
    def __init__(self):
        self.structure = []
        self.current = 0
        self.states = []

    def setstate(self, state):
        try:
            self.current = self.states.index(state)
        except ValueError:
            WellCrap = True

    def iterate(self):
        if len(self.states) > 0:
            distribution = self.structure[self.current]
            total = sum(self.structure[self.current])
            guess = r.random()
            level = 0
            nextstate = 0
            if total == 0:
                self.current = r.randint(0, len(self.states) - 1)
            else:
                for x in range(len(distribution)):
                    level += distribution[x] / total
                    if guess < level:
                        nextstate = x
                        break
                self.current = nextstate
        else:
            print("chain is empty!")

    def store(self, nextstate):
        try:
            statenumber = self.states.index(nextstate)
            self.structure[self.current][statenumber] += 1
        except ValueError:
            self.add(nextstate)
            self.store(nextstate)

    def add(self, state):
        length = len(self.structure)
        for x in range(length):
            self.structure[x].append(0)
        new = []
        for x in range(length + 1):
            new.append(0)
        self.structure.append(new)
        self.states.append(state)
        
author = chain() #Very funny, I know.

file = open(inputpath, "r")

source = file.read()

file.close()

length = len(source)

point = []

location = 0

for x in range(backlength):
    block = ""
    while True:
        block += source[location % length]
        location += 1
        if breaklogic(source[location % length]):
            break
    point.append(block)

try:
    print("storing...")
    clock = t.time()
    start = t.time()
    while location < length and (((t.time() - start) / 60 < timeLimit) or timeLimit == 0):
        author.setstate(point)
        block = ""
        while True:
            block += source[location % length]
            location += 1
            if breaklogic(source[(location - 1) % length]):
                break
        point = point[1:] + [block]
        author.store(point)
        if t.time() - clock >= alertrate:
            print("Stored " + str(location) + " characters, contains " + str(len(author.structure)) + " unique blocks.")
            clock = t.time()
except KeyboardInterrupt:
    print("terminated.")

print("generating...")

author.current = r.randint(0, len(author.states) - 1)

out = ""

clock = t.time()

try:
    for x in range(outputlength):
        author.iterate()
        out += author.states[author.current][0]
        if t.time() - clock >= alertrate:
            print("Generated " + str(x) + " blocks.")
            clock = t.time()
except KeyboardInterrupt:
    print("terminated.")

file = open(outputpath, "w")

file.write(out)

file.close()
