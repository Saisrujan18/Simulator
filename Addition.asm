.data
array:
    .word 2
ones:.word 2
.text ; eieufwu
.globl main  ; uuu
; ewfw
main:   
    add $t0,$t0,$t1
    addi $t4,$zero,1 # sdjfhsdjf
    addi $t2,$zero,2
    add $t0,$t0,$t1
exit:
    add $t0,$t0,$t1
    sub $t2,$t2,$t4
    addi $t0,$t0,1000
    bne $t2,$zero,exit
    lw $t7,4($t6)
    sw $t7,8($t6)
    j theend
    addi $t0,$t0,1000
theend :
    jr $ra