#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os
import argparse

class PA:
    def __init__(self, pos, result, rbi, run, endInning, note):
        self.pos        = pos
        self.result     = result
        self.rbi        = rbi
        self.run        = run
        self.endInning  = endInning
        self.note       = note
        

class Player:
    def __init__(self, order, number):
        self.order  = order
        self.number = number
        self.PAs = []

    def AddPA(self, pa):
        self.PAs.append(pa)

    def NumPA(self):
        return len(PAs)

def ParseEnd(end_str):
    n = len(end_str)
    rbi     = 0
    run     = 0
    isEnd   = False
    note    = 0
    for s in end_str:
        if( s == 'r' ):
            run += 1
        elif( s.isdigit() ):
            rbi += int(s)
        elif( s == '#' ):
            isEnd = True
        elif( s == '*' ):
            note = '*'
        else:
            print "Parse Error! Unknown notation " + s
            sys.exit(0)

    return (rbi, run, isEnd, note)


def ParsePA(PA_str):
    
    s = PA_str.split('-')
    if( len(s) == 1 ):          # res
        pa = PA(0, s[0], 0, 0, False, 0)
    elif( len(s) == 2 ):
        if( s[0].isdigit() ):   # pos-res
            pos = int(s[0])
            res = s[1]
            pa = PA(pos, res, 0, 0, False, 0)
        else:                   # res-end
            res = s[0]
            (rbi, run, isEnd, note) = ParseEnd(s[1])
            pa = PA(0, res, rbi, run, isEnd, note)
    elif( len(s) == 3 ):     # pos-res-end
        pos = int(s[0])
        res = s[1]
        (rbi, run, isEnd, note) = ParseEnd(s[2])
        pa = PA(pos, res, rbi, run, isEnd, note)
    else:
        print "Parse Error! Unknown notation " + PA_str

    return pa

def ParseGameData(record):
    player = []
    nPlayer = len(record);
    nPA = 0
    for row in record:
        player.append( Player(row[0], row[1]) )
        n = len(row)
        for i in range(2, n):
            pa = ParsePA(row[i])
            player.addPA(pa)


"""
    print "nPlayer = %d" %nPlayer
    print "nPA = %d" %nPA
    inning = 1
    indent = 0
    turn   = 1
    order  = 0
    pa_count = 0
    indent2inning = []

    for i in range(nPA):
        pa = parsePA(record[order][1+turn], inning, indent)
        player[order].addPA(pa)
        pa_count += 1
        if( pa.endInning ):
            pa_count = 0
            if( i == nPA-1 ):
                break
            else:
                inning += 1
                indent += 1
                indent2inning.append(inning)
        
        order += 1
        if( order == nPlayer ):
            order = 0
            turn += 1

        if( pa_count % nPlayer == 0 ):
            indent += 1
            indent2inning.append(inning)

        #print "PA = (%d, %s, %s, %d, %d, %r, %s)" %(pa.inning, pa.pos, pa.result, pa.rbi, pa.run, pa.endInning, pa.note)
"""
    return player

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

def DumpRecord2PTTformat(player, PA_inning, outFile):
    nPlayer = len(player)
    line = "          "
    for n in range(len(PA_inning)):
        line += (digit2Character(n+1) + "局    ")
        nPA = PA_inning[n]
        while( nPA > nPlayer ):
            line += ("        ")
            nPA -= nPlayer

    line += '\n'
    outFile.write(line)
    
    indentLevel = 0
    for n in range(nPlayer):
        order = "%2s" %player[n].order
        line = "%s. %-4s  " %(order, player[n].number)
        
        word = PA2character()


        line += '\n'
        outFile.write(line)
        
def PrintPlayer(player, n):
    print "Order No."
    if not n:
        for p in player:
            line = " %2s. %-4s  " %(p.order, p.number)
            for pa in p.PAs:

def main():

    recordFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    with open(recordFileName) as recordFile:
        print "load " + recordFileName
        record = [tuple(line.split()) for line in recordFile]

    player = ParseGameData(record)

    #outFile = open(outputFileName, 'w')
    #printRecord2PTTformat(player, PA_inning, outFile)
    #outFile.close()
    #r = record[0]
    #for i in range(len(r)):
    #    print r[i]
# end of main


if __name__ == "__main__":
    main()