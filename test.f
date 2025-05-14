      X=0
      PRINT 3
 3    FORMAT (36H           X      SIN(X)      COS(X))
      DO 1 I=1,10
      Y=SIN(X)
      Z=COS(X)
      PRINT 2,X,Y,Z
 2    FORMAT (3F12.6)
 1    X=X+.3
      END
