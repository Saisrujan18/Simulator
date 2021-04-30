.data
array:
    .word 2
.text 
.globl main  
main:
    addi $t0,$t0,1
    add $t3,$t0,$t2
    beq $t0,$t1,exit