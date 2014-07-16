#Baseball_Record_Parser
======================
Usage: 
----------
    ./parse_record.py [-h] -i INPUT_FILE_NAME [-o OUTPUT_FILE_NAME] [-nc]
    
optional:

    -h, --help           show this help message and exit
    -i INPUT_FILE_NAME   Specify input file name
    -o OUTPUT_FILE_NAME  Specify output file name [default: print to screen]
    -nc                  Close color mode [default: on]



Format of input file: 
-----------
(以下所有代號皆不分大小寫)

* PA: **(換投-代打-)方位-記錄-註解**
  
```
    換投:
        p + 背號
    代打: 
        r + 背號
    方位: 
        可以是守備代號(1~10)或L、R、C
    記錄: 
        1B  一壘安打
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
    註解: 
        1~4 打點
        r   得分
        x   出局數(目前這個打席造成的出局數，而非球員出局。例如雙殺打DP要寫兩個x)
        #   換局
        !   比賽結束
        *   補充說明
```        
        
* PA 的寫法可以為 
    - **記錄**
    - **方位-記錄**
    - **記錄-註解**
    - **方位-記錄-註解**

* 若同一打席同時有換投和換代打，可寫 **換投-代打-PA** 或 **代打-換投-PA**


Input Example
----------
```
T1  化研
p   6
1   n   R-1B-r   8-2B-r   8-F-x       8-2B-r  8-2B-2r
2   7   8-1B-r   9-3B-2r  6-1B-1      5-E-r   BB-r
3   23  L-1B-1r  7-2B-1r  8-1B-1x*#   7-2B-2r HR-4r
4   6   7-2B-2   7-HR-2r  6-G-x       7-2B-2  7-2B-r
5   26  6-F-xx*  7-2B-r   r31-6-1B    K-x     rOB-8-1b-1r
6   24  5-E-r    6-1B-r   7-2B        6-G-x#  8-E-r
7   17  7-1B-1   8-HR-3r  K-x         8-1B-r  6-1B
8   21  7-2B-x#* 7-1B-r   6-F-x#      6-1B-r  1-1B-1
9   25  8-1B     6-E-r    8-1B-r      5-F-x   6-DP-xx!
10  3   5-FC-xr  6-1B     rob-k-x     1-1b-r

T2  資工
p   24
1   74  BB      6-F-x   7-F-x
2   36  DP-xx   8-F-x   BB-r
3   7   1-F-x#  9-3B    8-2B-r
4   71  6-E-r   1-G-x#  8-2B-2
5   20  6-E     p99-8-F-x   6-G-x!
6   24  K-x     6-G-x
7   35  BB      BB
8   29  K-x     1-1B
9   21  1-E     6-FC-x#
10  77  K-x#    1-G-x
```

Output Example
-------------
* PTT format:

![ScreenShot](https://raw.github.com/phoenix104104/Baseball_Record_Parser/ver2.0/image/ptt_example.jpg)

* statistics:

![ScreenShot](https://raw.github.com/phoenix104104/Baseball_Record_Parser/ver2.0/image/statistics_output.jpg)



