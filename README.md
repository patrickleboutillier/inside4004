# inside4004

An RTL-level simulator for the Intel MCS-4 system, including the 4004 microprocesor, written in Python.

    $ ./141-PF.sh 
    ### DP[0] RND[F] ( )( )( ): h

    Keyboard (enter a sequence of keys and press enter):

                    a     d--------  r--
                                
                    S     7  8  9    -  #         CM   
                    EX    4  5  6    +  /    %    RM
                    CE    1  2  3       *    M+   M-
                    CL    0     .     =      M=+  M=-

    a:  Paper feed button   d:  Decimal point selector   r:   Round off switch
    S:  Minus sign                                       CM:  Clear memory
    EX: Exchange                                         RM:  Recall memory
    CE: Clear entry         M+:  Memory +                M-:  Memory -
    CL: Clear               M=+: Memory equals +         M=-: Memory equals -

    Status line:

        ### DP[0] RND[F] ( )( )( ):
            |      |   |  |  |
            |      |   |  |  ----> Memory light          
            |      |   |  -------> Negative light
            |      |   ----------> Overflow light
            |      --------------> Rounding mode (F:float, R:round, T:truncate)
            ---------------------> Decimal points (0-8) 

    ### DP[0] RND[F] ( )( )( ): 2+
    >>>  |              2 +     |
    ### DP[0] RND[F] ( )( )( ): 2+
    >>>  |              2 +     |
    ### DP[0] RND[F] ( )( )( ): =
    >>>  |              4    *  |
    >>>  |                      |
    ### DP[0] RND[F] ( )( )( ): q
