# IF = []
# IDRF = []
# EX = []
# MEM = []
# WB = []

# RegStatus={"$s1":0,"$s1":0,"$s2":0,"$s3":0,
#             "$s4":0,"$s5":0,"$s6":0,"$s7":0,"$t1":0,
#             "$t0":0,"$t2":0,"$t3":0,"$t4":0,"$t5":0,
#             "$t6":0,"$t7":0,"$t8":0,"$t9":0,"$zero":0,
#             "$a1e":0,"$a1":0,"$a2":0,"$a3":0,"$v1":0,
#             "$v1":0,"$gp":0,"$fp":0,"$sp":0,"$ra":0,
#             "$at":0,"$k1":0,"$k1":0}

# stageStatus = [True, True, True, True, True]


# def isUpdated(register):
#     global RegStatus
#     return (RegStatus[register] == 0)

# def setStatus(register, status):
#     global RegStatus
#     RegStatus[register] += status


# def isStageAval(stage):
#     global stageStatus
#     return stageStatus[stage]

# def setStageStatus(stage, status):
#     global stageStatus
#     stageStatus[stage] = status

# start = True
# cnt = 0
# isForwardingOn = True
# while start or cnt < 10:
#     jump = -1
#     printing = []
#     if WB != []:
#         if not isForwardingOn and (WB[0] in NormalOperations or WB[0] in MemoryRelated):
#             setStatus(WB[1],-1)
#     printing.append(WB)
    
#     if MEM != []:
#         if MEM[0] not in MemoryRelated:
#             setStageStatus(3,1)
#             WB = copy.deepcopy(MEM)
#         else:
#             pass
#     else:
#         WB = []    
#     printing.append(MEM)
    
#     if EX != []:
#         if EX[0] in ComparisonOperations:
#             # instruction_count += 1
#             # direct.__init__(EX[:-1],EX[-1]) 
#             # C = direct.makeWay()
#             if C == (EX[-1]+1):
#                 pass
#             else:
#                 PC = C
#                 jump = 2
#         if jump != 2:
#             if isStageAval(2):
#                 # call for execution
#                 # direct.__init__(EX[:-1],EX[-1]) 
#                 if isForwardingOn:
#                     if EX[0] in NormalOperations:
#                         if EX[0] != "la":
#                             setStatus(EX[1],-1)
#                 if isStageAval(3):
#                     setStageStatus(2,True)
#                     MEM = copy.deepcopy(EX)
#                 else:
#                     setStageStatus(2,False)
#             else:
#                 if isStageAval(3):
#                     setStageStatus(2,True)
#                     MEM = copy.deepcopy(EX)
#                 else:
#                     setStageStatus(3,False)
#     else:
#         if isStageAval(3):
#             MEM = []
#     printing.append(EX)

#     if IDRF != []:
#         if IDRF[0] in NonComparisionJumps:
#             jump = 1
#             if IDRF[0] == "jr":
#                 PC = Registers["$ra"]
#             else:
#                 PC = Loops[IRDF[1]]
#             setStageStatus(1,False)
#         elif isStageAval(2):
#             if IDRF[0] == "addi":
#                 if isUpdated(IDRF[2]):
#                     setStatus(IDRF[1],1)
#                     setStageStatus(1,True)
#                     EX = copy.deepcopy(IDRF)
#                 else:
#                     EX = []
#                     setStageStatus(1,False)
#             elif IDRF[0] in NormalOperations:
#                 if IDRF[0] != "la":
#                     if isUpdated(IDRF[2]) and isUpdated(IDRF[3]):
#                         setStatus(IDRF[1],1)
#                         print(RegStatus[IDRF[2]],IDRF[2])
#                         setStageStatus(1,True)
#                         EX = copy.deepcopy(IDRF)
#                     else:
#                         EX = []
#                         setStageStatus(1,False)
#             elif IDRF[0] in MemoryRelated:
#                 if IDRF[0] == "lw":
#                     reg = IDRF[-2].find('$')
#                     reg = IDRF[-2][reg:-1]
#                     if isUpdated(reg):
#                         setStatus(IDRF[1],1)
#                         setStageStatus(1,True)
#                         EX = copy.deepcopy(IDRF)
#                     else:
#                         EX = []
#                         setStageStatus(1,False)
#                 if IDRF[0] == "sw":
#                     reg = IDRF[-2].find('$')
#                     reg = IDRF[-2][reg:-1]
#                     if isUpdated(reg) and isUpdated(IRDF[1]):
#                         setStageStatus(1,True)
#                         EX = copy.deepcopy(IDRF)
#                     else:
#                         EX = []
#                         setStageStatus(1,False)
#             elif IDRF[0] in ComparisonOperations:
#                 if isUpdated(IDRF[2]) and isUpdated(IDRF[2]):
#                     setStageStatus(1,True)
#                     setStatus(IDRF[1],1)
#                     EX = copy.deepcopy(IDRF)
#                 else:
#                     EX = []
#                     setStageStatus(1,False)
#     else:
#         if isStageAval(2):
#             EX = []
#     printing.append(IDRF)
#     if IF != [] or start:
#         if isStageAval(0):
#             if PC == len(Instructions):
#                 IF = []
#             else:
#                 IF = copy.deepcopy(Instructions[PC])
#                 PC += 1
#         if isStageAval(1):
#             IDRF = copy.deepcopy(IF)
#             if not isStageAval(0):
#                 setStageStatus(0,True)
#                 # if PC == len(Instructions):
#                 #     IF = []
#                 # else:
#                 #     IF = copy.deepcopy(Instructions[PC])
#                 #     PC += 1
#         else:
#             setStageStatus(0,False)
#     else:
#         if isStageAval(1):
#             IDRF = []
#     printing.append(IF)
#     for i in range(len(printing)-1,-1,-1):
#         print(printing[i],end=" ");
#     print()

#     start = False
#     cnt += 1
#     if jump == 1:
#         setStageStatus(2,True)
#         setStageStatus(1,True)
#         IDRF = []
#         jump = -1
    
#     if jump == 2:
#         IDRF = []
#         EX = []
#         setStageStatus(1,True)
#         setStageStatus(2,True)
#         jump = -1
#         IDRF = []
#         EX = []
#         setStageStatus(1,True)
#         setStageStatus(2,True)
#         jump = -1



# # print(Instructions)

# # RegStatus={"$s0":[0,0],"$s1":[0,0],"$s2":[0,0],"$s3":[0,0],
# #             "$s4":[0,0],"$s5":[0,0],"$s6":[0,0],"$s7":[0,0],"$t0":[0,0],
# #             "$t1":[0,0],"$t2":[0,0],"$t3":[0,0],"$t4":[0,0],"$t5":[0,0],
# #             "$t6":[0,0],"$t7":[0,0],"$t8":[0,0],"$t9":[0,0],"$zero":[0,0],
# #             "$a0":[0,0],"$a1":[0,0],"$a2":[0,0],"$a3":[0,0],"$v0":[0,0],
# #             "$v1":[0,0],"$gp":[0,0],"$fp":[0,0],"$sp":[0,0],"$ra":[0,0],
# #             "$at":[0,0],"$k0":[0,0],"$k1":1}

# # stageStatus = [False,False,False,False,False]

# # class S1:
# #     def __init__(self):
# #         print("",end="")
    
# #     def purpose(self):
# #         global IF,PC,Instructions
# #         if stageStatus[1] == False:
# #             if PC==len(Instructions):
# #                 IF=[]
# #             else:
# #                 IF=copy.deepcopy(Instructions[PC])
# #                 PC+=1
# #         return False

# # wastherestall = False
# # IDRF_prev = 0

# # class S2:
# #     global IDRF # add $r1,$r2,$r3
# #     global Operating
# #     global RegStatus
# #     global first
# #     global PC
# #     global wastherestall
# #     global IDRF_prev
# #     def __init__(self):
# #         print("",end="")
    
# #     def purpose(self,CLOCK):
# #         ## to write for j,jal,jr --> done !!
# #         if wastherestall is True:
# #             if (IDRF_prev) > (CLOCK+1):
# #                 wastherestall = True
# #                 return [True, False]
# #             else:
# #                 wastherestall = False
# #                 return [False, False]

# #         if IDRF != [] and IDRF[0] == "addi":
# #             max_delay = 0
# #             if RegStatus[IDRF[2]][0] > 0:
# #                 max_delay = max(max_delay, RegStatus[IDRF[2]][0])
# #             IDRF_prev = max_delay
# #             RegStatus[IDRF[1]] = [RegStatus[IDRF[1]][0]+1,max(RegStatus[IDRF[1]][1],max(max_delay + 1, (CLOCK + 2) if isForwardingOn else (CLOCK+4)))]
# #         elif IDRF != [] and IDRF[0] in NormalOperations: 
# #             if IDRF[0] == "la":
# #                 RegStatus[IDRF[1]] = [RegStatus[IDRF[1]][1]+1,CLOCK+3 + (0 if isForwardingOn else 1)]
# #                 return [False,False]
# #             max_delay = 0
# #             if RegStatus[IDRF[2]][0] > 0:
# #                 max_delay = max(max_delay, RegStatus[IDRF[2]][1])

# #             if RegStatus[IDRF[3]][0] > 0:
# #                 max_delay = max(max_delay, RegStatus[IDRF[3]][1])
# #             RegStatus[IDRF[1]] = [RegStatus[IDRF[1]][0]+1,max(RegStatus[IDRF[1]][1]+1,max(max_delay + 1,(CLOCK + 2) if isForwardingOn else (CLOCK+4)))]
# #             # if IDRF[0] == "slt":
# #                 # print(max_delay,CLOCK,IDRF)
# #             IDRF_prev = max_delay
# #             stall = (True if max_delay > (CLOCK+1) else False) 
# #             return [stall,False]
        
# #         elif IDRF!= [] and IDRF[0] in MemoryRelated:
# #             if IDRF[0] == "lw":
# #                 reg = IDRF[-2].find('$')
# #                 reg = IDRF[-2][reg:-1]
# #                 RegStatus[IDRF[1]] = [RegStatus[IDRF[1]][0]+1,max(RegStatus[reg][1]+1,CLOCK + 3 + (0 if isForwardingOn else 1))]
# #                 # print(RegStatus[IDRF[1]],CLOCK)
# #             if IDRF[0] == "sw":
# #                 # print(IDRF)
# #                 reg = IDRF[-2].find('$')
# #                 reg = IDRF[-2][reg:-1]
# #                 # reg = "$t1"
# #                 max_delay = 0;
# #                 if RegStatus[reg][0] > 0:
# #                     max_delay =  RegStatus[reg][1]
# #                 IDRF_prev = max_delay
# #                 stall = (True if max_delay > (CLOCK+1) else False)
# #                 return [stall,False]

# #         elif IDRF!=[] and IDRF[0] in ComparisonOperations:
# #             max_delay = 0
# #             if RegStatus[IDRF[1]][0] > 0:
# #                 max_delay = max(max_delay, RegStatus[IDRF[1]][1])
# #             if RegStatus[IDRF[2]][0] > 0:
# #                 max_delay = max(max_delay, RegStatus[IDRF[2]][1])
# #             # print(max_delay,IDRF[1],IDRF[2])
# #             IDRF_prev = max_delay
# #             stall = (True if max_delay > (CLOCK+1) else False)
# #             return [stall,False]
        
# #         elif IDRF!=[] and IDRF[0] in jumpRelated:
# #             if IDRF[0] == "jr":
# #                 PC = Registers["$ra"]
# #                 # if PC > len(Instructions)
# #             else:
# #                 PC = Loops[IDRF[1]]
# #             return [True,True]
# #         return [False,False]
        
# # instruction_count = 0
# # class S3:
# #     global EX,PC,STALLS,instruction_count
# #     global RegStatus
# #     ## to write for bne beq and also call for execute
# #     ## idea -> if true change PC and return to True to stash the current inst
# #     ## Else continue 
# #     def __init__(self):
# #         print("",end="")
    
# #     def purpose(self,CLOCK):
# #         if EX==[]:
# #             return []
# #         whichop=EX[0]
# #         if whichop in NormalOperations or whichop in MemoryRelated:
# #             direct.__init__(EX[:-1],0)
# #             direct.makeWay()
# #         elif whichop in ComparisonOperations:
# #             instruction_count += 1
# #             direct.__init__(EX[:-1],EX[-1])
# #             C=direct.makeWay()
# #             # print(C,"njerer")
# #             if C==(EX[-1]+1):
# #                 pass
# #             else:
# #                 # print(C,"eererer")
# #                 return [True,C]
# #         return []

# # class S4:
# #     def __init__(self):
# #         print("",end="")
    
# #     def purpose(self,CLOCK):
# #         global MEM
# #         global RegStatus
# #         if MEM!=[] and MEM[0] in NormalOperations:
# #             pass
    
# # class S5:
# #     global instruction_count
# #     global IDRF
# #     global RegStatus
# #     def __init__(self):
# #         print("",end="")
    
# #     def purpose(self,CLOCK):
# #         if WB!= [] and WB[0] in NormalOperations:
# #             RegStatus[WB[1]] = [max(0,RegStatus[WB[1]][0]-1),CLOCK+1]
# #         if WB != []:
# #             instruction_count += 1

# # IFER=S1()
# # IDRFER=S2()
# # EXER=S3()
# # MEMER=S4()
# # WBER=S5()

# # Instructions.append(["BYTESPLEASE"])
# # start=True

# # insnum = 0
# # stinst = []

# # okayyy = int(input("Enter \'0\' to disable \"FORWARDING\" else Enter \'1\' : "))
# # print()
# # show= int(input("Enter \'0\' to view \"INSTRUCTIONS\" that are being executed else Enter \'1\' : "))
# # print()
# # def view(x):
# #     if x!=[]:
# #         return x[-1]
# #     return "   "

# # while start==True or WB!=["BYTESPLEASE"]:
# #     isForwardingOn = True if okayyy > 0 else False
# #     start=False
# #     CLOCK+=1
    
# #     isthereastall = False
    
# #     IFER.purpose()
    
# #     if show==0:
# #         print("[{}: {:<3}] , [{}: {:<3}] , [{}: {:<3}] , [{}: {:<3}] , [{}: {:<3}]".format("IF",view(IF),"IDRF",view(IDRF),"EX",view(EX),"MEM",view(MEM),"WB",view(WB)))
# #         # print(IF,IDRF,EX,MEM,WB)
# #     # print(IF)
    
# #     stageStatus[0] = False
        
# #     isthereastall,isjump=IDRFER.purpose(CLOCK)
# #     # print(isthereastall)
# #     stageStatus[1] = False
# #     wastherestall = False
# #     if isjump:        
# #         IF = []
# #         IDRF=[]
# #     elif isthereastall:
# #         wastherestall = True
# #         stageStatus[1] = True
# #         STALLS += 1
# #         # print(IDRF)
# #         stinst.append(IDRF[:-1])
    
# #     ExOutput=EXER.purpose(CLOCK)
    
# #     if ExOutput!=[]:
# #         # STALLS += 1;
# #         # stinst.append(EX[:-1])
# #         RegStatus[IDRF[1]] =[0,0]
# #         PC=ExOutput[-1]
# #         IF=[]
# #         IDRF,EX=[],[]

# #     MEMER.purpose(CLOCK)
    
# #     WBER.purpose(CLOCK)
    
# #     WB=copy.deepcopy(MEM)
# #     MEM=copy.deepcopy(EX)

# #     if stageStatus[2] == False:
# #         if stageStatus[1] == False:
# #             EX=copy.deepcopy(IDRF)
# #         else:
# #             EX=[]
# #     if stageStatus[1] == False:
# #         IDRF=copy.deepcopy(IF)

# # stnewinst = []
# # [stnewinst.append(x) for x in stinst if x not in stnewinst ]

# # print(instruction_count-1,CLOCK-4)
# # print(instruction_count)