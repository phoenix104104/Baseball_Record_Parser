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

```
type    聯賽名稱
date    yyyy-mm-dd
id      yyyymmdd1
location    比賽場地

AWAY    隊名
Box     0   1   2   3   4   5
姓名/背號  守位  PA  PA  PA
姓名/背號  守位  PA  PA  PA
...

HOME    隊名
Box     0   1   2   3   4   5
姓名/背號  守位  PA  PA  PA
姓名/背號  守位  PA  PA  PA
```

* PA: **(換投/代打/)方位/記錄/註解**
  
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
        FO  界外飛球接殺(Foul Out)
        
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
    - **方位/記錄**
    - **記錄/註解**
    - **方位/記錄/註解**

* 若同一打席同時有換投和換代打，可寫 **換投/代打/PA** 或 **代打/換投/PA**


Input Example
----------
```
type        台大慢壘聯盟
date        2014-01-01
id          201401011
location    萬壽橋

AWAY    化研
Box     4   10  0   4   9
n   1B  R/1B/r   8/2B/r   8/F         8/2B/r  8/2B/2r
7   2B  8/1B/r   9/3B/2r  6/1B/1      5/E/r   BB/r
23  3B  L/1B/1r  7/2B/1r  8/1B/1x*#   7/2B/2r HR/4r
6   P   7/2B/2   7/HR/2r  6/G         7/2B/2  7/2B/r
26  C   6/F/x*   7/2B/r   r31/6/1B    K       rOB/8/1b/1r
24  LF  5/E/r    6/1B/r   7/2B        6/G/#   8/E/r
17  RF  7/1B/1   8/HR/3r  K           8/1B/r  6/1B
21  CF  7/2B/x#* 7/1B/r   6/F/#       6/1B/r  1/1B/1
25  SS  8/1B     6/E/r    8/1B/r      5/F     6/DP/!
3   FF  5/FC/xr  6/1B     rob/k       1/1b/r

HOME    資工
Box     0   1   0   0   2
74  1B  BB      6/F     7/F
36  2B  DP      8/F     BB/r
7   3B  1/F/#   9/3B    8/2B/r
71  SS  6/E/r   1/G/#   8/2B/2
20  C   6/E     p99/8/F 6/G/!
24  P   K       6/G
35  LF  BB      BB
29  CF  K       1/1B
21  RF  1/E     6/FC/x#
77  FF  K/#     1/G
```

Output Example
-------------
* PTT format:

![ScreenShot](https://raw.github.com/phoenix104104/Baseball_Record_Parser/ver2.0/image/ptt_example.jpg)

* statistics:

![ScreenShot](https://raw.github.com/phoenix104104/Baseball_Record_Parser/ver2.0/image/statistics_output.jpg)



