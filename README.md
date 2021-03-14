
# SIMULATOR

### Requirements
```
 python version 3.7
 pip 21.0.1
 blessed library 
```
### Installation
```
 pip install blessed
 gh repo clone Saisrujan18/Simulator
```
### Description

Programming language used : Python

Memory supported: 4KB

*Registers*⬇️
```
 "$s0,"$s1","$s2","$s3","$s4","$s5","$s6","$s7",
  "$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$t8","$t9",
  "$zero",
  "$a0","$a1","$a2","$a3",
  "$v0","$v1",
  "$gp","$fp","$sp","$ra","$at",
  "$k0,"$k1"
```
Instructions supported : add , addi , sub , bne , beq , j , lw , sw , la , jal , jr , slt

Data type supported : .word

Additional features :
```
 Implemented basic console GUI
 Supports recursion
 Single and Multi step execution 
```
### Overview

*Run "python start.py" in your terminal.*
*Instructions:*
```
 Press _ENTER_ to execute the next instruction and view the status of registers and memory
 Press _q_ to fast forward the execution , Shows the final state of registers and memory
```

*SneakPeek :*  

![db9afa1b-ecbe-49bd-92e3-0c38d19f378d](https://user-images.githubusercontent.com/68287683/111061326-c1855b00-84c8-11eb-8537-ad9c90f58910.gif)
