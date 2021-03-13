# IMPORTING ALL THE LIBRARIES

import re
import sys
import copy
from blessed import Terminal

# ELEPHANT IN THE ROOM

Instructions=[]

operations=['add','addi','sub','bne','beq','j',"lw","sw","la","jal","jr","slt"]

Registers={"$s0":0,"$s1":0,"$s2":0,"$s3":0,"$s4":0,"$s5":0,"$s6":0,"$s7":0,"$t0":0,"$t1":0,"$t2":0,"$t3":0,"$t4":0,"$t5":0,"$t6":0,"$t7":0,"$t8":0,"$t9":0,"$zero":0,"$a0":0,"$a1":0,"$a2":0,"$a3":0,"$v0":0,"$v1":0,"$gp":0,"$fp":0,"$sp":0,"$ra":0,"$at":0,"$k0":0,"$k1":1}

Loops={}

jumpRelated=["j","beq","bne","jal","jr"]

MemoryRelated=["lw","sw","la"]

Memory={268435456+4*i:0 for i in range(1024)}

Data={}

MemoryIndex=268435456

Stackpointer=1023*4+268435456

term = Terminal()

y_pos=0

changed_register=""
changed_mem=""
changed = False
# 268435456 = 0x10000000

# FEW HELPFULL FUNCTIONS 

def print_registers(ch,chr):
    global y_pos    
    print(term.move_xy(term.width//2 - 5,2) + "REGISTERS")
    y_pos = 4
    x_pos = 0    
    for i in Registers:
        pri = f' {i} : {Registers[i]} '
        if x_pos+len(pri)+2 > term.width:
            x_pos = 0
            y_pos += 2
        if ch == True:
            print(term.move_xy(x_pos,y_pos) + term.on_bright_blue(pri))
        else:
            print(term.move_xy(x_pos,y_pos) + term.on_darkolivegreen(pri))
        x_pos += term.width//3

def print_memory():
    global y_pos
    x_pos = 0
    y_pos += 2
    print(term.move_xy(term.width//2 -3,y_pos) + "MEMORY")
    y_pos+=2
    for i in Memory:
        pri = f' {i} : {Memory[i]} '
        if x_pos+len(pri)+2 > term.width:
            x_pos = 0
            y_pos += 2
        if i > MemoryIndex:
            break
        print(term.move_xy(x_pos,y_pos) + term.on_darkolivegreen(pri))
        x_pos += len(pri)+3

def UpdateReturnAddress():
    global Stackpointer
    Registers["$ra"]=len(Instructions)
    Registers["$sp"]=Stackpointer

def AddToMemory(ins):
    global MemoryIndex
    if ins[1]!=".word":
        sys.exit()
    Data.update({ins[0]:MemoryIndex})
    for i in range(2,len(ins)):
        Memory[MemoryIndex]=int(ins[i])
        MemoryIndex+=4

def checkRegister(R):
    return True if R in Registers.keys() else False

# CLASSES FOR EACH INSTRUCTION

class add:
    instruction=[]
    def __init__(self,ins):
        self.instruction=copy.deepcopy(ins)
    
    def check(self):
        if len(self.instruction)==4: 
            ok = True
            for i in range(1,4):
                ok = ok and checkRegister(self.instruction[i])
            if ok:
                self.update()
                return
        sys.exit()
    
    def update(self):
        Registers[self.instruction[1]] = Registers[self.instruction[2]] + Registers[self.instruction[3]]
        changed = True
        changed_register=self.instruction[1]

class sub:
    instruction=[]
    def __init__(self,ins):
        self.instruction=copy.deepcopy(ins)

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
        Registers[self.instruction[1]] = Registers[self.instruction[2]] - Registers[self.instruction[3]]

class addi:
    global changed, changed_register
    instruction=[]
    def __init__(self,ins):
        self.instruction=copy.deepcopy(ins)

    def check(self):
        if len(self.instruction)== 4: 
            ok = True
            for i in range(1,4):
                if i<3 :
                    ok = ok and checkRegister(self.instruction[i])
                else:
                    temp=True
                    if checkRegister(self.instruction[-1])==True:
                        ok=False
                        temp=False
                    else:
                        ok=ok and temp
            if ok:
                self.update()
                return
            else:
                sys.exit()
        else:
            sys.exit()
    
    def update(self):
        Registers[self.instruction[1]] = Registers[self.instruction[2]] + int(self.instruction[-1])
        changed = True
        print(changed)
        changed_register=copy.deepcopy(self.instruction[1])

class beq:
    instruction=[]
    indexPosition=0
    def __init__(self,ins,ind):
        self.instruction=copy.deepcopy(ins)
        self.indexPosition=ind
    def check(self):
        if len(self.instruction)== 4: 
            ok = True
            for i in range(1,3):
                ok = ok and checkRegister(self.instruction[i])
            if self.instruction[-1] not in Loops.keys() :
                ok=False
            if ok:
                return self.update()
        sys.exit()
    
    def update(self):
        if Registers[self.instruction[1]]==Registers[self.instruction[2]]:
            return Loops[self.instruction[-1]]
        return self.indexPosition+1

class bne:
    instruction=[]
    indexPosition=0
    def __init__(self,ins,ind):
        self.instruction=copy.deepcopy(ins)
        self.indexPosition=ind
    def check(self):
        if len(self.instruction)== 4: 
            ok = True
            for i in range(1,3):
                ok = ok and checkRegister(self.instruction[i])
            if self.instruction[-1] not in Loops.keys() :
                ok=False
            if ok:
                return self.update()
        else:
            sys.exit()
    
    def update(self):
        if Registers[self.instruction[1]]!=Registers[self.instruction[2]]:
            return Loops[self.instruction[-1]]
        return self.indexPosition+1

class slt:
    instruction=[]
    def __init__(self,ins):
        self.instruction=copy.deepcopy(ins)
    
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
        if Registers[self.instruction[2]]<Registers[self.instruction[-1]]:
            Registers[self.instruction[1]]=1
            return
        Registers[self.instruction[1]]=0

class j:
    instruction=[]
    def __init__(self,ins):
        self.instruction=copy.deepcopy(ins)
    def check(self):
        if len(self.instruction)==2: 
            ok = True
            if self.instruction[-1] not in Loops.keys() :
                ok=False
            if ok:
                return self.update()
        sys.exit()
    
    def update(self):
        return Loops[self.instruction[-1]]

class lw:
    instructions=[]
    def __init__(self,ins):
        self.instructions=copy.deepcopy(ins)
    def check(self):
        if checkRegister(self.instructions[1])==False:
            sys.exit()
        self.instructions[-1]=self.instructions[-1].replace("(","")
        self.instructions[-1]=self.instructions[-1].replace(")","")
        offset=""
        whereisdollar=self.instructions[-1].find('$')
        for i in range(0,whereisdollar):
            offset+=self.instructions[-1][i]
        offset=int(offset)
        self.instructions[-1]=self.instructions[-1][whereisdollar:]
        if checkRegister(self.instructions[-1])==False:
            sys.exit()
        Registers[self.instructions[1]]=Memory[ (offset//4)*4 +Registers[self.instructions[-1]] ]

class sw:
    instructions=[]
    def __init__(self,ins):
        self.instructions=copy.deepcopy(ins)
    def check(self):
        if checkRegister(self.instructions[1])==False:
            sys.exit()
        self.instructions[-1]=self.instructions[-1].replace("(","")
        self.instructions[-1]=self.instructions[-1].replace(")","")
        offset=""
        whereisdollar=self.instructions[-1].find('$')
        for i in range(0,whereisdollar):
            offset+=self.instructions[-1][i]
        offset=int(offset)
        self.instructions[-1]=self.instructions[-1][whereisdollar:]
        if checkRegister(self.instructions[-1])==False:
            sys.exit()
        Memory[ (offset//4)*4 +Registers[self.instructions[-1]] ]=Registers[self.instructions[1]]

class jal:
    instruction=[]
    indexPosition = -1
    def __init__(self,ins,ind):
        self.instruction=copy.deepcopy(ins)
        self.indexPosition = ind
    def check(self):
        if len(self.instruction)==2: 
            ok = True
            if self.instruction[-1] not in Loops.keys() :
                ok=False
            if ok:
                return self.update()
        sys.exit()
    
    def update(self):
        Registers['$ra'] = self.indexPosition+1
        return Loops[self.instruction[-1]]

class jr:
    instruction=[]
    def __init__(self,ins):
        self.instruction=copy.deepcopy(ins)
    def check(self):
        if len(self.instruction)==2: 
            ok = True
            ok = ok and checkRegister(self.instruction[-1])
            if ok:
                return self.update()
        sys.exit()
    
    def update(self):
        return Registers[self.instruction[-1]]

class la:
    instructions=[]
    def __init__(self,ins):
        self.instructions=copy.deepcopy(ins)
    
    def check(self):
        if checkRegister(self.instructions[1])==False:
            sys.exit()
        if self.instructions[-1] not in Data.keys():
            sys.exit()
        self.update()
    
    def update(self):
        Registers[self.instructions[1]]=Data[self.instructions[-1]]

# MAIN CLASS WHERE EVERY INSTRUCTION IS SENT TO EXECUTE

class control:
    adder=add([])
    subber=sub([])
    addier=addi([])
    beqer=beq([],0)
    bneer=bne([],0)
    jer=j([])
    lwer=lw([])
    swer=sw([])
    slter=slt([])
    jaler=jal([],0)
    jrer=jr([])
    laer=la([])
    index=0
    def __init__(self,instruction,i):
        self.current=instruction
        self.index=i
    def makeWay(self):
        if len(self.current)==0 :
            sys.exit()
        operation=self.current[0]
        if len(self.current)==1:
            print("",end="")
        elif operation=="add" :
            self.adder.__init__(self.current)
            self.adder.check()
        elif operation=="sub":
            self.subber.__init__(self.current)
            self.subber.check()
        elif operation=="addi":
            self.addier.__init__(self.current)
            self.addier.check()
        elif operation=="beq":
            self.beqer.__init__(self.current,self.index)
            return self.beqer.check()
        elif operation=="bne":
            self.bneer.__init__(self.current,self.index)
            return self.bneer.check()
        elif operation=='j':
            self.jer.__init__(self.current)
            return self.jer.check()
        elif operation=="lw":
            self.lwer.__init__(self.current)
            self.lwer.check()
        elif operation=="sw":
            self.swer.__init__(self.current)
            self.swer.check()
        elif operation=="slt":
            self.slter.__init__(self.current)
            self.slter.check()
        elif operation=="jal":
            self.jaler.__init__(self.current,self.index)
            return self.jaler.check()
        elif operation=="jr":
            self.jrer.__init__(self.current)
            return self.jrer.check()
        elif operation=="la":
            self.laer.__init__(self.current)
            self.laer.check()
        else:
            sys.exit()

# >>>>>>> MANIPULAING INSTRUCTIONS START

#   FETCHING ALL LINES FROM ADDITION.ASM

with open("Addition.asm") as f:
    Instructions= f.readlines()

#   SPLITING EACHLINE ACCORDINGLY

for i in range(len(Instructions)):
    Instructions[i]=re.split(" |,|:|\n",Instructions[i])
    while "" in Instructions[i]:
        Instructions[i].remove('')
 
#   REMOVING COMMENTS FROM THE FILE 

for i in range(len(Instructions)):
    for j in range(len(Instructions[i])):
        if Instructions[i][j].find(";")!=-1 :
            temp=Instructions[i]
            temp=temp[:j]
            Instructions[i]=temp
            break
        if Instructions[i][j].find("#")!=-1 :
            temp=Instructions[i]
            temp=temp[:j]
            Instructions[i]=temp
            break


#   REMOVING EMPTY LINES

while [] in Instructions:
    Instructions.remove([])

# REMOVING TABS

for i in range(len(Instructions)):
    for j in range(len(Instructions[i])):
        while "\t" in Instructions[i][j]:
            Instructions[i][j]=Instructions[i][j].replace("\t","")

if [".text"]  in Instructions:
    temp1=Instructions.index([".text"])
    if Instructions[temp1+1]==[".globl","main"]:
        print("",end="")
    else:    
        sys.exit()
else:
    sys.exit()



if ['.text'] not in Instructions or [".globl","main"] not in Instructions:
    sys.exit()

# seperating loops with instructions which are in sameline

whereisgloblmain=len(Instructions)
for i in range(len(Instructions)):
    if Instructions[i]==[".globl","main"]:
        whereisgloblmain=i
        break

i=whereisgloblmain
n=len(Instructions)
while i<n:
    if Instructions[i][0] not in operations and len(Instructions[i])>2:
        Loops.update({Instructions[i][0]:i})
        temp=[Instructions[i][0]]
        temp2=Instructions[i][1:]
        Instructions[i]=temp
        Instructions.insert(i+1,temp2)
    n=len(Instructions)
    i+=1



if [".data"] in Instructions:
    i=1
    while Instructions[i]!=['.text']:
        if len(Instructions[i])==1:
            for j in range(len(Instructions[i+1])):
                Instructions[i].append(Instructions[i+1][j])
            m=Instructions.pop(i+1)
        i+=1

whereistext=len(Instructions)

for i in range(len(Instructions)):
    if Instructions[i]==[".text"]:
        whereistext=i
        break

for i in range(1,whereistext):
    AddToMemory(Instructions[i])


# <<<<<<< MANIPULATING INSTRUCTIONS ENDS HERE

InstructionsStartFrom=len(Instructions)

for i in range(len(Instructions)):
    if Instructions[i][0]=="main":
        InstructionsStartFrom=i
        for j in range(InstructionsStartFrom,len(Instructions)):
            if len(Instructions[j])==1:
                Loops.update({Instructions[j][0]:j})
        break

#   HEART OF THE SIMULATOR

UpdateReturnAddress()
direct=control([],0)
i=InstructionsStartFrom
# print(Instructions)

with term.cbreak(), term.hidden_cursor():    
    while i<len(Instructions):
        term.clear()
        if Instructions[i][0] in jumpRelated:
            direct.__init__(Instructions[i],i)
            i=direct.makeWay()
        elif len(Instructions[i])==1:
            i+=1
        else:
            direct.__init__(Instructions[i],i)
            direct.makeWay()
            i+=1
        # print(changed)
        print_registers(changed,changed_register)
        print_memory()
        which_instruction = str(Instructions[i])
        print(term.move_xy(0,y_pos+5)+term.on_darkolivegreen(which_instruction)+term.clear_eol)
        y_pos=0
        changed = False

        while term.inkey() == 'KEY_ENTER':
            print("ERROR")
        # inp = term.inkey()

#   RESULTS OF THE SIMULATOR

print(Instructions)
# print(Registers)
# for i in Memory:
#     if i <MemoryIndex:
#         print(i,end=" : ")
#         print(Memory[i])
#     else:
#         break
# print(Memory)
# print(Loops)
# print(Data)
# print(MemoryIndex)

# GUI 

# with term.cbreak(), term.hidden_cursor():    
#     print_registers()
#     print_memory()
#     inp = term.inkey()

