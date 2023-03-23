#!/usr/bin/python

import sys
from array import array

if len(sys.argv) > 1 and sys.argv[1] == "pow":
    CMEM = True     # read from CMEM file
else:
    CMEM = False    # read punch card file

MSIZE = 20000   # memory size in decimal digits
sys.set_int_max_str_digits(MSIZE)
PC = 0      # program counter
RM = 10     # record mark
NB = 12     # numeric blank
MAXSHOW = 130       # RAM dump maximum
OVER = "\u0305"     # overbar character
CARDNUM = 0         # current card number
CMD = open("cmd.txt", "w")  # output trace to text file
BRANCH_BACK = 0     # saved subroutine return address

# create memory and flag bit arrays
M = array('H', [0] * MSIZE)
F = array('H', [0] * MSIZE)

# create indicator status flags
IND = {}
IND["LASTCARD"] = False
IND["EQ"] = False
IND["HEQ"] = False
IND["HIGH"] = False

# read character codes
almer = {}
with open("alpha.txt") as alpha:
    for l in alpha:
        almer[l[3]] = int(l[0]), int(l[1])

# read op codes for printing trace to cmd.txt
c = """21 A
11 AM
22 S
12 SM
23 M
13 MM
28 LD
18 LDM
29 D
19 DM
25 TD
15 TDM
26 TF
16 TFM
31 TR
72 TNS
73 TNF
24 C
14 CM
49 B
44 BNF
45 BNR
43 BD
46 BI
47 BNI
27 BT
17 BTM
42 BB
36 RN
38 WN
35 DN
37 RA
39 WA
34 K
32 SF
33 CF
71 MF
48 H
41 NOP"""
cmd = {}
for l in c.splitlines():
    x,y = l.split(" ")
    cmd[x] = y.strip()

# read a punch card line to pos
def cardline(pos):
    global CARDNUM, PC

    if IND["LASTCARD"]:
        print("no more cards to read, halting at PC =", PC)
        sys.exit()
        #PC = 402
        #return

    l = CF.readline().strip()
    if l == "":
        IND["LASTCARD"] = True
    CARDNUM += 1
    #print("*** reading punch card: ", CARDNUM)
    #print(l, pos)
    for i, x in enumerate(l):
        n = i + pos
        asc = ord(x)
        if 47 < asc < 58:
            val = int(x)
            M[n] = val
            F[n] = 0
        if x == "]":
            M[n] = 0
            F[n] = 1
        if x == "|":
            #print("RM ***************", n)
            M[n] = RM
            F[n] = 0
        if x == "!":
            M[n] = RM
            F[n] = 1
        if x == "@" or x == " ":
            M[n] = NB
            F[n] = 0
        if 73 < asc < 83:
            M[n] = -(73 - asc)
            F[n] = 1

# Method 1 to get code into the emulator:
# open a punch card file (in SIMH txt format)
if not CMEM:
    CF = open("tic.txt")
    cardline(0)     # read first line from punch card file CF

# Method 2: load a CMEM core file into memory:
if CMEM:
    with open("APP_Power_Of_2.cmem") as cmem:
        for l in cmem:
            l = l.strip()
            if l == "": continue
            l = l.split("/")[0]
            if len(l) < 7: continue
            if l[5] == ":":
                x = int(l[:5])
                v = l[7:].split()
                for n, y in enumerate(v):
                    y = y.strip()
                    F[x+n] = int(y[0])
                    M[x+n] = int(y[1], 16)

# get immediate value
def getim(x):
    s = [str(M[q+x]) for q in range(5)]
    s = "".join(s)
    val = int(s)
    if F[x+4]:
        return -val
    else:
        return val

# get number field
def getnum(x):
    s = ""
    x2 = getim(x)
    while True:
        s = str(M[x2]) + s
        if F[x2] and x2 != x: break
        x2 -= 1
    val = int(s)
    if F[getim(x)]:
        return -val
    else:
        return val

# set number field
def setnum(x, val):
    if val < 0:
        s = "%u" % -val
    else:
        s = "%u" % val
    sz = max(2, len(s))
    for n in range(sz):
        M[x-n] = 0
        F[x-n] = 0
    for n in range(len(s)):
        M[x-n] = int(s[-n-1])
    F[x-sz+1] = 1
    if val < 0:
        F[x] = 1
    else:
        F[x] = 0

# print start of memory
def show():
    print("       ", end="")
    for n in range(MAXSHOW // 10):
        print(str(n)[-1] + 9 * " " , end="")
    print()
    print("%5u: " % PC, end="")
    for n in range(MAXSHOW):
        if F[n]:
            print(hex(M[n])[2:] + OVER, end="")
        else:
            print(hex(M[n])[2:], end="")
    print()

# dump memory as PNG image, green = non-zero, blue = flag bit
def dumpmem():
    from PIL import Image
    x, y = 80, 250
    im = Image.new("RGB", (x, y))
    g = open("mem.txt", "w")
    for j in range(y):
        for i in range(x):
            z = x * j + i
            im.putpixel((i, j), (0, 255 * M[z], 255 * F[z]))
            #g.write("%5u: %2u\n" % (z, M[z]))
            g.write("%u:\t%u%s\n" % (z, F[z], hex(M[z]).upper()[2:] ))
    im.save("dump.png")

#show()

# check for known op codes
known = (
(2,1),(1,1),(3,3),(4,8),(2,2),(1,2),(3,2),(3,7),(3,6),(3,9),(3,8),
(4,1),(2,6),(1,6),(4,6),(4,9),(4,5),(2,5),(1,5),(4,4),(3,1),(3,4),
(1,4),(4,3),(4,7),(2,4),(1,7),(4,2),(2,3),(1,3)
)

# set indicators
def set_ind(x):
    if x > 0:
        IND["HIGH"] = True
    else:
        IND["HIGH"] = False
    if x == 0:
        IND["EQ"] = True
    else:
        IND["EQ"] = False
    if IND["HIGH"] or IND["EQ"]:
        IND["HEQ"] = True
    else:
        IND["HEQ"] = False

while True:
    if 0: #PC == 232:   # set breakpoint
        dumpmem()
        sys.exit()

    CMD.write(str(PC) + ": ")
    CMD.write(cmd.get(str(M[PC]) + str(M[PC+1]), "**") + " ")
    for i in range(2, 12):
        CMD.write(str(M[PC+i]))
    CMD.write("\n")
    if (M[PC], M[PC+1]) not in known:
        print()
        print("*** Error: op code not implemented:", M[PC], M[PC+1], M[PC+2:PC+12], "PC = ", PC)
        dumpmem()
        sys.exit()
    # A
    if M[PC] == 2 and M[PC+1] == 1:
        p = getnum(PC+2)
        q = getnum(PC+7)
        #print("***",p," ",q," ")
        setnum(getim(PC+2), p + q)
        set_ind(p + q)

    # AM
    if M[PC] == 1 and M[PC+1] == 1:
        p = getnum(PC+2)
        q = getim(PC+7)
        #print("***",p," ",q," ")
        setnum(getim(PC+2), p + q)
        set_ind(p + q)

    # M
    if M[PC] == 2 and M[PC+1] == 3:
        p = getnum(PC+2)
        q = getnum(PC+7)
        #print("***",p," ",q," ")
        setnum(99, p * q)
        set_ind(p * q)

    # MM
    if M[PC] == 1 and M[PC+1] == 3:
        p = getnum(PC+2)
        q = getim(PC+7)
        #print("***",p," ",q," ")
        setnum(99, p * q)
        set_ind(p * q)

    # CM
    if M[PC] == 1 and M[PC+1] == 4:
        p = getnum(PC+2)
        q = getim(PC+7)
        #print("CM:",p,q)
        if p > q:
            IND["HIGH"] = True
        else:
            IND["HIGH"] = False
        if p == q:
            IND["EQ"] = True
        else:
            IND["EQ"] = False
        if IND["HIGH"] or IND["EQ"]:
            IND["HEQ"] = True
        else:
            IND["HEQ"] = False

    # C
    if M[PC] == 2 and M[PC+1] == 4:
        p = getnum(PC+2)
        q = getnum(PC+7)
        if p > q:
            IND["HIGH"] = True
        else:
            IND["HIGH"] = False
        if p == q:
            IND["EQ"] = True
        else:
            IND["EQ"] = False
        if IND["HIGH"] or IND["EQ"]:
            IND["HEQ"] = True
        else:
            IND["HEQ"] = False

    # CF
    if M[PC] == 3 and M[PC+1] == 3:
        F[getim(PC+2)] = 0

    # H
    if M[PC] == 4 and M[PC+1] == 8:
        #break
        print()
        print("*** auto-resume from HALT at", PC)
        PC += 12
        continue

    # S
    if M[PC] == 2 and M[PC+1] == 2:
        p = getnum(PC+2)
        q = getnum(PC+7)
        #print("***",p," ",q," ")
        setnum(getim(PC+2), p - q)
        set_ind(p - q)

    # SM
    if M[PC] == 1 and M[PC+1] == 2:
        p = getnum(PC+2)
        q = getim(PC+7)
        #print("SM: ",p," ",q," ")
        setnum(getim(PC+2), p - q)
        set_ind(p - q)

    # SF
    if M[PC] == 3 and M[PC+1] == 2:
        F[getim(PC+2)] = 1

    # RA (TTY)
    if M[PC] == 3 and M[PC+1] == 7:
        n = getim(PC+2)
        txt = input()
        txt = txt.strip()
        for x in txt:
            M[n-1] = almer[x.upper()][0]
            M[n] = almer[x.upper()][1]
            n += 2

    # RN
    if M[PC] == 3 and M[PC+1] == 6:
        pos = getim(PC+2)
        dev = str(getim(PC+7))[-3]
        if dev == "5": # (punch card)
            cardline(pos)
            #print("reading", pos)
        if dev == "1": # TTY
            s = input()
            for n, x in enumerate(s):
                M[pos+n] = int(x)

    # WA (TTY)
    if M[PC] == 3 and M[PC+1] == 9:
        n = getim(PC+2)-1
        while True:
            c1, c2 = M[n], M[n+1]
            out = " "
            if c1 == RM or c2 == RM:
                break
            for k in almer.keys():
                if almer[k][0] == c1 and almer[k][1] == c2:
                    out = k
            print(out, end="")
            n += 2
        #print()

    # WN (TTY)
    if M[PC] == 3 and M[PC+1] == 8:
        n = getim(PC+2)
        while True:
            if M[n] == RM:
                #print()
                break
            if F[n]:
                print(str(M[n]) + OVER, end="")
            else:
                print(M[n], end="")
            n += 1

    # TF
    if M[PC] == 2 and M[PC+1] == 6:
        p = getim(PC+2)
        q = getim(PC+7)
        while True:
            M[p] = M[q]
            F[p] = F[q]
            if F[q]:
                break
            p -= 1
            q -= 1

    # TR
    if M[PC] == 3 and M[PC+1] == 1:
        p = getim(PC+2)
        q = getim(PC+7)
        #print("TR: ", p, q)
        while True:
            M[p] = M[q]
            F[p] = F[q]
            if M[q] == RM:
                break
            p += 1
            q += 1

    # TFM
    if M[PC] == 1 and M[PC+1] == 6:
        p = getim(PC+2)
        q = PC+11
        while True:
            M[p] = M[q]
            F[p] = F[q]
            if F[q] or q == PC+7:
                break
            p -= 1
            q -= 1

    # BTM
    if M[PC] == 1 and M[PC+1] == 7:
        pos = getim(PC+2)
        q = getim(PC+7)
        for n, i in enumerate("%05u" % q):
            M[pos-5+n] = int(i)
        F[pos-5] = 1
        BRANCH_BACK = PC + 12
        PC = pos
        continue

    # BB
    if M[PC] == 4 and M[PC+1] == 2:
        PC = BRANCH_BACK
        continue

    # BI
    if M[PC] == 4 and M[PC+1] == 6:
        pos = getim(PC+2)
        dev = getim(PC+7)
        #print(dev)
        if dev == 600:
            pass #print("read check", pos)
        elif dev == 700:
            pass #print("write check", pos)
        elif dev == 900:
            #print("card check", PC, pos)
            if IND["LASTCARD"]:
                PC = pos
                continue
        elif dev == 1100:
            if IND["HIGH"]:
                PC = pos
                continue
        elif dev == 1200:
            if IND["EQ"]:
                PC = pos
                continue
        elif dev == 1300:
            if IND["HEQ"]:
                PC = pos
                continue
        elif dev == 1400:
            pass #print("overflow check", pos)
        elif dev == 1600:
            pass #print("mem check", pos)
        elif dev == 1700:
            pass #print("mem check 2", pos)
        elif dev <= 400:
            pass #print("sense", pos)
        else:
            print("BI fail", pos, dev)
            sys.exit(0)

    # BNI
    if M[PC] == 4 and M[PC+1] == 7:
        pos = getim(PC+2)
        dev = getim(PC+7)
        jump = True
        #print(dev)
        if dev == 600:
            pass #print("read check", pos)
        elif dev == 700:
            pass #print("write check", pos)
        elif dev == 900:
            #print("card check", PC, pos)
            if not IND["LASTCARD"]:
                PC = pos
                continue
        elif dev == 1100:
            if not IND["HIGH"]:
                PC = pos
                continue
        elif dev == 1200:
            if not IND["EQ"]:
                PC = pos
                continue
        elif dev == 1300:
            if not IND["HEQ"]:
                PC = pos
                continue
        elif dev == 1400:
            pass #print("overflow check", pos)
        elif dev == 1600:
            pass #print("mem check", pos)
        elif dev == 1700:
            pass #print("mem check 2", pos)
        elif dev <= 400:
            pass #print("sense", pos)
        else:
            print("BNI fail", pos, dev)
            sys.exit(0)

    # B
    if M[PC] == 4 and M[PC+1] == 9:
        pos = getim(PC+2)
        PC = pos
        #print("B PC:", PC)
        continue

    # BD
    if M[PC] == 4 and M[PC+1] == 3:
        pos = getim(PC+2)
        q = getim(PC+7)
        if M[q]:
            #print("BD: ",M[q],PC,pos)
            PC = pos
            continue

    # BNF
    if M[PC] == 4 and M[PC+1] == 4:
        pos = getim(PC+2)
        q = getim(PC+7)
        if not F[q]:
            PC = pos
            continue

    # BNR
    if M[PC] == 4 and M[PC+1] == 5:
        p = getim(PC+2)
        q = getim(PC+7)
        #print(M[PC:PC+12])
        q = q%20000 # *** is this really needed?
        if M[q] != RM:
            PC = p
            continue

    # TD
    if M[PC] == 2 and M[PC+1] == 5:
        p = getim(PC+2)
        q = getim(PC+7)
        M[p] = M[q]
        F[p] = F[q]

    # TDM
    if M[PC] == 1 and M[PC+1] == 5:
        p = getim(PC+2)
        q = getim(PC+7)
        M[p] = q
        F[p] = F[PC+11]

    # K
    if M[PC] == 3 and M[PC+1] == 4:
        q = getim(PC+7)
        if q == 101:
            print(" ", end="")
        if q == 102:
            print()
        if q == 108:
            print("\t", end="")

    PC += 12
    #print("new PC: ", PC)
    #show()


