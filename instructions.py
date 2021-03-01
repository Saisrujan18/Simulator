def checkRegister(R):
    return True if R in Registers.keys() else False;

class add:
    # add $t1 $t1 $t1
    # inst[0] inst[1] inst[2] inst[3]
    #     final, a, b
    def __init__(self):
        print("ere")
    def exe(self, inst):
        # if true the syntax is proper
        # check if length is proper
        # then iterate over the last three and checkRegister
        if len(inst)== 4: 
            ok = True
            for i in range(1,4):
                ok = ok and checkRegister(inst[i])
            if ok:
                self.update(inst)
                return
        print("ERROR")
    
    def update(self, inst):
        Registers[inst[1]] = Registers[inst[2]] + Registers[inst[3]]
