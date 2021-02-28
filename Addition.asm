.data
array:
    .word 2
.text
.globl main
main:
    add $t0,$t0,$t1
    add $t0,$t0,$t1
exit:
    add $t0,$t0,$t1
    sub $t0,$t0,$t1
    addi $t0,$t0,1000
    jr $ra