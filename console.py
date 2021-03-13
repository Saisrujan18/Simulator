from blessed import Terminal

term = Terminal()

#first the memory and then the regsiters and then the code

Registers={"$s0":0,"$s1":0,"$s2":0,"$s3":0,"$s4":0,"$s5":0,"$s6":0,"$s7":0,"$t0":0,"$t1":0,"$t2":0,"$t3":0,"$t4":0,"$t5":0,"$t6":0,"$t7":0,"$t8":0,"$t9":0,"$zero":0,"$a0":0,"$a1":0,"$a2":0,"$a3":0,"$v0":0,"$v1":0,"$gp":0,"$fp":0,"$sp":0,"$ra":0,"$at":0}
Memory={268435456+4*i:0 for i in range(1024)}

MemoryIndex = 268435456

y_pos = 0

def print_registers():
    global y_pos
    print(term.move_xy(term.width//2 - 5,2) + "REGISTERS")
    y_pos = 4
    x_pos = 0
    for i in Registers:
        pri = f' {i} : {Registers[i]} '
        if x_pos+len(pri)+2 > term.width:
            x_pos = 0
            y_pos += 2
        print(term.move_xy(x_pos,y_pos) + term.on_darkolivegreen(pri))
        x_pos += len(pri)+2


def print_memory():
    global y_pos
    x_pos = 0
    y_pos += 2
    print(term.move_xy(term.width//2 -3,y_pos) + "MEMORY")
    y_pos+=2
    for i in Memory:
        if i > MemoryIndex:
            break
        print(term.move_xy(x_pos,y_pos) + term.on_darkolivegreen(f' {i} : {Memory[i]} '))
        x_pos += 10
        if x_pos > term.width:
            x_pos = 0
            y_pos += 2



with term.cbreak(), term.hidden_cursor():    
    print_registers()
    print_memory()
    inp = term.inkey()


    #while start() 