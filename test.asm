.data
array: 
    .word 100, 2, 1, 5, 10, 8
.text 
.globl main

main:
    add $t1,$t1,$t2
    add $t2, $t1, $t1