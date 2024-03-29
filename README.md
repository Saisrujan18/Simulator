
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

__Programming language used__ : Python

__Memory supported__: 4KB

__*Registers*⬇️__
```
 "$s0,"$s1","$s2","$s3","$s4","$s5","$s6","$s7",
  "$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$t8","$t9",
  "$zero",
  "$a0","$a1","$a2","$a3",
  "$v0","$v1",
  "$gp","$fp","$sp","$ra","$at",
  "$k0,"$k1"
```
__Instructions supported__ : add , addi , sub , bne , beq , j , lw , sw , la , jal , jr , slt

__Data type supported__ : .word

__Additional features__ :
```
 Implemented basic console GUI
 Supports RECURSION
 Single and Multi step execution 
```
### Overview

*Run __python start.py__ in your terminal.*
*Instructions:*
```
 Press _ENTER_ to execute the next instruction and view the status of registers and memory
 Press _q_ to fast forward the execution , Shows the final state of registers and memory
```

__*SneakPeek :*__  

![db9afa1b-ecbe-49bd-92e3-0c38d19f378d](https://user-images.githubusercontent.com/68287683/111061326-c1855b00-84c8-11eb-8537-ad9c90f58910.gif)

## Simulator Phase II
1. _Added pipelining to Phase-I_
2. _Takes input to toggle __forwarding__ in the pipeline._
3. _At the end displays,_
   * Number of Stalls
   * Instructions per Cycle
   * List of Instructions which resulted in stalls
   * __NOTE__: branch instructions and jump instructions donot result in stalls(assuming simple branch predictor).

Run __python start2.py__ in your terminal to execute the program.

## Simulator Phase III
1. Changed the prior model of pipeline.
2. Implemented Two Level Cache (LRU Cache).
3. __CacheInput.txt__ contains all the specifications related to the Cache.
4. Results Displayed after Execution:
   * Number of stalls
   * Instructions per Cycle
   * Cache One Miss Rate
   * Cache Two Miss Rate
   * Final contents in Memory and Registers.
5. Run __python start3.py__ in terminal to execute the program.

## User Interface : 

![mipssimss](https://user-images.githubusercontent.com/68287683/120660292-cf81c100-c4a4-11eb-8717-0a740c59b704.PNG)
