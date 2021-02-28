import re
import sys

Instructions=[]

Registers={"$s0":0,"$s1":0,"$s2":0,"$s3":0,"$s4":0,"$s5":0,"$s6":0,"$s7":0,"$t0":0,"$t1":10,"$t2":0,"$t3":0,"$t4":0,"$t5":0,"$t6":0,"$t7":0,"$t8":0,"$t9":0,"$zero":0,"$a0":0,"$a1":0,"$a2":0,"$a3":0,"$v0":0,"$v1":0,"$gp":0,"$fp":0,"$sp":0,"$ra":0,"$at":0}

Memory=[]

def checkRegister(R):
    return True if R in Registers.keys() else False


class add:
    instruction=[]
    def __init__(self,ins):
        self.instruction=ins
    
    def check(self):
        
        if len(self.instruction)== 4: 
            ok = True
            for i in range(1,4):
                ok = ok and checkRegister(self.instruction[i])
            if ok:
                self.update()
                return
        sys.exit()
    
    def update(self):
        Registers[self.instruction[1]] = Registers[self.instruction[2]] + Registers[self.instruction[3]]


class control:
    adder=add([])
    def __init__(self,instruction):
        self.current=instruction
    
    def makeWay(self):
        if len(self.current)==0 :
            sys.exit()
        operation=self.current[0]
        if operation=="add" :
            self.adder.__init__(self.current)
            self.adder.check()
        else:
            sys.exit()

with open("Addition.asm") as f:
    Instructions= f.readlines()

for i in range(len(Instructions)):
    Instructions[i]=re.split(" |,|\n",Instructions[i])
    while "" in Instructions[i]:
        Instructions[i].remove('')

InstructionsStartFrom=0

for i in range(len(Instructions)):
    if Instructions[i][0]=="main:":
        InstructionsStartFrom=i+1
        break
direct=control(Instructions[InstructionsStartFrom])

# for i in range(InstructionsStartFrom,len(Instructions)):
# direct.__init__(Instructions[i])
direct.makeWay()

print(Instructions)
print(Registers)
print(Memory)