#!/usr/bin/python

import sys, time
from array import array

DEBUG = False       # log commands to cmd.txt?
SLOW  = False       # realistic output speed (10 cps)?
SINGLE_STEP = False # single-step/manual mode

if len(sys.argv) > 1 and sys.argv[1][-5:] == ".cmem":
    CMEM = True     # read from CMEM file
    CMEM_FILE = sys.argv[1]
else:
    CMEM = False    # read punch card file

# default punch card input file
CARD_FILE = "tic.txt"

if len(sys.argv) > 1:
    CARD_FILE = sys.argv[1]

# default setting of sense switches

SENSE_SW = [False, False, False, False]
if len(sys.argv) > 2:
    if len(sys.argv[2]) != 4:
        print("*** length of sense switch argument is not 4!")
    SENSE_SW = [True if q != "0" else False for q in sys.argv[2]]
    #print(SENSE_SW)

# card punch output file
if len(sys.argv) > 3:
    OUTFILE = open(sys.argv[3], "w")

# CPU trace output file
if DEBUG:
    CMD = open("cmd.txt", "w")  # output trace to text file

MSIZE = 20000   # memory size in decimal digits
sys.set_int_max_str_digits(MSIZE)
PC = 0      # program counter
RM = 10     # record mark
NB = 12     # numeric blank
MAXSHOW = 130       # RAM dump maximum
OVER = "\u0305"     # overbar character
CH_UNDEF = "\u0416" # undefined character
CH_REC = "\u2021"   # record mark double dagger character
CARDNUM = 0         # current card number
BRANCH_BACK = 0     # saved subroutine return address

# define a circular array (because memory on the IBM 1620 is circular)
class MyArray:
    def __init__(s, x):
        s.arr = array('B', [0] * x)
        s.size = x

    def __getitem__(s, x):
        x = x % s.size
        return s.arr[x]

    def __setitem__(s, x, y):
        x = x % s.size
        s.arr[x] = y

# create memory and flag bit arrays
M = MyArray(MSIZE)
F = MyArray(MSIZE)

# create indicator status flags
IND = {}
IND["LASTCARD"] = False
IND["EQ"] = False
IND["HEQ"] = False
IND["HIGH"] = False
IND["OVERFLOW"] = False

# read character codes
alpha = """00  
03 .
04 )
10 +
13 $
14 *
20 -
21 /
23 ,
24 (
33 =
34 @
41 A
42 B
43 C
44 D
45 E
46 F
47 G
48 H
49 I
50 ]
51 J
52 K
53 L
54 M
55 N
56 O
57 P
58 Q
59 R
62 S
63 T
64 U
65 V
66 W
67 X
68 Y
69 Z
70 0
71 1
72 2
73 3
74 4
75 5
76 6
77 7
78 8
79 9"""
almer = {}
for l in alpha.splitlines():
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

# read a punch card line to pos (numeric)
def cardline(pos):
    global CARDNUM, PC

    if IND["LASTCARD"]:
        print("*** no more cards to read, halting at PC =", PC)
        debugger("halt")

    l = CF.readline().rstrip()
    if l == "":
        IND["LASTCARD"] = True
    CARDNUM += 1
    #CMD.write(l + "\n")
    #print("*** reading punch card: ", CARDNUM)
    #print(l, pos)
    for i, x in enumerate(l):
        n = i + pos
        asc = ord(x)
        if x not in "0123456789 JKLMNOPQR ]-/|!@":
            print("*** error: card character not in whitelist:", x)
            sys.exit()
        if 47 < asc < 58:
            val = int(x)
            M[n] = val
            F[n] = 0
        if x == "]" or x == "-":
            M[n] = 0
            F[n] = 1
        if x == "/":
            M[n] = 1
            F[n] = 0
        if x == "|":
            M[n] = RM
            F[n] = 0
        if x == "!":
            M[n] = RM
            F[n] = 1
        if x == "@":
            M[n] = NB
            F[n] = 0
        if x == " ":
            M[n] = 0
            F[n] = 0
        if 73 < asc < 83:
            M[n] = -(73 - asc)
            F[n] = 1

# read a punch card line to pos (alphanumeric)
def cardline_alpha(pos):
    global CARDNUM, PC

    if IND["LASTCARD"]:
        print("*** no more cards to read, halting at PC =", PC)
        debugger("halt")

    l = CF.readline().rstrip()
    if l == "":
        IND["LASTCARD"] = True
    CARDNUM += 1
    #print("*** reading alphanumeric punch card: ", CARDNUM)
    #print(l, pos)
    for i, x in enumerate(l):
        n = 2 * i + pos - 1
        #print(i,x,n)
        if x == "|":
            M[n+1] = RM
            break
        M[n]   = almer[x.upper()][0]
        M[n+1] = almer[x.upper()][1]

# Method 1 to get code into the emulator:
# open a punch card file (in SIMH txt format)
if not CMEM:
    CF = open(CARD_FILE)
    cardline(0)     # read first line from punch card file CF

# Method 2: load a CMEM core file into memory:
if CMEM:
    with open(CMEM_FILE) as cmem:
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
                    if len(y) < 2:
                        y = "0" + y
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

# get immediate value (stopping at flag) as a tuple of (string, sign)
def getimflag(x):
    s = ""
    for i in range(4, -1, -1):
        s = str(M[x + i]) + s
        if F[x + i] and i < 4:
            break
    s = "".join(s)
    if F[x+4]:
        return (s, -1)
    else:
        return (s, 1)

# get number field as a tuple of (string, sign)
def getnum(x, x2 = None):
    s = ""
    if x2 == None:     # no direct address supplied, so get it from x
        x2 = getim(x)
    start = x2
    while True:
        s = str(M[x2]) + s
        if F[x2] and x2 != start: break
        x2 -= 1
    if F[start]:
        return (s, -1)
    else:
        return (s, 1)

# set number field
def setnum(x, val, digits = None, over = False):
    if val < 0:
        s = "%u" % -val
    else:
        s = "%u" % val
    if digits != None:
        digdiff = digits - len(s)
        if digdiff > 0:
            s = "0" * digdiff + s

    sz = max(2, len(s))

    # check if there is enough space for number
    #   and remove extra digits if necessary
    IND["OVERFLOW"] = over
    for n in range(1, sz):
        if M[x-n] == RM:
            IND["OVERFLOW"] = True
            s = s[-n:]
            sz = max(2, len(s))
            break
        if n < sz - 1 and F[x-n]:
            IND["OVERFLOW"] = True
            s = s[-n - 1:]
            sz = max(2, len(s))
            break

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

# debugger prompt
def debugger(prompt = "debug"):
    global SINGLE_STEP, PC

    while True:
        inp = input(prompt + "> ").strip()
        if len(inp) == 0:
            break
        # some debugger commands when system has been halted:
        if inp[0] == "d":   # save memory dump
            dumpmem()
        if inp[0] == "e":   # examine memory
            # "/" means second parameter is an address offset
            if "/" in inp:
                inp = inp.replace("/", " ")
                is_range = True
            else:
                is_range = False
            if "-" in inp:
                inp = inp.replace("-", " ")

            try:    # two addresses
                start, end = [int(_) for _ in inp[1:].split()]
            except: # single location
                start = int(inp[1:])
                end = start

            if is_range:
                end += start - 1
            for i in range(start, end + 1):
                print("%5u: %1u %2u" % (i, F[i], M[i]))
        if inp[0] == "s":   # show current sense switch settings
            sw_out = "".join(["1" if q else "0" for q in SENSE_SW])
            print("sense switches: " + sw_out)
        if inp[0] == "t":   # toggle a sense switch with t1, t2, t3, t4
            sw = int(inp[1])
            SENSE_SW[sw - 1] = not SENSE_SW[sw - 1]
            sw_out = "".join(["1" if q else "0" for q in SENSE_SW])
            print("sense switches now: " + sw_out)
        if inp[0] == "i":   # show indicators
            print(IND)
        if inp[0] == "q":   # quit emulator
            sys.exit()
        if inp[0] == "m":   # manual mode (= single-step mode)
            SINGLE_STEP = True
        if inp[0] == "a":   # auto mode
            SINGLE_STEP = False
        if inp[0] == "g":   # set PC
            PC = int(inp.split()[1])
            print("PC = ", PC)
        if inp[0] == "c":   # continue
            break
        if inp[0] == "h":   # print help
            print("    Available commands when system is halted:")
            print("      d        save memory dump")
            print("      e        examine memory")
            print("      s        show current sense switch settings")
            print("      t        toggle a sense switch with t1, t2, t3, t4")
            print("      i        show indicators")
            print("      m        manual mode (= single-step mode)")
            print("      a        auto mode")
            print("      g        set PC to value")
            print("      c        continue (or just press Return)")
            print("      q        quit emulator")
            print("    PC = %u; print current instruction with: e %u/12" % (PC, PC))

#show()

# check for known op codes
known = (
(2,1),(1,1),(3,3),(4,8),(2,2),(1,2),(3,2),(3,7),(3,6),(3,9),(3,8),
(4,1),(2,6),(1,6),(4,6),(4,9),(4,5),(2,5),(1,5),(4,4),(3,1),(3,4),
(1,4),(4,3),(4,7),(2,4),(1,7),(4,2),(2,3),(1,3),(2,7),(3,5),
(2,8),(2,9),(1,8),(1,9)
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

# set overflow indicator if len(b) > len(a)
def set_over(a, b):
    if len(a) < len(b):
        return True
    else:
        return False

# pretty-print command arguments
def show_args(x):
    out = ""
    for i in range(10):
        out += str(M[x + i])
    out = out[:5] + " " + out[5:]
    return out

def same_sign(a, b):
    if (a < 0 and b < 0) or (a >= 0 and b >= 0):
        return True
    else:
        return False

WATCHED = -1      # watches a memory address for changes if >= 0
WATCH_LAST = -1   # last contents of watched address
BREAKPOINT = -1   # set breakpoints here

while True:

    if WATCHED > -1:    # watch a memory location for changes
        new_watch = "%1u %2u" % (F[WATCHED], M[WATCHED])
        if new_watch != WATCH_LAST:
            if WATCH_LAST == -1:
                WATCH_LAST = new_watch
            else:
                print("*** memory change at", WATCHED, "detected at PC =", PC)
                print("old:", WATCH_LAST)
                print("new:", new_watch)
                WATCH_LAST = new_watch
                debugger("watch")

    if PC == BREAKPOINT:
        dumpmem()
        print("*** breakpoint at PC =", PC)
        debugger("break")

    if DEBUG:
        CMD.write(str(PC) + ": ")
        CMD.write(cmd.get(str(M[PC]) + str(M[PC+1]), "**") + " ")
        for i in range(2, 12):
            CMD.write(str(M[PC+i]))
        CMD.write("\n")
        CMD.flush()

    if SINGLE_STEP:
        print("*** single-step, PC = ", PC, ":", cmd.get(str(M[PC]) + str(M[PC+1])), show_args(PC+2))
        debugger("step")

    OP = M[PC], M[PC+1]

    if OP not in known:
        print()
        print("*** Error: op code not implemented:", M[PC], M[PC+1], show_args(PC+2), "PC = ", PC)
        if DEBUG:
            dumpmem()
        debugger("error")

    # A
    if OP == (2, 1):
        p = getnum(PC+2)
        q = getnum(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        #print("***",p," ",q," ")
        setnum(getim(PC+2), pi + qi, digits = len(p[0]), over = set_over(p[0], q[0]))
        set_ind(pi + qi)

    # AM
    if OP == (1, 1):
        p = getnum(PC+2)
        q = getimflag(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        #print("***",p," ",q," ")
        setnum(getim(PC+2), pi + qi, digits = len(p[0]), over = set_over(p[0], q[0]))
        set_ind(pi + qi)

    # M
    if OP == (2, 3):
        p = getnum(PC+2)
        q = getnum(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        for i in range(80, 100):
            M[i] = 0
            F[i] = 0
        #print("***",p," ",q," ")
        setnum(99, pi * qi, digits = len(p[0]) + len(q[0]))
        set_ind(pi * qi)

    # MM
    if OP == (1, 3):
        p = getnum(PC+2)
        q = getimflag(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        for i in range(80, 100):
            M[i] = 0
            F[i] = 0
        #print("***",p," ",q," ")
        setnum(99, pi * qi, digits = len(p[0]) + len(q[0]))
        set_ind(pi * qi)

    # LD
    if OP == (2, 8):
        p = getim(PC+2)
        q = getim(PC+7)
        start = q
        for i in range(80, 100):
            M[i] = 0
            F[i] = 0
        F[99] = F[q]
        while True:
            M[p] = M[q]
            if (F[q] and q != start):
                F[p] = F[q]
                break
            p -= 1
            q -= 1

    # LDM
    if OP == (1, 8):
        p = getim(PC+2)
        q = PC + 11
        start = q
        for i in range(80, 100):
            M[i] = 0
            F[i] = 0
        F[99] = F[q]
        while True:
            M[p] = M[q]
            if (F[q] and q != start):
                F[p] = F[q]
                break
            p -= 1
            q -= 1

    # D
    if OP == (2, 9):
        p = getnum(0, x2 = 99)
        q = getnum(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        if qi != 0 and int(getnum(PC+2)[0]) / int(q[0]) > 9:
            first_digit = True
        else:
            first_digit = False
        for i in range(80, 100):
            M[i] = 0
            F[i] = 0

        if qi == 0:
            IND["OVERFLOW"] = True
        else:
            d, m = divmod(int(p[0]), int(q[0]))
            m = m * p[1]
            dig_rem = max(2, len(q[0]))
            #print("***",p,q,pi,qi,d,m,dig_rem)
            setnum(99, m, digits = dig_rem)
            if not same_sign(pi, qi):
                d = -d
            setnum(99 - dig_rem, d, digits = len(p[0]), over = set_over(p[0], q[0]))
            set_ind(pi / qi)
            if first_digit:
                IND["OVERFLOW"] = True

    # DM
    if OP == (1, 9):
        p = getnum(0, x2 = 99)
        q = getimflag(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        if qi != 0 and int(getnum(PC+2)[0]) / int(q[0]) > 9:
            first_digit = True
        else:
            first_digit = False
        for i in range(80, 100):
            M[i] = 0
            F[i] = 0

        if qi == 0:
            IND["OVERFLOW"] = True
        else:
            d, m = divmod(int(p[0]), int(q[0]))
            m = m * p[1]
            dig_rem = max(2, len(q[0]))
            #print("***",p,q,pi,qi,d,m,dig_rem)
            setnum(99, m, digits = dig_rem)
            if not same_sign(pi, qi):
                d = -d
            setnum(99 - dig_rem, d, digits = len(p[0]), over = set_over(p[0], q[0]))
            set_ind(pi / qi)
            if first_digit:
                IND["OVERFLOW"] = True

    # CM
    if OP == (1, 4):
        p = getnum(PC+2)
        q = getimflag(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        #print("CM:",p,q)
        if pi > qi:
            IND["HIGH"] = True
        else:
            IND["HIGH"] = False
        if pi == qi:
            IND["EQ"] = True
        else:
            IND["EQ"] = False
        if IND["HIGH"] or IND["EQ"]:
            IND["HEQ"] = True
        else:
            IND["HEQ"] = False

    # C
    if OP == (2, 4):
        p = getnum(PC+2)
        q = getnum(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        if pi > qi:
            IND["HIGH"] = True
        else:
            IND["HIGH"] = False
        if pi == qi:
            IND["EQ"] = True
        else:
            IND["EQ"] = False
        if IND["HIGH"] or IND["EQ"]:
            IND["HEQ"] = True
        else:
            IND["HEQ"] = False
        IND["OVERFLOW"] = False
        if same_sign(pi, qi):
            if len(p[0]) < len(q[0]):
                IND["OVERFLOW"] = True

    # CF
    if OP == (3, 3):
        F[getim(PC+2)] = 0

    # H
    if OP == (4, 8):
        #break
        print()
        print("*** HALT at %u; press Return to continue; enter 'h' for help or 'q' to quit" % PC)
        debugger("halt")
        PC += 12
        continue

    # S
    if OP == (2, 2):
        p = getnum(PC+2)
        q = getnum(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        #print("***",p," ",q," ")
        setnum(getim(PC+2), pi - qi, digits = len(p[0]), over = set_over(p[0], q[0]))
        set_ind(pi - qi)

    # SM
    if OP == (1, 2):
        p = getnum(PC+2)
        q = getimflag(PC+7)
        pi, qi = p[1] * int(p[0]), q[1] * int(q[0])
        #print("***",p," ",q," ")
        setnum(getim(PC+2), pi - qi, digits = len(p[0]), over = set_over(p[0], q[0]))
        set_ind(pi - qi)

    # SF
    if OP == (3, 2):
        F[getim(PC+2)] = 1

    # RA
    if OP == (3, 7):
        n = getim(PC+2)
        dev = M[PC + 9]
        if dev == 5: # (punch card)
            cardline_alpha(n)
        if dev == 1: # TTY
            txt = input()
            txt = txt.strip()
            for x in txt:
                M[n-1] = almer[x.upper()][0]
                M[n] = almer[x.upper()][1]
                n += 2

    # RN
    if OP == (3, 6):
        pos = getim(PC+2)
        dev = M[PC + 9]
        if dev == 5: # (punch card)
            cardline(pos)
            #print("reading", pos)
        if dev == 1: # TTY
            s = input()
            for n, x in enumerate(s):
                M[pos+n] = int(x)

    # WA
    if OP == (3, 9):
        n = getim(PC+2)-1
        dev = M[PC+9]
        if dev == 1:    # TTY
            while True:
                if SLOW:
                    sys.stdout.flush()
                    time.sleep(.1)
                c1, c2 = M[n], M[n+1]
                out = CH_UNDEF      # undefined character
                if c1 == RM or c2 == RM:
                    break
                for k in almer.keys():
                    if almer[k][0] == c1 and almer[k][1] == c2:
                        out = k
                print(out, end="")
                sys.stdout.flush()
                n += 2
        if dev == 4:    # card punch
            while True:
                c1, c2 = M[n], M[n+1]
                out = CH_UNDEF      # undefined character
                if c1 == RM or c2 == RM:
                    break
                for k in almer.keys():
                    if almer[k][0] == c1 and almer[k][1] == c2:
                        out = k
                OUTFILE.write(out)
                n += 2
            OUTFILE.write("\n")
            OUTFILE.flush()

    # WN (TTY)
    if OP == (3, 8):
        n = getim(PC+2)
        while True:
            if SLOW:
                sys.stdout.flush()
                time.sleep(.1)
            if M[n] == RM:
                break
            if F[n]:
                print(str(M[n]) + OVER, end="")
            else:
                print(M[n], end="")
            sys.stdout.flush()
            n += 1

    # DN
    if OP == (3, 5):
        start = getim(PC+2)
        dev = M[PC + 9]
        if dev == 1:    # TTY
            for i in range(start, MSIZE):
                if M[i] == RM:
                    print(CH_REC, end="")
                    continue
                if F[i]:
                    print(str(M[i]) + OVER, end="")
                else:
                    print(M[i], end="")
        if dev == 4:    # punch card
            flagchar = "]JKLMNOPQR"
            for i in range(start, MSIZE):
                if F[i]:
                    OUTFILE.write(flagchar[M[i]])
                else:
                    OUTFILE.write(str(M[i]))
            OUTFILE.write("\n")

    # TF
    if OP == (2, 6):
        p = getim(PC+2)
        q = getim(PC+7)
        start = p
        while True:
            M[p] = M[q]
            F[p] = F[q]
            if (F[q] and p != start):
                break
            p -= 1
            q -= 1

    # TR
    if OP == (3, 1):
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
    if OP == (1, 6):
        p = getim(PC+2)
        q = PC+11
        start = p
        while True:
            M[p] = M[q]
            F[p] = F[q]
            if (F[q] and p != start) or q == PC+7:
                break
            p -= 1
            q -= 1

    # BTM
    if OP == (1, 7):
        pos = getim(PC+2)
        for i in range(4, -1, -1):
            M[pos-5+i] = M[PC+7+i]
            F[pos-5+i] = F[PC+7+i]
            if i < 4 and F[PC+7+i]:
                break
        BRANCH_BACK = PC + 12
        PC = pos
        continue

    # BT
    if OP == (2, 7):
        pos = getim(PC+2)
        q = getim(PC+7)
        i = pos - 1
        while True:
            M[i] = M[q]
            F[i] = F[q]
            if F[i] and i != pos - 1:
                break
            i -= 1
            q -= 1
        BRANCH_BACK = PC + 12
        PC = pos
        continue

    # BB
    if OP == (4, 2):
        PC = BRANCH_BACK
        continue

    # BI
    if OP == (4, 6):
        pos = getim(PC+2)
        dev = 10 * M[PC+8] + M[PC+9]
        #print(dev)
        if dev == 6:
            pass #print("read check", pos)
        elif dev == 7:
            pass #print("write check", pos)
        elif dev == 9:
            #print("card check", PC, pos)
            if IND["LASTCARD"]:
                PC = pos
                continue
        elif dev == 11:
            if IND["HIGH"]:
                PC = pos
                continue
        elif dev == 12:
            if IND["EQ"]:
                PC = pos
                continue
        elif dev == 13:
            if IND["HEQ"]:
                PC = pos
                continue
        elif dev == 14:
            if IND["OVERFLOW"]:
                IND["OVERFLOW"] = False
                PC = pos
                continue
        elif dev == 16:
            pass #print("mem check", pos)
        elif dev == 17:
            pass #print("mem check 2", pos)
        elif dev == 19:
            pass  # GOTRAN needs this check
        elif dev <= 4:
            if dev == 1 and SENSE_SW[0]:
                PC = pos
                continue
            if dev == 2 and SENSE_SW[1]:
                PC = pos
                continue
            if dev == 3 and SENSE_SW[2]:
                PC = pos
                continue
            if dev == 4 and SENSE_SW[3]:
                PC = pos
                continue
        else:
            print("*** BI fail", PC, pos, dev)
            debugger("halt")

    # BNI
    if OP == (4, 7):
        pos = getim(PC+2)
        dev = 10 * M[PC+8] + M[PC+9]
        #print(dev)
        if dev == 6:
            pass #print("read check", pos)
        elif dev == 7:
            pass #print("write check", pos)
        elif dev == 8: # GOTRAN needs this check
            PC = pos
            continue
        elif dev == 9:
            #print("card check", PC, pos)
            if not IND["LASTCARD"]:
                PC = pos
                continue
        elif dev == 11:
            if not IND["HIGH"]:
                PC = pos
                continue
        elif dev == 12:
            if not IND["EQ"]:
                PC = pos
                continue
        elif dev == 13:
            if not IND["HEQ"]:
                PC = pos
                continue
        elif dev == 14:
            if not IND["OVERFLOW"]:
                PC = pos
                continue
            else:
                IND["OVERFLOW"] = False
        elif dev == 16:
            pass #print("mem check", pos)
        elif dev == 17:
            pass #print("mem check 2", pos)
        elif dev <= 4:
            if dev == 1 and not SENSE_SW[0]:
                PC = pos
                continue
            if dev == 2 and not SENSE_SW[1]:
                PC = pos
                continue
            if dev == 3 and not SENSE_SW[2]:
                PC = pos
                continue
            if dev == 4 and not SENSE_SW[3]:
                PC = pos
                continue
        else:
            print("*** BNI fail", PC, pos, dev)
            debugger("halt")

    # B
    if OP == (4, 9):
        pos = getim(PC+2)
        PC = pos
        #print("B PC:", PC)
        continue

    # BD
    if OP == (4, 3):
        pos = getim(PC+2)
        q = getim(PC+7)
        if M[q]:
            #print("BD: ",M[q],PC,pos)
            PC = pos
            continue

    # BNF
    if OP == (4, 4):
        pos = getim(PC+2)
        q = getim(PC+7)
        if not F[q]:
            PC = pos
            continue

    # BNR
    if OP == (4, 5):
        p = getim(PC+2)
        q = getim(PC+7)
        #print(M[PC:PC+12])
        if M[q] != RM:
            PC = p
            continue

    # TD
    if OP == (2, 5):
        p = getim(PC+2)
        q = getim(PC+7)
        M[p] = M[q]
        F[p] = F[q]

    # TDM
    if OP == (1, 5):
        p = getim(PC+2)
        q = getim(PC+7)
        M[p] = abs(q)
        F[p] = F[PC+11]

    # K
    if OP == (3, 4):
        dev = M[PC+9]
        if dev == 1:
            if M[PC+11] == 1:
                print(" ", end="")
            if M[PC+11] == 2:
                print()
            if M[PC+11] == 8:
                print("\t", end="")
            if SLOW:
                sys.stdout.flush()
                time.sleep(.1)

    PC += 12
    #print("new PC: ", PC)
    #show()


