#!/usr/bin/python

# Decode output from blocks program

import sys

t = open(sys.argv[1]).readlines()

co = """ 
] 11-0
@ 4-8
* 11-4-8
| 0-2-8
! 11-2-8
} 0-7-8
" 12-7-8
. 12-3-8
) 12-4-8
+ 12
$ 11-3-8
* 11-4-8
- 11
/ 0-1
, 0-3-8
( 0-4-8
= 3-8
A 12-1
B 12-2
C 12-3
D 12-4
E 12-5
F 12-6
G 12-7
H 12-8
I 12-9
J 11-1
K 11-2
L 11-3
M 11-4
N 11-5
O 11-6
P 11-7
Q 11-8
R 11-9
S 0-2
T 0-3
U 0-4
V 0-5
W 0-6
X 0-7
Y 0-8
Z 0-9
0 0
0 12-0
1 1
2 2
3 3
4 4
5 5
6 6
7 7
8 8
9 9
"""

nholes = 12, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

def holes(x):
    for l in co.splitlines():
        if l[0] == x:
            c, h = l.split()
            hh = h.split("-")
            return [int(_) for _ in hh]

card = [["."] * 80 for _ in range(12)]
#print(card)

CARDN = 0
for l in t:
    l = l.rstrip()
    if len(l) == 0: continue
    CARDN += 1
    for x in range(len(l)):
        if l[x] != " ":
            h = holes(l[x])
            for y in range(12):
                if nholes[y] in h:
                    if CARDN <= 3:
                        card[y][x] = "*"
                    else:
                        card[11-y][x] = "*"

for y in range(12):
    for x in range(80):
        print(card[y][x], end = "")
    print()


