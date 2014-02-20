#Baseball_Record_Parser
======================
Usage: 
----------
    ./parse_record.py [-h] -i INPUT_FILE_NAME [-o OUTPUT_FILE_NAME] [-nc]

* optional arguments:

.. code-block::

    -h, --help           show this help message and exit
    -i INPUT_FILE_NAME   Specify input file name
    -o OUTPUT_FILE_NAME  Specify output file name [default: print to screen]
    -nc                  Close color mode [default: on]



Format of input file: (以下所有代號皆不分大小寫)

PA: (換投-代打-)方位-記錄-註解
  
  代打: r + 背號
  
  方位: 可以是守備代號(1~10)或L、R、C
  
  記錄: 1B  一壘安打
        2B  二壘安打
        3B  三壘安打
        HR  全壘打
        SF  高飛犧牲打
        BB  保送
        K   三振
        G   滾地球出局
        F   飛球出局
        DP  雙殺打
        FC  野手選擇
        E   失誤
        IB  違規擊球(Illegal Batted)
        CB  投手強襲球(combacker)
        IF  內野高飛必死球(Infield Fly)
        
  註解: 1~4 打點
        r   得分
        x   出局數(目前這個打席造成的出局數，而非球員出局。例如雙殺打DP要寫兩個x)
        #   換局
        !   比賽結束
        *   補充說明
        
PA 的寫法可以為 "記錄"
                "方位-記錄"
                "記錄-註解"
                "方位-記錄-註解"

若同一打席同時有換投和換代打，記錄請寫"換投-代打-PA"


example:

T1  資工
p   24
1   74  7-2B-r      8-2B-2r     5-F-x       6-E-r
2   36  3-F-x       10-1B       8-1B-r      1-G-x
3   7   5-G-x       9-2B-1      HR-3r       8-2B-2
4   20  BB          6-1B        2-F-x#      6-G-x!
5   35  9-1B-1      K-x#        K-x
6   24  6-E         6-F-x       7-1B
7   29  10-F-x#     BB          8-1B
8   21  5-1B        K-x         K-x
9   77  BB-r        1-G-x#      K-x#
10  n   K-x         K-x         BB
11  ob  6-1B-xr*    BB-r        8-1B-rx*

T2 OP牙
P   33
1   20  BB-r    K-x     5-G-x
2   25  7-2B-1r 7-2B    10-1B
3   33  K-x     3-F-x   4-F-x#
4   81  6-1B-1  4-F-x#  9-2B-r
5   43  9-1B    9-1B-r  4-F-x
6   40  K-x     7-2B-1r 7-1B
7   47  6-F-x#  10-1B-1 3-E-x*
8   55  5-F-x   7-F-x   1-1B
9   1   1-G-x   K-x     K-x!
10  88  10-F-x# K-x#    
11  66  4-1B    4-F-x

