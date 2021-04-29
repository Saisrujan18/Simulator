
# IMPORTING ALL THE LIBRARIES
from collections import OrderedDict

import re
import sys
import copy
import math

# ELEPHANT IN THE ROOM

Instructions=[]

operations=['add','addi','sub','bne','beq','j',"lw","sw","la","jal","jr","slt"]

NormalOperations=["add","addi","sub","la","slt"]

ComparisonOperations=["beq","bne"]

NonComparisionJumps=["j",'jal','jr']

jumpRelated=["j","beq","bne","jal","jr"]

MemoryRelated=["lw","sw","la"]


Registers={"$zero":0,"$at":0,"$v0":0,"$v1":0,"$a0":0,"$a1":0,"$a2":0,"$a3":0,"$t0":0,"$t1":0,"$t2":0,"$t3":0,"$t4":0,"$t5":0,"$t6":0,"$t7":0,"$s0":0,"$s1":0,"$s2":0,"$s3":0,"$s4":0,"$s5":0,"$s6":0,"$s7":0,"$t8":0,"$t9":0,"$k0":0,"$k1":1,"$gp":0,"$sp":0,"$s8":0,"$ra":0}

Loops={}

Memory={268435456+4*i:0 for i in range(1024)}

Data={}

MemoryIndex=268435456

Stackpointer=1023*4+268435456

IF,IDRF,EX,MEM,WB=[],[],[],[],[] 

BufferRegisters=[0,0,0,0,0]

STALLS,CLOCK=0,0

isForwardingOn=False

LruCounter=0

# 268435456 = 0x10000000

NumberOfSets=0
NumberOfBlocks=0
NumberOfElements=0
CacheOneLatency=0
CahceTwoLatency=0
MainMemoryLatency=0

with open("CacheInput") as f:
    CacheInput= f.readlines()

CacheOneLatency=int(CacheInput[-3])
CacheTwoLatency=int(CacheInput[-2])
MainMemoryLatency=int(CacheInput[-1])
NumberOfBlocks=int(CacheInput[-4])

NumberOfElements=int(CacheInput[1])//4 
NumberOfSets=int(CacheInput[0])//(NumberOfBlocks*int(CacheInput[1]))

# print(NumberOfBlocks,NumberOfElements,NumberOfSets)


offsetBits=int(math.log(NumberOfElements,2))
indexBits=int(math.log(NumberOfSets,2))

NumberOfElements=2**offsetBits
NumberOfSets=2**indexBits

HitsCacheOne=0
TotalCacheOne=0
HitsCacheTwo=0
TotalCacheTwo=0


# FEW HELPFULL FUNCTIONS 

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

def getIndex(address):
    temp=address>>(offsetBits+2)
    answer=temp%(2**indexBits) 
    # print(address,answer)
    return answer

def BaseAddress(address):
    temp=address>>(offsetBits+2)
    return temp<<(offsetBits+2)


class block:
    LruIndex=0
    blocksize=0
    data=[]
    def __init__(self,noe):
        self.LruIndex=0
        self.occupied=False
        self.blocksize=noe
        self.baseAddress=-1
    
    def insert(self,address):
        global LruCounter
        self.LruIndex=LruCounter+1
        LruCounter+=1
        base=BaseAddress(address)
        self.baseAddress=base
        for i in range(self.blocksize):
            self.data.append([base+i*0,Memory[base+i*0]])
    
    def replace(self,address):
        global LruCounter
        self.LruIndex=LruCounter+1
        LruCounter+=1
        newaddress=self.data[0][0]
        base=BaseAddress(address)
        self.baseAddress=base
        for i in range(self.blocksize):
            self.data.append([base+i*0,Memory[base+i*0]])
        return newaddress

    def search(self,address):
        if len(self.data)==0:
            return False
        bamse=BaseAddress(address)
        for i in range(self.blocksize):
            if self.data[i][0]==bamse:
                return True
        return False
    
    def update(self):
        global LruCounter
        self.LruIndex=LruCounter+1
        LruCounter+=1

class set:
    def __init__(self,numberofBlocks,numberOfdata,unique):
        self.blockers=[block(numberOfdata) for i in range(numberofBlocks)]
        self.index=unique
    
    def insert(self,address):
        temp=self.isAnyOneFree()
        if temp==-1:
            # all are occupied
            self.blockers.sort(key = lambda x:x.LruIndex)
            newaddress=self.blockers[0].replace(address)
            return newaddress
        self.blockers[temp].insert(address)
        return -1
    
    def isAnyOneFree(self):
        for i in range(len(self.blockers)):
            if self.blockers[i].occupied==False:
                return i
        return -1

    def search(self,address):
        for i in range(len(self.blockers)):
            if self.blockers[i].search(address)==True:
                return True
        return False

    def update(self,address):
        base=BaseAddress(address)
        for i in range(len(self.blockers)):
            if self.blockers[i].baseAddress==base:
                self.blockers[i].update()
                break

class cache:

    def __init__(self,numberOfSets,numberOfblocks,numberofDataElements,laten):
        self.setters=[set(numberOfblocks,numberofDataElements,i) for i in range(numberOfSets)]
        self.latency=laten

    def insert(self,address):
        whichset=getIndex(address)
        return self.setters[whichset].insert(address)

    def search(self,address):
        whichset=getIndex(address)
        return self.setters[whichset].search(address)   

    def update(self,address):
        whichset=getIndex(address)
        self.setters[whichset].update(address)   

class Processor:

    def __init__(self,numberOfSets,numberOfblocks,numberofDataElements,L1latency,L2latency):
        self.LevelOneCache=cache(numberOfSets,numberOfblocks,numberofDataElements,L1latency)
        self.LevelTwoCache=cache(numberOfSets,2*numberOfblocks,numberofDataElements,L2latency)
   
    def process(self,address):
        global TotalCacheOne,TotalCacheTwo,HitsCacheOne,HitsCacheTwo
        TotalCacheOne+=1
        # print(address,BaseAddress(address))
        if self.LevelOneCache.search(address)==True:
            HitsCacheOne+=1
            self.LevelOneCache.update(address)
            return self.LevelOneCache.latency
        TotalCacheTwo+=1
        if self.LevelTwoCache.search(address)==True:
            HitsCacheTwo+=1
            # print("l2",address,BaseAddress(address))
            newaddress=self.LevelOneCache.insert(address)
            if newaddress!=-1:
                # indication to add to L2
                random=self.LevelTwoCache.insert(newaddress)
            return self.LevelOneCache.latency+self.LevelTwoCache.latency
        
        newaddress=self.LevelOneCache.insert(address)
        if newaddress!=-1:
            # indication to add to L2
            random=self.LevelTwoCache.insert(newaddress)
        return self.LevelOneCache.latency+self.LevelTwoCache.latency+MainMemoryLatency

Intel=Processor(NumberOfSets,NumberOfBlocks,NumberOfElements,CacheOneLatency,CacheTwoLatency)


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
        requiredAddress=(offset//4)*4 +Registers[self.instructions[-1]]
        Registers[self.instructions[1]]=Memory[ requiredAddress ]
        # print(requiredAddress)
        return Intel.process(requiredAddress)

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
        requiredAddress= (offset//4)*4 +Registers[self.instructions[-1]] 
        Memory[requiredAddress]=Registers[self.instructions[1]]
        return Intel.process(requiredAddress)

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
# Bubblesort
with open("Bubblesort.asm") as f:
    Instructions= f.readlines()

#   SPLITING EACHLINE ACCORDINGLY

for i in range(len(Instructions)):
    Instructions[i]=re.split(" |,|:|\n",Instructions[i])
    while "" in Instructions[i]:
        Instructions[i].remove('')
 
#   REMOVING COMMENTS FROM THE FILE 

for i in range(len(Instructions)):
    for j in range(len(Instructions[i])):
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

# CHECKING CORRECTNESS

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
Instructions=Instructions[whereisgloblmain:]
InstructionsStartFrom=0

# #############################################################################
itr=0
while True:
    if len(Instructions[itr])==1:
        Loops.update({Instructions[itr][0]:itr})
        Instructions.pop(itr)
    itr+=1
    if itr>=len(Instructions):
        break

# #############################################################################


UpdateReturnAddress()
direct=control([],0)

for i in range(len(Instructions)):
    Instructions[i].append(i)


#   HEART OF THE SIMULATOR
#   GUI USING CONSOLE

# PHASE 2 SPECIAL FUNCTIONS
PC=InstructionsStartFrom
Operating={}
# print(Instructions)

RegStatus={"$s0":[0,0],"$s1":[0,0],"$s2":[0,0],"$s3":[0,0],
            "$s4":[0,0],"$s5":[0,0],"$s6":[0,0],"$s7":[0,0],"$t0":[0,0],
            "$t1":[0,0],"$t2":[0,0],"$t3":[0,0],"$t4":[0,0],"$t5":[0,0],
            "$t6":[0,0],"$t7":[0,0],"$t8":[0,0],"$t9":[0,0],"$zero":[0,0],
            "$a0":[0,0],"$a1":[0,0],"$a2":[0,0],"$a3":[0,0],"$v0":[0,0],
            "$v1":[0,0],"$gp":[0,0],"$fp":[0,0],"$sp":[0,0],"$ra":[0,0],
            "$at":[0,0],"$k0":[0,0],"$k1":1}

stageStatus = [False,False,False,False,False]

class S1:
    def __init__(self):
        print("",end="")
    
    def purpose(self):
        global IF,PC,Instructions
        if stageStatus[1] == False:
            if PC==len(Instructions):
                IF=[]
            else:
                IF=copy.deepcopy(Instructions[PC])
                PC+=1
        return False

wastherestall = False
IDRF_prev = 0

class S2:
    def __init__(self):
        print("",end="")
    
    def purpose(self,CLOCK):
        global IDRF # add $r1,$r2,$r3
        global Operating
        global RegStatus
        global first
        global PC
        global wastherestall
        global IDRF_prev
        ## to write for j,jal,jr --> done !!
        if wastherestall is True:
            if (IDRF_prev) > (CLOCK+1):
                wastherestall = True
                return [True, False]
            else:
                wastherestall = False
                return [False, False]

        if IDRF != [] and IDRF[0] == "addi":
            max_delay = 0
            if RegStatus[IDRF[2]][0] > 0:
                max_delay = max(max_delay, RegStatus[IDRF[2]][0])
            IDRF_prev = max_delay
            RegStatus[IDRF[1]] = [RegStatus[IDRF[1]][0]+1,max(RegStatus[IDRF[1]][1],max(max_delay + 1, (CLOCK + 2) if isForwardingOn else (CLOCK+4)))]
        elif IDRF != [] and IDRF[0] in NormalOperations: 
            if IDRF[0] == "la":
                RegStatus[IDRF[1]] = [RegStatus[IDRF[1]][1]+1,CLOCK+3 + (0 if isForwardingOn else 1)]
                return [False,False]
            max_delay = 0
            if RegStatus[IDRF[2]][0] > 0:
                max_delay = max(max_delay, RegStatus[IDRF[2]][1])

            if RegStatus[IDRF[3]][0] > 0:
                max_delay = max(max_delay, RegStatus[IDRF[3]][1])
            RegStatus[IDRF[1]] = [RegStatus[IDRF[1]][0]+1,max(RegStatus[IDRF[1]][1]+1,max(max_delay + 1,(CLOCK + 2) if isForwardingOn else (CLOCK+4)))]
            # if IDRF[0] == "slt":
                # print(max_delay,CLOCK,IDRF)
            IDRF_prev = max_delay
            stall = (True if max_delay > (CLOCK+1) else False) 
            return [stall,False]
        
        elif IDRF!= [] and IDRF[0] in MemoryRelated:
            if IDRF[0] == "lw":
                reg = IDRF[-2].find('$')
                reg = IDRF[-2][reg:-1]
                RegStatus[IDRF[1]] = [RegStatus[IDRF[1]][0]+1,max(RegStatus[reg][1]+1,CLOCK + 3 + (0 if isForwardingOn else 1))]
                # print(RegStatus[IDRF[1]],CLOCK)
            if IDRF[0] == "sw":
                # print(IDRF)
                reg = IDRF[-2].find('$')
                reg = IDRF[-2][reg:-1]
                # reg = "$t1"
                max_delay = 0;
                if RegStatus[reg][0] > 0:
                    max_delay =  RegStatus[reg][1]
                IDRF_prev = max_delay
                stall = (True if max_delay > (CLOCK+1) else False)
                return [stall,False]

        elif IDRF!=[] and IDRF[0] in ComparisonOperations:
            max_delay = 0
            if RegStatus[IDRF[1]][0] > 0:
                max_delay = max(max_delay, RegStatus[IDRF[1]][1])
            if RegStatus[IDRF[2]][0] > 0:
                max_delay = max(max_delay, RegStatus[IDRF[2]][1])
            # print(max_delay,IDRF[1],IDRF[2])
            IDRF_prev = max_delay
            stall = (True if max_delay > (CLOCK+1) else False)
            return [stall,False]
        
        elif IDRF!=[] and IDRF[0] in jumpRelated:
            if IDRF[0] == "jr":
                PC = Registers["$ra"]
                # if PC > len(Instructions)
            else:
                PC = Loops[IDRF[1]]
            return [True,True]
        return [False,False]
        
instruction_count = 0
class S3:
  
    ## to write for bne beq and also call for execute
    ## idea -> if true change PC and return to True to stash the current inst
    ## Else continue 
    def __init__(self):
        print("",end="")
    
    def purpose(self,CLOCK):
        global EX,PC,STALLS,instruction_count
        global RegStatus
        if EX==[]:
            return []
        whichop=EX[0]
        if whichop in NormalOperations or whichop in MemoryRelated:
            direct.__init__(EX[:-1],0)
            direct.makeWay()
        elif whichop in ComparisonOperations:
            instruction_count += 1
            direct.__init__(EX[:-1],EX[-1])
            C=direct.makeWay()
            # print(C,"njerer")
            if C==(EX[-1]+1):
                pass
            else:
                # print(C,"eererer")
                return [True,C]
        return []

class S4:
    def __init__(self):
        print("",end="")
    
    def purpose(self,CLOCK):
        global MEM
        global RegStatus
        if MEM!=[] and MEM[0] in NormalOperations:
            pass
    
class S5:
    def __init__(self):
        print("",end="")
    
    def purpose(self,CLOCK):
        global instruction_count
        global IDRF
        global RegStatus
        if WB!= [] and WB[0] in NormalOperations:
            RegStatus[WB[1]] = [max(0,RegStatus[WB[1]][0]-1),CLOCK+1]
        if WB != []:
            instruction_count += 1

IFER=S1()
IDRFER=S2()
EXER=S3()
MEMER=S4()
WBER=S5()

Instructions.append(["BYTESPLEASE"])
start=True

insnum = 0
stinst = []

okayyy = int(input("Enter \'0\' to disable \"FORWARDING\" else Enter \'1\' : "))
print()
show= int(input("Enter \'0\' to view \"INSTRUCTIONS\" that are being executed else Enter \'1\' : "))
print()
def view(x):
    if x!=[]:
        return x[-1]
    return "   "

while start==True or WB!=["BYTESPLEASE"]:
    isForwardingOn = True if okayyy > 0 else False
    start=False
    CLOCK+=1
    
    isthereastall = False
    
    IFER.purpose()
    
    if show==0:
        print("[{}: {:<3}] , [{}: {:<3}] , [{}: {:<3}] , [{}: {:<3}] , [{}: {:<3}]".format("IF",view(IF),"IDRF",view(IDRF),"EX",view(EX),"MEM",view(MEM),"WB",view(WB)))
        # print(IF,IDRF,EX,MEM,WB)
    # print(IF)
    
    stageStatus[0] = False
        
    isthereastall,isjump=IDRFER.purpose(CLOCK)
    # print(isthereastall)
    stageStatus[1] = False
    wastherestall = False
    if isjump:        
        IF = []
        IDRF=[]
    elif isthereastall:
        wastherestall = True
        stageStatus[1] = True
        STALLS += 1
        # print(IDRF)
        stinst.append(IDRF[:-1])
    
    ExOutput=EXER.purpose(CLOCK)
    
    if ExOutput!=[]:
        # STALLS += 1;
        # stinst.append(EX[:-1])
        RegStatus[IDRF[1]] =[0,0]
        PC=ExOutput[-1]
        IF=[]
        IDRF,EX=[],[]

    MEMER.purpose(CLOCK)
    
    WBER.purpose(CLOCK)
    
    WB=copy.deepcopy(MEM)
    MEM=copy.deepcopy(EX)

    if stageStatus[2] == False:
        if stageStatus[1] == False:
            EX=copy.deepcopy(IDRF)
        else:
            EX=[]
    if stageStatus[1] == False:
        IDRF=copy.deepcopy(IF)

stnewinst = []
[stnewinst.append(x) for x in stinst if x not in stnewinst ]

# print(instruction_count-1,CLOCK-4)
# print(instruction_count)


#################################################################################

print()
print("{:-^100s}".format("REGISTERS"))
print()
itr=0
for i in Registers:
    print("R{:3} {:7} = {}".format(str(itr),"["+str(i)+"]",Registers[i]))
    itr+=1
print()
print("{:-^100s}".format(""))
print("{:-^100s}".format("MEMORY"))
print()
for i in Memory:
    if i<MemoryIndex:
        print("{:13} : {}".format(str(i),str(Memory[i])))
    else:
        break
print()
print("{:-^100s}".format(""))
print("{:-^100s}".format(""))
print()

print("{:27} : {}".format("Number of Stalls",str(STALLS)))
print()
print("{:27} :".format("Instructions Per Count"), end=" ")
print((instruction_count-1)/(CLOCK-4))
print()
print("Instruction causing Stalls  :")
print("\n")
for i in range(len(stnewinst)):
    x=", ".join(stnewinst[i])
    print(x)
    print()

print("{:-^100s}".format(""))

# print(HitsCacheOne,TotalCacheOne)
# print(HitsCacheTwo,TotalCacheTwo)