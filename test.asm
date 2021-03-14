.data
array:
    .word 2
.text 
.globl main  
main:   
    add $t0,$t0,$t1
    addi $t4,$zero,1
    addi $t2,$zero,2
    add $t0,$t0,$t1
exit:
    add $t0,$t0,$t1
    sub $t2,$t2,$t4
    addi $t0,$t0,1000
    bne $t2,$zero,exit
    j theend
    addi $t0,$t0,1000
theend :
    jr $ra