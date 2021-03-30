.data
array:
    .word 2
.text 
.globl main  
main:
    add $t0,$t1,$t2
    add $t3,$t0,$t2
    bne $t0,$t1,exit
    add $t5,$t6,$t7
exit:
    add $t9,$t9,$t9
jumper:   
    add $t5,$t3,$t2