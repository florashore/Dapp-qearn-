     START RCTY
     LOOP  SM  FC,1
           SM  BC,1
           CM  FC,0
           BNE DOBUZ
           WATYFIZZ
           AM  OUT,1
           AM  FC,3
     DOBUZ CM  BC,0
           BNE END
           WATYBUZZ
           AM  OUT,1
           AM  BC,5
     END   CM  OUT,0
           BNE ENDL
           WNTYIT-2
     ENDL  AM  IT,1
           SM  COUNT,1
           TFM OUT,0
           RCTY
           CM  COUNT,0
           BNE LOOP
           H    
     FIZZ  DAC 5,FIZZ@
     BUZZ  DAC 5,BUZZ@
     FC    DC  5,3
     BC    DC  5,5
     OUT   DC  5,0
     IT    DC  5,1
           DC  1,@
     COUNT DC  5,100
           DENDSTART
