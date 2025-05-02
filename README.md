![logo](logo.png "Py1620 logo")

## Py1620 (IBM 1620 emulator)

This [IBM 1620](https://en.wikipedia.org/wiki/IBM_1620) emulator in Python can now run the famous IBM 1620 baseball game (with ```CARD_FILE = "base.txt"```). Also included are the [Computer History Museum](https://computerhistory.org/)'s [Power of Two](https://github.com/IBM-1620/Junior/blob/master/diagnostics/binaries/APP_Power_Of_2.cmem) demo program, 2-D Tic-Tac-Toe (11.0.013; ```CARD_FILE = "tic.txt"```) from the 1620 General Program Library, and "99 Bottles of Beer" by Chuck Guzis (2005; ```CARD_FILE = "beer.txt"```).

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

2**8 = 2̅56



N = 100

2**1̅00 = 1̅267650600228229401496703205376
```

### Tic-Tac-Toe

The program is loaded from the punch card text file. When the computer loses, it will learn the losing move and play differently next time:

![TTT](Tic-Tac-Toe_software_catalog.png "Tic-Tac-Toe in the 1971 software catalog")

```
$ python3 py1620.py

*** System HALT at address 0; please press Return to continue


SQUARES NUMBERED AS FOLLOWS

1  2  3

4  5  6

7  8  9

SW 1 ON FOR DATA,PUSH START
*** System HALT at address 1350; please press Return to continue


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
```

### Credits

The IBM 1403 printer font is available at [ibm-1401.info](http://ibm-1401.info/Sched2008December.html#1403-Font).

[IBM 1620 image](https://commons.wikimedia.org/wiki/File:IBM_1620_console_typewriter.mw.jpg) by Marcin Wichary, CC BY 2.0 <https://creativecommons.org/licenses/by/2.0>, via Wikimedia Commons

### Further reading

* [Basic Programming Concepts and the IBM 1620 Computer](http://www.bitsavers.org/pdf/ibm/1620/Basic_Programming_Concepts_and_the_IBM_1620_Computer_1962.pdf)
