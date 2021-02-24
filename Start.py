Instructions=[]
with open("Addition.asm") as f:
    Instructions= f.readlines()
print(Instructions)
for i in range(len(Instructions)):
    Instructions[i]=Instructions[i].split(" ")
print(Instructions)