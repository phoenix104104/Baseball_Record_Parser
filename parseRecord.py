#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os
import argparse

class PA:
    def __init__(self, isPlay, pos=0, result=0, rbi=0, run=0, out=0, endInning=0, note=0):
        self.isPlay     = isPlay    # used for no-play batter
        self.pos        = pos       # hit-ball direction
        self.result     = result    # result
        self.rbi        = rbi       # RBI
        self.run        = run       # RUN
        self.out        = out       # out
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
            if( pa.result == "BB" ):
                self.BB += 1
            elif( pa.result == "SF"):
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

    def getERA(self):
        if( self.ER == 0 ):
            self.ERA = 0
        else:
            if( self.IP == 0 ):
                self.ERA = float("inf")
            else:
                self.ERA = self.ER * 21.0 / self.IP
        
        return self.ERA

def ParseEndstring(end_str):
    n = len(end_str)
    rbi     = 0
    run     = 0
    out     = 0
    isEnd   = 0
    note    = 0
    for s in end_str:
        if( s == 'R' ):
            run += 1
        elif( s.isdigit() ):
            rbi += int(s)
        elif( s == 'X' ):
            out += 1
        elif( (s == '#') | (s == '!') ):
            isEnd = s
        elif( s == '*' ):
            note = s
        else:
            print "Parse Error! Unknown end notation %s (%s)" %(s, end_str)
            sys.exit(0)

    return (rbi, run, out, isEnd, note)


def ParsePAstring(PA_str):
    
    if( PA_str == '-' ):
        pa = PA(False)
    else:
        s = PA_str.split('-')
        if( len(s) == 1 ):      # res
            pa = PA(True, 0, s[0], 0, 0, 0, 0, 0)
        elif( len(s) == 2 ):
            if( s[0].isdigit() | (s[0] == 'L') | (s[0] == 'R') | (s[0] == 'C') ):   # pos-res
                pos = s[0]
                res = s[1]
                pa = PA(True, pos, res, 0, 0, 0, 0, 0)
            else:               # res-end
                res = s[0]
                (rbi, run, out, isEnd, note) = ParseEndstring(s[1])
                pa = PA(True, 0, res, rbi, run, out, isEnd, note)
        elif( len(s) == 3 ):    # pos-res-end
            pos = s[0]
            res = s[1]
            (rbi, run, out, isEnd, note) = ParseEndstring(s[2])
            pa = PA(True, pos, res, rbi, run, out, isEnd, note)
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
            supposedOut = 1
        elif( pa.result == "G" ):
            pitcher.GO += 1
            supposedOut = 1
        elif( pa.result == "F" ):
            pitcher.FO += 1
            supposedOut = 1
        elif( pa.result == "SF" ):
            pitcher.FO += 1
            supposedOut = 1
        elif( pa.result == "DP" ): # TODO: need to seperate G-DP or F-DP ?
            pitcher.GO += 2
            supposedOut = 2
        elif( pa.result == "E" ):
            supposedOut = 1
        elif( (pa.result == "FC") & (pa.out > 0) ):
            pitcher.GO += 1
            supposedOut = 1
        elif( pa.result == "CB" ):  # combacker 投手強襲球
            supposedOut = 1
        elif( pa.result == "IB" ):  # Illegal batted 違規擊球
            supposedOut = 1
        elif( pa.result == "IF" ):  # Infield Fly 內野高飛必死球
            pitcher.FO += 1
            supposedOut = 1


        pitcher.IP += pa.out
        pitcher.RUN += pa.run
        if (isER):
            pitcher.ER += pa.rbi

    return supposedOut

def ParseGameData(record):
    player = []
    nPlayer = len(record);
    pitcher = Pitcher()

    for i in range(nPlayer):
        player.append( Batter(record[i][0].upper(), record[i][1].upper()) )
        n = len(record[i])
        for j in range(2, n):
            pa = ParsePAstring(record[i][j].upper())
            player[i].AddPA(pa)

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
        if( (pa_count % nPlayer == 0) & (pa.endInning != '#') ):
            column2inning.append(inning)
            column += 1

        if( pa.endInning == '#' ): # end of inning\
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


def digit2FullWidth(n):
    if( n == 1 ):
        return "１"
    elif( n == 2 ):
        return "２"
    elif( n == 3 ):
        return "３"
    elif( n == 4 ):
        return "４"
    elif( n == 5 ):
        return "５"
    elif( n == 6 ):
        return "６"
    elif( n == 7 ):
        return "７"
    elif( n == 8 ):
        return "８"
    elif( n == 9 ):
        return "９"
    else:
        print "Error! Unsupported digit %d!" %n
        sys.exit(0)

def pos2word(pos, res):
    if( pos == "1" ):
        if( res == "1B" ):
            word = "內"
        else:
            word = "投"
    elif( pos == "2" ):
        word = "捕"
    elif( pos == "3" ):
        if( res == "1B" ):
            word = "右"
        else:
            word = "一"
    elif( pos == "4" ):
        if( res == "1B" ):
            word = "右"
        else:
            word = "二"
    elif( pos == "5" ):
        if( res == "1B" ):
            word = "左"
        else:
            word = "三"
    elif( pos == "6" ):
        word = "游"
    elif( (pos == "7") | (pos == "L") ):
        word = "左"
    elif( (pos == "8") | (pos == "C") ):
        word = "中"
    elif( (pos == "9") | (pos == "R") ):
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
        elif( res == "E" ):
            word = "失"
        elif( res == "DP" ):
            word = "雙"
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
        elif( res == "IB" ):
            word = "違擊"
        elif( res == "E" ):
            word = "失誤"
        elif( res == "CB" ):
            word = "強襲"
        elif( res == "IF" ):
            word = "內飛"
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
    if( (pa.note != 0) & (pa.note != 'X') ):
        word += pa.note

    return word, len(word)

def PA2Character(pa):
    if( not pa.isPlay ):
        word = ("　　") # Full-Width white
        word_len = 4
    else:
        if( pa.pos == 0 ):
            word = res2word(pa.result, 2)
        else:
            word = pos2word(pa.pos, pa.result)
            word += res2word(pa.result, 1)

        word_len = 4
        word = AddColor(pa.result, word)
        pa_word, n = end2word(pa)
        word += pa_word
        word_len += n

    return word, word_len

def AddColor(pa_result, word):
    if( (pa_result == "1B") | (pa_result == "2B") | (pa_result == "3B") ):
        word = "\x1b[1;31m%s\x1b[m" %word
    elif( pa_result == "HR" ):
        word = "\x1b[1;5;1;31m%s\x1b[m" %word
    elif( pa_result == "SF" ):
        word = "\x1b[1;35m%s\x1b[m" %word
    elif( pa_result == "BB" ):
        word = "\x1b[1;32m%s\x1b[m" %word
    elif( pa_result == "K" ):
        word = "\x1b[1;33m%s\x1b[m" %word
    
    return word

def DumpRecord2PTTformat(player, column2inning, outFile):
    nPlayer = len(player)
    line = " "*10
    line += (digit2FullWidth(1) + "局    ")
        
    for n in range(1, len(column2inning)):
        if( column2inning[n] == column2inning[n-1] ):
            line += (" "*8)
        else:
            line += (digit2FullWidth(column2inning[n]) + "局    ")

    line += '\n'
    outFile.write(line)
    
    for n in range(nPlayer):
        if( player[n].order == 'R' ):
            order = "代"
        else:
            order = player[n].order

        line = "%2s. " %order

        if( player[n].number == 'N' ):
            num = "新生"
        else:
            num = player[n].number
        space = " " * (6 - len(num.decode('utf8').encode('big5') ) ) 
        line += "%s%s" %(num, space)

        column = -1
        for i in range(len(player[n].PAs) ):

            k = player[n].PAs[i].column - column
            line += ( " "*8*(k-1) )
            column = player[n].PAs[i].column
            word, word_len = PA2Character(player[n].PAs[i])

            space = " " * (8 - word_len)
            line += "%s%s" %(word, space)

        line += '\n'
        outFile.write(line)

def DumpPlayerStatistic(player, pitcher, outFile):
    # opponent pitcher result
    IP = round(pitcher.IP / 3)
    if( pitcher.IP % 3 == 1 ):
        IP += 0.1
    elif( pitcher.IP % 3 == 2 ):
        IP += 0.2
    
    outFile.write("  投    投局 面打  被   被   四  三  失  自  滾  飛   Ｅ\n")
    outFile.write("  手    球數 對席 安打 全壘  壞  振  分  責  地  球   RA\n")
    line = "  %2s     %.1f  %2d   %2d   %2d   %2d  %2d  %2d  %2d  %2d  %2d  %.2f\n" %(pitcher.number, IP, pitcher.TBF, pitcher.H, pitcher.HR, pitcher.BB, pitcher.K, pitcher.RUN, pitcher.ER, pitcher.GO, pitcher.FO, pitcher.getERA())
    outFile.write(line)

    outFile.write('\n')

    # Batting Statistic
    outFile.write("        PA  AB  1B  2B  3B  HR  DP RBI RUN  BB   K  SF\n")
    for p in player:
        line = "%2s. %-4s" %(p.order, p.number)
        line += "%2d  %2d  %2d  %2d  %2d  %2d  %2d %3d %3d  %2d   %d  %2d\n" %(p.PA, p.AB, p.B1, p.B2, p.B3, p.HR, p.DP, p.RBI, p.RUN, p.BB, p.K, p.SF)
        outFile.write(line)


def PrintPlayer(player, n=-1):
    if n == -1:
        for p in player:
            print "Ord No. Inn Col Pos Res RBI Run out end note"
            print "%3s %2s." %(p.order, p.number)
            for pa in p.PAs:
                if not pa.isPlay:
                    print '\t-'
                else:
                    print "\t( %d,  %d,  %s,  %2s,  %d,  %d,  %d,  %s,  %s)" %(pa.inning, pa.column, pa.pos, pa.result, pa.rbi, pa.run, pa.out, pa.endInning, pa.note)
    else:
        p = player[n]
        print "Order No. Inn Col Pos Res RBI Run out end note"
        print " %s   %s." %(p.order, p.number)
        for pa in p.PAs:
            if not pa.isPlay:
                print "\t-"
            else:
                print "\t(%d, %d, %s, %s, %d, %d, %d, %s, %s)" %(pa.inning, pa.column, pa.pos, pa.result, pa.rbi, pa.run, pa.out, pa.endInning, pa.note)

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
    outFile.write('\n')
    DumpPlayerStatistic(player, pitcher, outFile)
    outFile.close()
    print "Save " + outputFileName
# end of main


if __name__ == "__main__":
    main()