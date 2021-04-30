
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

MemoryRelated=["lw","sw"]


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
        # print(noe)
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
        self.data=[]
        for i in range(self.blocksize):
            self.data.append(base+i*4)
    
    def replace(self,address):
        global LruCounter
        self.LruIndex=LruCounter+1
        LruCounter+=1
        newaddress=self.data[0][0]
        base=BaseAddress(address)
        self.baseAddress=base
        self.data=[]
        for i in range(self.blocksize):
            self.data.append(base+i*4)
        return newaddress

    def search(self,address):
        if len(self.data)==0:
            return False
        bamse=BaseAddress(address)
        if self.data[0]==bamse:
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
        print(self.instructions,offset)
        Registers[self.instructions[1]]=Memory[ requiredAddress ]
        # print(requiredAddress)
        latennn = (Intel.process(requiredAddress))
        print("latennn :",latennn)
        return latennn

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
            return self.lwer.check()
        elif operation=="sw":
            self.swer.__init__(self.current)
            return self.swer.check()
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


# PHASE 2 SPECIAL FUNCTIONS
PC=InstructionsStartFrom
Operating={}
# print(Instructions)

IF = []
IDRF = []
EX = []
MEM = []
WB = []

# Following are declarations are related to phase II.
# For each stage we have a container which holds the instruction.
# The Following loop mimics each clock cycle.
# We give a reserved status to some register which helps to deal with stalling.
# A register can be reserved when its value is still not updated either due to a memory operation
# or due to some pending computation or pending WB or due to some already reserved resgister.
# To show a stall we pass on a null container to that stage.


RegStatus={"$s0":0,"$s1":0,"$s2":0,"$s3":0,
            "$s4":0,"$s5":0,"$s6":0,"$s7":0,"$t1":0,
            "$t0":0,"$t2":0,"$t3":0,"$t4":0,"$t5":0,
            "$t6":0,"$t7":0,"$t8":0,"$t9":0,"$zero":0,
            "$a1e":0,"$a1":0,"$a2":0,"$a3":0,"$v1":0,
            "$v1":0,"$gp":0,"$fp":0,"$sp":0,"$ra":0,
            "$at":0,"$k1":0,"$k1":0}

stageStatus = [True, True, True, True, True]

start = True
cnt = 0


def isUpdated(register):
    global RegStatus
    return (RegStatus[register] == 0)

def setStatus(register, status):
    global RegStatus
    RegStatus[register] += status


def isStageAval(stage):
    global stageStatus
    return stageStatus[stage] or (stageStatus[stage] > 0) 

def setStageStatus(stage, status):
    global stageStatus
    stageStatus[stage] = status

def addStall(inc):
    global STALLS
    STALLS += inc


Mem_stalls = 0
CPC = -1

while start or MEM!= [] or WB!=[] or IF!=[] or IDRF!=[] or EX!=[]:
    jump = -1
    printing = []
    if WB != []:
        if not isForwardingOn and (WB[0] in NormalOperations or WB[0] in MemoryRelated):
            setStatus(WB[1],-1)
    printing.append(WB)
    
    if MEM != []:
        if Mem_stalls > 0:
            setStageStatus(3,0)
            Mem_stalls -= 1
            if Mem_stalls == 0:
                if isForwardingOn:
                    setStatus(MEM[1],-1)
            if isStageAval(4):
                WB = []
        else:
            if MEM[0] not in MemoryRelated:
                setStageStatus(3,1)
                WB = copy.deepcopy(MEM)
            else:
                direct.__init__(MEM[:-1],MEM[-1])       ## MEM ACCESS
                print(MEM)
                get_stalls = direct.makeWay()
                setStatus(MEM[1],1)                       ## Reserving the register for x CCycles.
                print(get_stalls)
                setStageStatus(3,0)
    else:
        WB = []    
    printing.append(MEM)
    
    if EX != []:
        if EX[0] in ComparisonOperations:
            # instruction_count += 1
            direct.__init__(EX[:-1],EX[-1]) 
            C = direct.makeWay()
            # print("C : EX",C, EX[-1])
            if C == (EX[-1]+1):
                pass
            else:
                CPC = C
                jump = 2
                if isStageAval(3):
                    MEM = [] 
        if jump != 2:
            if isStageAval(2):
                # call for execution
                direct.__init__(EX[:-1],EX[-1]) 
                direct.makeWay()
                if isForwardingOn:
                    if EX[0] in NormalOperations:
                            setStatus(EX[1],-1)
                if EX[0] == "la":
                    setStatus(EX[1],-1)
                if isStageAval(3):
                    setStageStatus(2,True)
                    MEM = copy.deepcopy(EX)
                else:
                    setStageStatus(2,False)
            else:
                if isStageAval(3):
                    setStageStatus(2,True)
                    MEM = copy.deepcopy(EX)
                else:
                    setStageStatus(3,False)
    else:
        if isStageAval(3):
            MEM = []
    printing.append(EX)

    if IDRF != []:
        if IDRF[0] in NonComparisionJumps:
            jump = 1
            if IDRF[0] == "jr":
                CPC = Registers["$ra"]
            else:
                CPC = Loops[IDRF[1]]
            setStageStatus(1,False)
            if isStageAval(2):
                EX = []
        if jump != 1:
            if isStageAval(2):
                if IDRF[0] == "addi":
                    if isUpdated(IDRF[2]):
                        setStatus(IDRF[1],1)
                        setStageStatus(1,True)
                        EX = copy.deepcopy(IDRF)
                    else:
                        EX = []
                        setStageStatus(1,False)
                elif IDRF[0] in NormalOperations:
                    if IDRF[0] != "la":
                        if isUpdated(IDRF[2]) and isUpdated(IDRF[3]):
                            setStatus(IDRF[1],1)
                            # print(RegStatus[IDRF[2]],IDRF[2])
                            setStageStatus(1,True)
                            EX = copy.deepcopy(IDRF)
                        else:
                            EX = []
                            setStageStatus(1,False)
                    else:
                        EX = copy.deepcopy(IF)
                        setStatus(IDRF[1], 1)
                        setStageStatus(1,True)
                elif IDRF[0] in MemoryRelated:
                    if IDRF[0] == "lw":
                        reg = IDRF[-2].find('$')
                        reg = IDRF[-2][reg:-1]
                        if isUpdated(reg):
                            setStatus(IDRF[1],1)
                            setStageStatus(1,True)
                            EX = copy.deepcopy(IDRF)
                        else:
                            EX = []
                            setStageStatus(1,False)
                    if IDRF[0] == "sw":
                        reg = IDRF[-2].find('$')
                        reg = IDRF[-2][reg:-1]
                        if isUpdated(reg) and isUpdated(IRDF[1]):
                            setStageStatus(1,True)
                            EX = copy.deepcopy(IDRF)
                        else:
                            EX = []
                            setStageStatus(1,False)
                elif IDRF[0] in ComparisonOperations:
                    if isUpdated(IDRF[2]) and isUpdated(IDRF[2]):
                        setStageStatus(1,True)
                        setStatus(IDRF[1],1)
                        EX = copy.deepcopy(IDRF)
                    else:
                        EX = []
                        setStageStatus(1,False)
    else:
        if isStageAval(2):
            EX = []
    printing.append(IDRF)
    
    if IF != [] or start:
        if isStageAval(0):
            if PC == len(Instructions):
                IF = []
            else:
                IF = copy.deepcopy(Instructions[PC])
                PC += 1
        if isStageAval(1):
            IDRF = copy.deepcopy(IF)
            if not isStageAval(0):
                setStageStatus(0,True)
                # if PC == len(Instructions):
                #     IF = []
                # else:
                #     IF = copy.deepcopy(Instructions[PC])
                #     PC += 1
        else:
            setStageStatus(0,False)
    else:
        if isStageAval(1):
            IDRF = [] 
    printing.append(IF)

    for i in range(len(printing)-1,-1,-1):
        print(printing[i],end=" ");
    print()

    start = False
    cnt += 1
    if jump == 1:
        setStageStatus(2,True)
        setStageStatus(1,True)
        IDRF = []
        jump = -1
        PC = CPC
    
    if jump == 2:
        IDRF = []
        EX = []
        setStageStatus(1,True)
        setStageStatus(2,True)
        if isStageAval(3):
            MEM = []
        PC = CPC
        jump = -1

# stnewinst = []
# [stnewinst.append(x) for x in stinst if x not in stnewinst ]


# for i in range(NumberOfSets):
#     for j in range(NumberOfBlocks):
#         print()
#         print(len(Intel.LevelOneCache.setters[i].blockers[j].data))
#         print()
#         print(Intel.LevelOneCache.setters[i].blockers[j].data)

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