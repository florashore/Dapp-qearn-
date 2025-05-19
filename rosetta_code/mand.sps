     START RCTY                ,,, RETURN CARRIAGE
     LOOPY NOP
           TFL X0,MIN2         ,,, RESET X0 TO -2
           TFM XP,0
           RCTY
     LOOPX NOP
           TFM ITER,0
           TFL X,ZERO
           TFL Y,ZERO
     LOOPI NOP
           TFL X2,X            ,,, CALCULATE X*X AND Y*Y
           FMULX2,X
           TFL Y2,Y
           FMULY2,Y
           TFL XT,X2           ,,, CALCULATE XT
           FSUBXT,Y2
           FADDXT,X0
           TFL XY,X            ,,, CALCULATE 2*X*Y
           FMULXY,Y
           FMULXY,TWO
           TFL Y,Y0            ,,, CALCULATE Y
           FADDY,XY
           TFL X,XT
           TFL Z,X2            ,,, CALCULATE Z
           FADDZ,Y2
           FSUBZ,FOUR          ,,, CHECK IF Z LARGER THAN 4
           CM  Z-2,0
           BH  FAIL
           AM  ITER,1
           CM  ITER,20         ,,, ITERATE 20 TIMES
           BNE LOOPI
           WATYSTAR            ,,, PRINT A STAR
           B   CONT
     FAIL  SPTY                ,,, PRINT A SPACE
     CONT  FADDX0,XD
           AM  XP,1
           CM  XP,76
           BNE LOOPX           ,,, JUMP BACK TO X LOOP
           FADDY0,YD
           AM  YP,1
           CM  YP,31
           BNE LOOPY           ,,, JUMP BACK TO Y LOOP
           H                   ,,, HALT WHEN FINISHED
           DC  6,0
     X     DC  2,0
           DC  6,0
     Y     DC  2,0
           DC  6,0
     X2    DC  2,0
           DC  6,0
     Y2    DC  2,0
           DC  6,0
     XT    DC  2,0
           DC  6,0
     XY    DC  2,0
           DC  6,0
     Z     DC  2,0
           DC  6,-200000
     X0    DC  2,1             ,,, X0 = -2.
           DC  6,-100000
     Y0    DC  2,1             ,,, Y0 = -1.
           DC  6,333333
     XD    DC  2,-1            ,,, XD = .0333
           DC  6,666666
     YD    DC  2,-1            ,,, YD = .0666
           DC  6,200000
     TWO   DC  2,1             ,,, TWO = 2.
           DC  6,0
     ZERO  DC  2,-99           ,,, ZERO = 0.
           DC  6,-200000
     MIN2  DC  2,1             ,,, MIN2 = -2.
     ONE2  DC  2,1             ,,, ONE2 = 01
           DC  6,400000
     FOUR  DC  2,1             ,,, FOUR = 4.
     ITER  DC  5,0             ,,, CURRENT ITERATION
     XP    DC  5,0             ,,, X SCREEN LOCATION
     YP    DC  5,0             ,,, Y SCREEN LOCATION
     STAR  DAC 2,*@            ,,, STAR CHARACTER
           DENDSTART
