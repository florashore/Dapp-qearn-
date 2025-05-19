     START RCTY                ,,, RETURN CARRIAGE
     LOOP  WNTYOLD-19          ,,, LOOP FOR EACH ITERATION
           TFM POS,18
           TF  NEW,NULL
     LOOP2 TFM COUNT,0         ,,, LOOP OVER ROW
           TFM POSMEM,OLD
           S   POSMEM,POS
           TF  PFROM,POSMEM
           SM  PFROM,1
           TF  TEST1+11,PFROM
     TEST1 TD  TEST,PFROM      ,,, TRANSFER DIGIT 1 TO TEST AREA
           A   COUNT,TEST
           AM  PFROM,1
           TF  TEST2+11,PFROM
     TEST2 TD  TEST,PFROM      ,,, TRANSFER DIGIT 2 TO TEST AREA
           A   COUNT,TEST
           AM  PFROM,1
           TF  TEST3+11,PFROM
     TEST3 TD  TEST,PFROM      ,,, TRANSFER DIGIT 3 TO TEST AREA
           A   COUNT,TEST
           CM  COUNT,2         ,,, CHECK IF COUNT EQUALS 2
           BNE ZERO
           TFM POSTO,NEW
           S   POSTO,POS
           TF  FLAG+6,POSTO
     FLAG  TDM POSTO,1
     ZERO  SM  POS,1
           CM  POS,1
           BNE LOOP2           ,,, LOOP UNTIL ROW COMPLETE
           AM  IT,1
           TF  OLD,NEW
           RCTY
           CM  IT,10
           BNE LOOP            ,,, RUN 10 ITERATIONS
           H
     OLD   DC  21,01110110101010100100
           DC  1,@
     NEW   DC  21,0
           DC  1,@
     NULL  DC  21,00000000000000000000
     IT    DC  5,0
     POS   DC  5,0
     POSMEMDC  5,0
     PFROM DC  5,0
     POSTO DC  5,0
     TEST  DC  5,0
     COUNT DC  5,0
           DENDSTART
