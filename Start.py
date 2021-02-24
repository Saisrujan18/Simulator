import re
Instructions=[]
Registers=[]
Memory=[]
for i in range(32):
    Registers.append(0)
with open("Addition.asm") as f:
    Instructions= f.readlines()
for i in range(len(Instructions)):
    Instructions[i]=re.split(" |,|\n",Instructions[i])
    while "" in Instructions[i]:
        Instructions[i].remove('')
print(Instructions)
print(Registers)
print(Memory)