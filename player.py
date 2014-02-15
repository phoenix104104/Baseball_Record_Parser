#!/usr/bin/python
# -*- coding: utf8 -*-

class PA:
    def __init__(self, isPlay, pos=0, result=0, rbi=0, run=0, out=0, endInning=0, note=0):
        self.isPlay     = isPlay    # used for no-play batter
        self.pos        = pos       # hit-ball direction
        self.result     = result    # result string
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
            if( pa.isPlay ):
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