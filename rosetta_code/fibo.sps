     START RCTY                ,,, RETURN CARRIAGE
     LOOP  BT  FIBO,FIBN       ,,, PASS FIBN VALUE TO FUNCTION FIBO
           AM  FIBN,1          ,,, ADD 1 TO FIBN
           CM  FIBN,20         ,,, LOOP OVER THE FIRST 20 FIBONACCI NUMBERS
           BNE LOOP            ,,, JUMP BACK TO LOOP IF 20 NOT YET REACHED
           H                   ,,, HALT WHEN DONE
     N     DC  5,0             ,,, INPUT VALUE N GOES HERE
     FIBO  CM  FIBO-1,3        ,,, START OF FIBONACCI FUNCTION
           BL  PRINT           ,,, JUMP TO PRINT AND OUTPUT 1 IF N LESS THAN 3
           TFM L2,2            ,,, OTHERWISE SET UP VARIABLES FOR SUMMATION LOOP
           TFM A,1
           TFM B,1
     LOOP2 TFM C,0             ,,, ITERATIVE LOOP FOR SUMMING VALUE
           A   C,A
           A   C,B
           TF  A,B
           TF  B,C
           AM  L2,1
           C   L2,FIBO-1
           BL  LOOP2
           WNTYB-3             ,,, OUTPUT B (SHOWING LAST 4 DIGITS)
           RCTY
           BB                  ,,, BRANCH BACK TO MAIN LOOP
     PRINT WNTYONE-3           ,,, OUTPUT 1
           RCTY
           BB                  ,,, BRANCH BACK TO MAIN LOOP
     FIBN  DC  5,1             ,,, WHICH FIBONACCI NUMBER TO PRINT
     ONE   DC  5,1
           DC  1,@             ,,, ADD A RECORD MARK SO ONE CAN BE PRINTED
     L2    DC  5,0             ,,, LOOP 2 INDEX
     A     DC  5,0
     B     DC  5,0
           DC  1,@             ,,, ADD A RECORD MARK SO B CAN BE PRINTED
     C     DC  5,0
           DENDSTART
