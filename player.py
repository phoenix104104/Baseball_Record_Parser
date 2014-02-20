#!/usr/bin/python
# -*- coding: utf8 -*-
import sys

class Game:
    def __init__(self):
        self.team1 = None
        self.team2 = None
        self.total_innings = 0
        self.score_board = []

class Team:
    def __init__(self):
        self.name = ""
        self.batters        = []   # batter per PA record (in raw string format)
        self.pitchers       = []
        self.orders         = []
        self.order_table    = []
        self.scores         = []
        self.col2inn        = None
        self.H              = 0
        self.E              = 0

    def order(self):
        return len(self.order_table)

    def nBatter(self):
        return len(self.batters)

    def Runs(self):
        return sum(self.scores) 

class PA:
    def __init__(self):
        self.isPlay     = False     # used for no-play batter
        self.pos        = None      # hit-ball direction
        self.result     = None      # result string
        self.rbi        = 0         # RBI
        self.run        = 0         # RUN
        self.out        = 0         # number of outs in this play
        self.endInning  = ""        # should be 0, '#' or '!'
        self.note       = ""        # 0 or *'
        self.inning     = -1        # inning
        self.column     = 0         # column in printed table
        self.raw_str    = ""        # pa code string
        self.change_pitcher = None

class Batter:
    def __init__(self, order, number):
        self.order      = order
        self.number     = number
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
        self.SF  = 0    # sacrificed fly 高飛犧牲打
        self.CB  = 0    # combacker 投手強襲球
        self.IB  = 0    # illegal batted 違規擊球
        self.IF  = 0    # infield fly 內野高飛必死球

    def AddPA(self, pa):
        if (pa.result not in ['1B', '2B', '3B', 'HR', 'SF', 'BB', 'K', 'G', 'F', 'DP', 'FC', 'E', 'IB', 'CB', 'IF']):
            sys.exit('Error! Not support PA notation %s in %s' %(pa.result, pa.raw_str))

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
                elif( pa.result == "CB" ):
                    self.CB += 1
                elif( pa.result == "IB" ):
                    self.IB += 1
                elif( pa.result == "IF" ):
                    self.IF += 1

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
        self.TBF = 0    # total batters faced 面對人次
        self.Out = 0
        self.H   = 0
        self.HR  = 0
        self.BB  = 0
        self.K   = 0
        self.Run = 0
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
                self.ERA = float(self.ER) / self.Out * (7*3)
        
        return self.ERA

    def IP(self):
        if( self.Out == 0 ):
            return '0.0'
        else:
            N = int(self.Out / 3)
            m = self.Out % 3
            return '%d.%d' %(N, m)
            

    def AddPa(self, pa, isER=True):
        if( pa.isPlay ):
            self.TBF += 1
            if( pa.result in ("1B", "2B", "3B", "HR") ):
                self.H  += 1
                if( pa.result == "HR" ):
                    self.HR += 1
            elif( pa.result == "BB" ):
                self.BB += 1
            elif( pa.result == "K" ):
                self.K += 1
            elif( pa.result == "G" ):
                self.GO += 1
            elif( pa.result in ("F", "SF") ):
                self.FO += 1
            elif( pa.result == "DP" ): # TODO: need to seperate G-DP or F-DP ?
                self.GO += 2
            elif( (pa.result == "FC") & (pa.out > 0) ):
                self.GO += 1
            elif( pa.result == "IF" ):  # Infield Fly 內野高飛必死球
                self.FO += 1
    
            self.Out += pa.out
            self.Run += pa.run
            if (isER):
                self.ER += pa.rbi
    
