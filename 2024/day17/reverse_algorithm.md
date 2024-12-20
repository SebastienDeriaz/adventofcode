# Run algorithm in reverse

## Program

1) 2 BST 4 : B10 = A1 % 8
2) 1 BXL 1 : B11 = B10 ^ 1
3) 7 CDV 5 : C1 = A1 / 2**B11
4) 0 ADV 3 : A2 = A1 / 8
5) 4 BXC 7 : B12 = B11 ^ C1
6) 1 BXL 6 : B13 = B12 ^ 6
7) 5 OUT 5 : B13
8) 3 JNZ 0 : A != 0 -> 0

Output is [2, 4, 1, 1, 7, 5, 0, 3, 4, 7, 1, 6, 5, 5, 3, 0]

## A range

range to get 16 iterations (thus 16 prints)

min value for A : 35184372088832
max value for A : 281474976710655

## Value

B13 = 2
B12 = 4

B11 = B12 ^ C1
C1 = A1 / 2**B11

B10 < 8
B11 < 8
C1 < 8

A1 < 8 * 2**8