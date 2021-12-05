import sys
import csv
import random
from os import system

class Perk():
    def __init__(self,category,text,value=-1):
        self.category = category
        self.text = text
        self.value = value
        self.answered = 0
        self.answer_chance = 1

    def setValue(self,value):
        self.value = value

    def incrementAnswered(self):
        self.answered += 1

    def halfAnswerChance(self):
        self.answer_chance /= 2

    def __str__(self):
        out = self.category + " " + self.text + " " + str(self.value) + " " + str(self.answered)
        return out

def from_file(filepath):
    with open(filepath, newline='') as file:
        csvreader = csv.reader(file,delimiter=',')
        perks = []
        options = dict()

        headers = csvreader.__next__()
        for value in headers:
            options[value] = 0

        for line in csvreader:
            for count, value in enumerate(line):
                if (value != "-"):
                    perk = Perk(headers[count],value)
                    perks.append(perk)

        return options,perks

options, perks = from_file("input.csv")
answered_count = 0
to_answer = len(perks)

system("clear")

while (answered_count < to_answer):
    iter = random.randint(0,to_answer - 1)
    if (perks[iter].answer_chance > random.random()):
        print("\nPlease rate this option on a scale of 1-5:")
        perks[iter].incrementAnswered()
        print(perks[iter].text + ": ", end='')
        value = int(input())

        if (perks[iter].answered == 1):
            answered_count += 1
            perks[iter].setValue(value)
        else:
            new_value = perks[iter].value*(perks[iter].answered-1)
            new_value += value
            new_value /= perks[iter].answered
            perks[iter].setValue(new_value)

        perks[iter].halfAnswerChance()
        #sys.stdout.write("\033[{}C\033[1A\r".format(" "*(len(perks[iter].text)+5)))
        system("clear")

# Begin adding up.
for perk in perks:
    options[perk.category] = options[perk.category] + perk.value

first = max(options,key=options.get)
top = options[first]
del options[first]

second = max(options,key=options.get)
not_top = options[second]

print("\nWinner: " + first + " by " + str(top - not_top))
print("Runner up: " + second + "\n")

print("\n" + first + " perks:")
for perk in perks:
    if (perk.category == first):
        print(perk.text + ": " + str(perk.value))

print("\n" + second + " perks:")
for perk in perks:
    if (perk.category == second):
        print(perk.text + ": " + str(perk.value))
