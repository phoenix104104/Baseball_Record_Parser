#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os
import argparse

class PA:
    def __init__(self, isPlay, pos=0, result=0, rbi=0, run=0, endInning=0, note=0):
        self.isPlay     = isPlay    # used for no-play batter
        self.pos        = pos       # hit-ball direction
        self.result     = result    # result
        self.rbi        = rbi       # RBI
        self.run        = run       # RUN
        self.endInning  = endInning # should be 0, '#' or '!'
        self.note       = note      # 0 or *'
        self.inning     = -1
        self.column     = -1

    def SetInning(self, inning, column):
        self.inning     = inning    # inning
        self.column     = column    # column position in the PTT format

class Batter:
    def __init__(self, order, number):
        self.order  = order
        self.number = number
        self.PAs = []
        self.PA  = 0
        self.AB  = 0
        self.B1  = 0
        self.B2  = 0
        self.B3  = 0
        self.HR  = 0
        self.DP  = 0
        self.RBI = 0
        self.RUN = 0
        self.BB  = 0
        self.K   = 0
        self.SF  = 0

    def AddPA(self, pa):
        self.PAs.append(pa)
        if( pa.isPlay ):
            self.PA += 1
            if( pa.result != "BB" ):
                self.BB += 1
            elif( pa.result != "SF"):
                self.SF += 1
            else:
                self.AB += 1
                if( pa.result == "1B" ):
                    self.B1 += 1
                elif( pa.result == "2B" ):
                    self.B2 += 1
                elif( pa.result == "3B" ):
                    self.B3 += 1
                elif( pa.result == "HR" ):
                    self.HR += 1
                elif( pa.result == "DP" ):
                    self.DP += 1
                elif( pa.result == "K" ):
                    self.K += 1
            self.RBI += pa.rbi
            self.RUN += pa.run


    def NumPA(self):
        n = 0
        for pa in PAs:
            if( pa != '-' ):
                n += 1
        return n

class Pitcher:
    def __init__(self, number='0'):
        self.number = number
        self.IP  = 0
        self.TBF = 0
        self.H   = 0
        self.HR  = 0
        self.BB  = 0
        self.K   = 0
        self.RUN = 0
        self.ER  = 0
        self.GO  = 0
        self.FO  = 0

def ParseEndstring(end_str):
    n = len(end_str)
    rbi     = 0
    run     = 0
    isEnd   = 0
    note    = 0
    for s in end_str:
        if( s == 'R' ):
            run += 1
        elif( s.isdigit() ):
            rbi += int(s)
        elif( (s == '#') | (s == '!') ):
            isEnd = s
        elif( (s == '*') | (s == 'x') ):
            note = s
        else:
            print "Parse Error! Unknown end notation %s (%s)" %(s, end_str)
            sys.exit(0)

    return (rbi, run, isEnd, note)


def ParsePAstring(PA_str):
    
    if( PA_str == '-' ):
        pa = PA(False)
    else:
        s = PA_str.split('-')
        if( len(s) == 1 ):      # res
            pa = PA(True, 0, s[0], 0, 0, 0, 0)
        elif( len(s) == 2 ):
            if( s[0].isdigit() | (s[0] == 'L') | (s[0] == 'R') | (s[0] == 'C') ):   # pos-res
                pos = s[0]
                res = s[1]
                pa = PA(True, pos, res, 0, 0, 0, 0)
            else:               # res-end
                res = s[0]
                (rbi, run, isEnd, note) = ParseEndstring(s[1])
                pa = PA(True, 0, res, rbi, run, isEnd, note)
        elif( len(s) == 3 ):    # pos-res-end
            pos = s[0]
            res = s[1]
            (rbi, run, isEnd, note) = ParseEndstring(s[2])
            pa = PA(True, pos, res, rbi, run, isEnd, note)
        else:
            print "Parse Error! Unknown notation " + PA_str

    return pa

def AddPitcherInfo(pitcher, pa, isER=True):
    supposedOut = 0
    if( pa.isPlay ):
        pitcher.TBF += 1
        if( (pa.result == "1B") | (pa.result == "2B") | (pa.result == "3B") | (pa.result == "HR")):
            pitcher.H  += 1
            if( pa.result == "HR" ):
                pitcher.HR += 1
        elif( pa.result == "BB" ):
            pitcher.BB += 1
        elif( pa.result == "K" ):
            pitcher.K += 1
            pitcher.IP += 1
            supposedOut = 1
        elif( pa.result == "G" ):
            pitcher.GO += 1
            pitcher.IP += 1
            supposedOut = 1
        elif( pa.result == "F" ):
            pitcher.FO += 1
            pitcher.IP += 1  
            supposedOut = 1
        elif( pa.result == "DP" ): # TODO: need to seperate G-DP or F-DP ?
            pitcher.GO += 1
            pitcher.IP += 2
            supposedOut = 2
        elif( (pa.result == "FC") & (pa.note == 'x') ):
            pitcher.IP += 1
            supposedOut = 1
        elif( pa.result == "E" ):
            supposedOut = 1

        pitcher.RUN += pa.run
        if (isER):
            pitcher.ER += pa.run

    return supposedOut

def ParseGameData(record):
    player = []
    nPlayer = len(record);
    pitcher = Pitcher()

    for i in range(nPlayer):
        player.append( Batter(record[i][0], record[i][1]) )
        n = len(record[i])
        for j in range(2, n):
            pa = ParsePAstring(record[i][j].upper())
            player[i].AddPA(pa)

    print "nPlayer = %d" %nPlayer

    # parse inning information
    inning = 1
    column = 0
    turn   = 0
    order  = 0
    pa_count = 0
    column2inning = []
    out = 0
    isER = True
    while(True):
        pa = player[order].PAs[turn]
        pa.SetInning(inning, column)

        out += AddPitcherInfo(pitcher, pa, isER)
        if( out >= 3 ):
            isER = False

        if( pa.endInning == '!'): # end of game
            column2inning.append(inning)
            break

        pa_count += 1
        if( pa_count % nPlayer == 0 ):
            column2inning.append(inning)
            column += 1

        if( pa.endInning == '#' ): # end of inning
            pa_count = 0
            out = 0
            isER = True
            column2inning.append(inning)
            inning += 1
            column += 1
        
        order += 1
        if( order == nPlayer ):
            order = 0
            turn += 1

    return player, pitcher, column2inning


def digit2Character(n):
    if( n == 1 ):
        return "一"
    elif( n == 2 ):
        return "二"
    elif( n == 3 ):
        return "三"
    elif( n == 4 ):
        return "四"
    elif( n == 5 ):
        return "五"
    elif( n == 6 ):
        return "六"
    elif( n == 7 ):
        return "七"
    elif( n == 8 ):
        return "八"
    elif( n == 9 ):
        return "九"
    else:
        print "Error! Unsupported digit %d!" %n
        sys.exit(0)

def pos2word(pos):
    if( pos == "1" ):
        word = "投"
    elif( pos == "2" ):
        word = "捕"
    elif( pos == "3" ):
        word = "一"
    elif( pos == "4" ):
        word = "二"
    elif( pos == "5" ):
        word = "三"
    elif( pos == "6" ):
        word = "游"
    elif( (pos == "7") | (pos == "L") | (pos == "l") ):
        word = "左"
    elif( (pos == "8") | (pos == "R") | (pos == "r") ):
        word = "中"
    elif( (pos == "9") | (pos == "C") | (pos == "c") ):
        word = "右"
    elif( pos == "10" ):
        word = "自"
    
    return word

def res2word(res, wordLen):
    if(wordLen == 1):
        if( res == "G" ):
            word = "滾"
        elif( res == "F" ):
            word = "飛"
        elif( res == "1B" ):
            word = "安"
        elif( res == "2B" ):
            word = "二"
        elif( res == "3B" ):
            word = "三"
        elif( res == "HR" ):
            word = "全"
        elif( res == "FC" ):
            word = "選"
        elif( res == "SF" ):
            word = "犧"
        else:
            print "Error! Unknown res notation %s" %res
            sys.exit(0)  
    else:   # wordLen = 2
        if( res == "BB" ):
            word = "四壞"
        elif( res == "K" ):
            word = "三振"
        elif( res == "G" ):
            word = "滾地"
        elif( res == "F" ):
            word = "飛球"
        elif( res == "DP" ):
            word = "雙殺"
        elif( res == "1B" ):
            word = "一安"
        elif( res == "2B" ):
            word = "二安"
        elif( res == "3B" ):
            word = "三安"
        elif( res == "HR" ):
            word = "全壘"
        elif( res == "SF" ):
            word = "犧牲"
        elif( res == "FC" ):
            word = "野選"
        elif( res == "V" ):
            word += "違擊"
        else:
            print "Error! Unknown res notation %s" %res
            sys.exit(0)  

    return word

def end2word(pa):
    word = ""
    if( pa.rbi != 0 ):
        word += str(pa.rbi)
    if( pa.run != 0 ):
        word += "r"
    if( pa.endInning != 0 ):
        word += "#"
    if( pa.note != 0 ):
        word += pa.note

    return word

def PA2Character(pa):
    if( not pa.isPlay ):
        word = ("　　") # Full-Width white
    else:
        if( pa.pos == 0 ):
            word = res2word(pa.result, 2)
        else:
            word = pos2word(pa.pos)
            word += res2word(pa.result, 1)

        word += end2word(pa)

    return word

def DumpRecord2PTTformat(player, column2inning, outFile):
    nPlayer = len(player)
    line = " "*10
    line += (digit2Character(1) + "局    ")
        
    for n in range(1, len(column2inning)):
        if( column2inning[n] == column2inning[n-1] ):
            line += (" "*8)
        else:
            line += (digit2Character(column2inning[n]) + "局    ")

    line += '\n'
    outFile.write(line)
    
    for n in range(nPlayer):
        line = "%2s. %-4s  " %(player[n].order, player[n].number)
        column = -1
        for i in range(len(player[n].PAs) ):

            k = player[n].PAs[i].column - column
            line += ( " "*8*(k-1) )
            column = player[n].PAs[i].column
            word = PA2Character(player[n].PAs[i])

            line += "%-10s" %word

        line += '\n'
        outFile.write(line)

def DumpPlayerStatistic(player, pitcher, outFile):
    # opponent pitcher result
    print "IP = %d" %pitcher.IP
    IP = round(pitcher.IP / 3)
    if( pitcher.IP % 3 == 1 ):
        IP += 0.1
    elif( pitcher.IP % 3 == 2 ):
        IP += 0.2
    
    outFile.write("  投    投局 面打  被   被   四  三  失  自  滾  飛   Ｅ\n")
    outFile.write("  手    球數 對席 安打 全壘  壞  振  分  責  地  球   RA\n")
    line = "  %s     %.1f   %2d   %2d   %2d   %2d  %2d  %2d  %2d  %2d  %2d\n" %(pitcher.number, IP, pitcher.TBF, pitcher.H, pitcher.HR, pitcher.BB, pitcher.K, pitcher.RUN, pitcher.ER, pitcher.GO, pitcher.FO)
    outFile.write(line)

    outFile.write('\n\n')

    # Batting Statistic
    outFile.write("        PA  AB  1B  2B  3B  HR  DP RBI RUN  BB   K  SF\n")
    for p in player:
        line = "%2s. %-4s" %(p.order, p.number)
        line += "%2d  %2d  %2d  %2d  %2d  %2d  %2d %3d %3d  %2d   %d  %2d\n" %(p.PA, p.AB, p.B1, p.B2, p.B3, p.HR, p.DP, p.RBI, p.RUN, p.BB, p.K, p.SF)
        outFile.write(line)


def PrintPlayer(player, n=-1):
    if n == -1:
        print "Order No."
        for p in player:
            print " %s   %s." %(p.order, p.number)
            for pa in p.PAs:
                if not pa.isPlay:
                    print '-'
                else:
                    print "\t(%d, %d, %s, %s, %d, %d, %s, %s)" %(pa.inning, pa.column, pa.pos, pa.result, pa.rbi, pa.run, pa.endInning, pa.note)
    else:
        p = player[n]
        print "Order No."
        print " %s   %s." %(p.order, p.number)
        for pa in p.PAs:
            if not pa.isPlay:
                print "\t-"
            else:
                print "\t(%d, %d, %s, %s, %d, %d, %s, %s)" %(pa.inning, pa.column, pa.pos, pa.result, pa.rbi, pa.run, pa.endInning, pa.note)

def main():

    recordFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    with open(recordFileName) as recordFile:
        print "Load " + recordFileName
        record = [tuple(line.split()) for line in recordFile]

    player, pitcher, column2inning = ParseGameData(record)

    #PrintPlayer(player)
    outFile = open(outputFileName, 'w')
    DumpRecord2PTTformat(player, column2inning, outFile)
    DumpPlayerStatistic(player, pitcher, outFile)
    outFile.close()
    print "Save " + outputFileName
# end of main


if __name__ == "__main__":
    main()