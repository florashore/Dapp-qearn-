![logo](logo.png "Py1620 logo")

## Py1620 (IBM 1620 emulator)

This [IBM 1620](https://en.wikipedia.org/wiki/IBM_1620) emulator in Python can now run the famous IBM 1620 baseball game ("base.txt" = newer version; "bbc1.txt" = older version). Also included are the [Computer History Museum](https://computerhistory.org/)'s [Power of Two](https://github.com/IBM-1620/Junior/blob/master/diagnostics/binaries/APP_Power_Of_2.cmem) demo program, 2-D tic-tac-toe (11.0.013; "tic.txt") from the 1620 General Program Library, and "99 Bottles of Beer" by Chuck Guzis (2005; "beer.txt").

The emulated machine is an IBM 1620 Model 1 in its base configuration with 20,000 decimal digits of memory and without any special features (such as divide instructions, indirect or indexed addressing, or floating point instructions). The addition and multiplication tables in 1620 memory are not used but standard Python integer math.

### Usage

```python3 py1620.py input.txt [0000] [output.txt]```

where input.txt is a card reader input file in SIMH format, 0000 are the (optional) sense switch settings, and output.txt is the card punch output file (optional).

E.g., to run the baseball game with sense switch 3 set to on (= play only a single game):

```python3 py1620.py base.txt 0010```

To run the slot machine / one-armed bandit, playing for 50 cents (sense switch 4):

```python3 py1620.py band.txt 0001```

Without any arguments, the tic-tac-toe game is run.

If the ```SLOW``` parameter in line 7 of py1620.py is set to True, terminal output speed will be limited to 10 characters per second like a typewriter on a real IBM 1620. This setting makes sense especially for the baseball game and the 99 bottles of beer demo, because otherwise output will scroll by much too fast to read.

See the [IBM1620-Baseball](https://github.com/mdoege/IBM1620-Baseball) repo for additional IBM 1620 tools and documentation.

### Power of 2

![Py1620](py1620.png "Power of Two output in IBM 1403 font")

The program is loaded from the CMEM file. Computing 2**9999 takes about 18 seconds on a PC, so the program is about 70x as fast as a real IBM 1620.

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

### Block letters on punch cards

The block.txt program outputs block letters on punch cards, with either one or two lines of text on a card and up to 10 characters per line.

Each card is fed into the punch six times: 3x the normal way to print the upper half; then 3x flipped and rotated to print the lower half. When setting the number of cards to 1, this will produce a six-line output file from the emulator.

#### One line of text

```
$ python3 py1620.py block.txt 0000 output1.txt

*** HALT at 0; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

SET CENTERING SWITCHES BEFORE TYPING EACH LINE
SW1 ON-NO UPPER CENTERING	SW2 ON-NO LOWER CENTERING
TEN CHARACTER LIMIT PER LINE

NO. OF 2-LINE SETS-0
	NO. OF 1-LINE SETS-1


1-LINE SETS-
SET NO. 01	FIRST LINE-hello

NO. OF CARDS-1


LOAD 003 CARDS(12-EDGE 1ST, FACE UP)
RELOAD SAME WAY-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

RELOAD SAME WAY-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 


FLIP CARDS(PUT 9-EDGE 1ST, FACE DOWN)-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

RELOAD SAME WAY-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

RELOAD SAME WAY-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 


PUNCHING COMPLETE-PUSH START
*** HALT at 15908; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
```

The program block_decode.py can then be used to show what the finished card would look like:

```
$ python3 block_decode.py output1.txt 
................................................................................
.....................**...**.*******.**......**.......*****.....................
.....................**...**.**......**......**......**...**....................
.....................**...**.**......**......**......**...**....................
.....................**...**.**......**......**......**...**....................
.....................*******.*****...**......**......**...**....................
.....................*******.*****...**......**......**...**....................
.....................**...**.**......**......**......**...**....................
.....................**...**.**......**......**......**...**....................
.....................**...**.**......**......**......**...**....................
.....................**...**.*******.*******.*******..*****.....................
................................................................................
```

#### Two lines of text

```
$ python3 py1620.py block.txt 0000 output2.txt

*** HALT at 0; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

SET CENTERING SWITCHES BEFORE TYPING EACH LINE
SW1 ON-NO UPPER CENTERING	SW2 ON-NO LOWER CENTERING
TEN CHARACTER LIMIT PER LINE

NO. OF 2-LINE SETS-1
	NO. OF 1-LINE SETS-0


2-LINE SETS-
SET NO. 01	FIRST LINE-hello
     SECOND LINE-friends

NO. OF CARDS-1


LOAD 003 CARDS(12-EDGE 1ST, FACE UP)
RELOAD SAME WAY-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

RELOAD SAME WAY-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 


FLIP CARDS(PUT 9-EDGE 1ST, FACE DOWN)-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

RELOAD SAME WAY-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 

RELOAD SAME WAY-PUSH START
*** HALT at 15716; press Return to continue; enter 'h' for help or 'q' to quit
halt> 


PUNCHING COMPLETE-PUSH START
*** HALT at 15908; press Return to continue; enter 'h' for help or 'q' to quit
halt> 
```

Decoding produces:

```
$ python3 block_decode.py output2.txt 
................................................................................
.....................*....*..******..*.......*........****......................
.....................*....*..*.......*.......*.......*....*.....................
.....................******..*****...*.......*.......*....*.....................
.....................*....*..*.......*.......*.......*....*.....................
.....................*....*..******..******..******...****......................
................................................................................
.............******..*****....***....******..*...*...*****....****..............
.............*.......*....*....*.....*.......**..*...*....*..*..................
.............*****...*****.....*.....*****...*.*.*...*....*...****..............
.............*.......*..*......*.....*.......*..**...*....*.......*.............
.............*.......*...*....***....******..*...*...*****....****..............
```

#### Output as PNG images

With block_decode_image.py, the output can also be converted to an image of a punch card (needs PIL):

```
python3 block_decode_image.py output1.txt block_card1.png
python3 block_decode_image.py output2.txt block_card2.png
```

![punch card 1](block_card1.png "punch card 1")

![punch card 2](block_card2.png "punch card 2")

### Credits

The IBM 1403 printer font is available at [ibm-1401.info](http://ibm-1401.info/Sched2008December.html#1403-Font).

[IBM 1620 image](https://commons.wikimedia.org/wiki/File:IBM_1620_console_typewriter.mw.jpg) by Marcin Wichary, CC BY 2.0 <https://creativecommons.org/licenses/by/2.0>, via Wikimedia Commons

IBM punch card  image from [Douglas W. Jones's punched card collection](https://homepage.divms.uiowa.edu/~jones/cards/collection/i-onefield.shtml).

### Further reading

* [Basic Programming Concepts and the IBM 1620 Computer](http://www.bitsavers.org/pdf/ibm/1620/Basic_Programming_Concepts_and_the_IBM_1620_Computer_1962.pdf)
