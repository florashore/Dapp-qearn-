![logo](logo.png "Py1620 logo")

## Py1620 (IBM 1620 emulator)

This [IBM 1620](https://en.wikipedia.org/wiki/IBM_1620) emulator in Python can now run the famous IBM 1620 baseball game ("base.txt" = newer version; "bbc1.txt" = older version). Also included are the [Computer History Museum](https://computerhistory.org/)'s [Power of Two](https://github.com/IBM-1620/Junior/blob/master/diagnostics/binaries/APP_Power_Of_2.cmem) demo program, 2-D tic-tac-toe (11.0.013; "tic.txt") from the 1620 General Program Library, and "99 Bottles of Beer" by Chuck Guzis (2005; "beer.txt").

### Usage

```python3 py1620.py [card deck input file] [sense switch settings (optional)]```

E.g., to run the baseball game with sense switch 3 set to on (= play only a single game):

```python3 py1620.py base.txt 0010```

To run the slot machine / one-armed bandit, playing for 50 cents (sense switch 4):

```python3 py1620.py band.txt 0001```

Without any arguments, the tic-tac-toe game is run.

If the "SLOW" parameter in line 7 of py1620.py is set to True, terminal output speed will be limited to 10 characters per second like a typewriter on a real IBM 1620.

See the [IBM1620-Baseball](https://github.com/mdoege/IBM1620-Baseball) repo for additional IBM 1620 tools and documentation.

### Power of 2

![Py1620](py1620.png "Power of Two output in IBM 1403 font")

The program is loaded from the CMEM file. The addition and multiplication tables in 1620 memory are not used but standard Python integer math. Computing 2**9999 takes about 18 seconds on a PC, so the program is about 70x as fast as a real IBM 1620.

Overbars for the flag bit are printed using Unicode combining characters and may not look good (e.g. be shifted horizontally) with some fonts.

Also see this [YouTube video](https://www.youtube.com/watch?v=e4JH26yF_u0) of Power of Two running on the [1620 Junior](https://github.com/IBM-1620) emulator.

```
$ python3 py1620.py pow

POWER OF 2 CALCULATOR

N = 8

2**8 = 256



N = 100

2**100 = 1267650600228229401496703205376
```

### Tic-Tac-Toe (default program)

The program is loaded from the punch card text file. When the computer loses, it will learn the losing move and play differently next time:

![TTT](Tic-Tac-Toe_software_catalog.png "Tic-Tac-Toe in the 1971 software catalog")

```
$ python3 py1620.py

*** HALT at 0; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

SQUARES NUMBERED AS FOLLOWS

1  2  3

4  5  6

7  8  9

SW 1 ON FOR DATA,PUSH START
*** HALT at 1350; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

NEW GAME
YOUR PLAY 5
   MY PLAY IS 1
YOUR PLAY 2
   MY PLAY IS 8
YOUR PLAY 9
   MY PLAY IS 3
YOUR PLAY 6
   MY PLAY IS 4
YOUR PLAY 7
 TIE GAME
NEW GAME
YOUR PLAY 
```

### One-armed bandit

Setting all sense switches to off (with "t4" in the debugger in the run below) prints your account balance and resets the account to zero:
```
$ python3 py1620.py band.txt 0001

TYPE A 10-DIGIT NUMBER, THEN HIT RELEASE + START.
1234512345


HERE ARE THE PAYOFFS. . .
Ж  Ж  Ж    PAYS THE JACKPOT. . .  YOU WIN A 1620.
$  $  $    PAYS 20 TO 1,
X  X  X    PAYS 12 TO 1,
Ж  Ж  X    PAYS  8 TO 1,
$  $  X    PAYS  5 TO 1,
Ж  X  X    PAYS  2 TO 1, AND
$  X  X    PAYS  1 TO 1.
     X REPRESENTS ANY SYMBOL OTHER THAN Ж OR $.

TO PLAY FOR NICKELS, TURN ON SWITCH 1.
TO PLAY FOR DIMES, TURN ON SWITCH 2.
TO PLAY FOR QUARTERS, TURN ON SWITCH 3.
TO PLAY FOR HALVES, TURN ON SWITCH 4.

TO CHANGE PLAYERS AT ANY TIME, TURN ALL SWITCHES OFF AND HIT START.

TO SPIN THE WHEELS, PUSH START WITH GREAT VIGOR.

*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
=   Ж   Ж

*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
+   Ж   @

*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
*   *   *	YOU WIN  $6.00

*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
+   @   =

*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
*   @   *

*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
@   =   +

*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
$   $   =	YOU WIN  $2.50

*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> t4
sense switches now: 0000
halt> 

YOU WON $5.00

CHECK SWITCHES FOR YOUR BET.
TO SPIN THE WHEELS, PUSH START WITH GREAT VIGOR.



*** HALT at 1838; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
```

### 99 Bottles of Beer

```
$ python3 py1620.py beer.txt 

*** HALT at 0; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

99 BOTTLES OF BEER ON THE WALL.
99 BOTTLES OF BEER.
TAKE ONE DOWN, PASS IT AROUND -
98 BOTTLES OF BEER ON THE WALL.

98 BOTTLES OF BEER ON THE WALL.
98 BOTTLES OF BEER.
TAKE ONE DOWN, PASS IT AROUND -
97 BOTTLES OF BEER ON THE WALL.

97 BOTTLES OF BEER ON THE WALL.
97 BOTTLES OF BEER.
TAKE ONE DOWN, PASS IT AROUND -
96 BOTTLES OF BEER ON THE WALL.

96 BOTTLES OF BEER ON THE WALL.
96 BOTTLES OF BEER.
TAKE ONE DOWN, PASS IT AROUND -
95 BOTTLES OF BEER ON THE WALL.

95 BOTTLES OF BEER ON THE WALL.
95 BOTTLES OF BEER.
TAKE ONE DOWN, PASS IT AROUND -
94 BOTTLES OF BEER ON THE WALL.

…………………and many beers later:

3 BOTTLES OF BEER ON THE WALL.
3 BOTTLES OF BEER.
TAKE ONE DOWN, PASS IT AROUND -
2 BOTTLES OF BEER ON THE WALL.

2 BOTTLES OF BEER ON THE WALL.
2 BOTTLES OF BEER.
TAKE ONE DOWN, PASS IT AROUND -
1 BOTTLE OF BEER ON THE WALL.

1 BOTTLE OF BEER ON THE WALL.
1 BOTTLE OF BEER.
TAKE ONE DOWN, PASS IT AROUND -
NO MORE BEER.

*** HALT at 606; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
```

### Credits

The IBM 1403 printer font is available at [ibm-1401.info](http://ibm-1401.info/Sched2008December.html#1403-Font).

[IBM 1620 image](https://commons.wikimedia.org/wiki/File:IBM_1620_console_typewriter.mw.jpg) by Marcin Wichary, CC BY 2.0 <https://creativecommons.org/licenses/by/2.0>, via Wikimedia Commons

### Further reading

* [Basic Programming Concepts and the IBM 1620 Computer](http://www.bitsavers.org/pdf/ibm/1620/Basic_Programming_Concepts_and_the_IBM_1620_Computer_1962.pdf)
