.data
array: 
    .word 100, 2, 1, 5, 10, 8
.text 
.globl main
main:   
    addi $t0,$t0,24  # n
    addi $t1,$t1,20  # n - 1
    addi $t2,$t2,0  # iterator = i 
    addi $t4,$t4,4 
    la $s0, array
    # sw $t1, 0($s0)
loop1:
    beq $t2,$t0,exit # i == n
    la $s0,array
    # addi $s0,$zero,0
    addi $t3,$zero,0  # j = 0 
loop2:
    beq $t3,$t1,exitloop2
    lw $t5, 0($s0)
    lw $t6, 4($s0)
    slt $v0,$t6,$t5 # if a[j+1] < a[j]       
    bne $v0,$zero,swap
    addi $t3,$t3,4
    addi $s0,$s0,4
    j loop2                     
swap:
    sw $t5,4($s0)
    sw $t6,0($s0)
    addi $t3,$t3,4
    addi $s0,$s0,4
    j loop2
exitloop2:
    addi $t2,$t2,4
    sub $t1,$t1,$t4
    j loop1
exit:
    jr $ra