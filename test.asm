.data
array:
    .word 2
.text 
.globl main  
main:
    la $s0, array
    lw $t0, 0($s0)