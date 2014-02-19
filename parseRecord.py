#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os
import argparse
from player import Game, Team, Batter, Pitcher, PA
from dump_record import make_PTT_format, make_database_format

def parse_base(pa, str):

    n = len(str)
    rbi   = 0
    run   = 0
    out   = 0
    isEnd = 0
    note  = 0
    for s in str:
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
            print "Parse Error! Unknown end notation %s (%s)" %(s, str)
            sys.exit(0)
    
    pa.rbi = rbi
    pa.run = run
    pa.out = out
    pa.endInning = isEnd
    pa.note = note
    return pa


def parse_PA(team, order_table, order, turn, inning, curr_order):
    
    pa_str = order_table[order][turn].upper()
    s = pa_str.split('-')

    pa = PA()
    pa.inning = inning
    pa.isPlay = True
    pa.raw_str = pa_str
    
    batter = curr_order[order] # pointer to current batter
    if( s[0][0] == 'R' and len(s[0])!= 1  ):  # change batter
        no = s[0][1:]
        idx = team.batters.index(batter)
        batter = Batter('R', no)
        team.batters.insert(idx+1, batter)
        curr_order[order] = batter
        s = s[1:]

    if( len(s) == 1 ):      # result
        pa.result = s[0]

    elif( len(s) == 2 ):

        if( s[0].isdigit() or (s[0] in ['L', 'R', 'C']) ):   # pos-res
            pa.pos    = s[0]
            pa.result = s[1]

        else:               # res-end
            pa.result = s[0]
            pa = parse_base(pa, s[1])

    elif( len(s) == 3 ):    # pos-res-end
        pa.pos    = s[0]
        pa.result = s[1]
        pa = parse_base(pa, s[2])

    else:
       print "Parse Error! Unknown notation " + PA_str

    batter.AddPA(pa)
    order_table[order][turn] = [batter, pa]
    return pa


def parse_teams(game_data):

    team1 = Team()
    team2 = Team()
    
    for data in game_data:
        if data[0] == 'T1':
            team = team1
            team.name = data[1]

        elif data[0] == 'T2':
            team = team2
            team.name = data[1]

        elif data[0].upper() == 'P':
            no = data[1].upper()
            team.pitchers.append( Pitcher(no) )

        elif data[0].isdigit():
            order = data[0].upper()
            no    = data[1].upper()
            PAs   = data[2:]
            team.batters.append( Batter(order, no) )
            team.order_table.append( PAs )

    return team1, team2



def parse_pitcher_info(team, pitcher):

    # parse inning information
    inning   = 1
    turn     = 0
    order    = 0
    column   = 0
    pa_count = 0
    isER     = True
    nOrder   = len(team.order_table)
    nBatter  = team.nBatter()
    supp_out = 0    # supposed out
    col2inn  = []

    while(True):
        pa = team.order_table[order][turn][1]    
        pitcher.AddPa(pa, isER)
        pa.column = column

        if( pa.endInning == '!'): # end of game
            col2inn.append(inning)
            break

        supp_out += pa.out
        if( pa.result == "E" ):
            supp_out += 1
        
        if( supp_out >= 3 ):
            isER = False

        pa_count += 1
        if( pa_count % nOrder == 0 and pa.endInning != '#' ):
            col2inn.append(inning)
            column += 1

        if( pa.endInning == '#' ): # change inning
            pa_count = 0
            supp_out = 0
            isER = True
            col2inn.append(inning)
            inning += 1
            column += 1

        order += 1
        if( order == nOrder ):
            order = 0
            turn += 1
    
    team.col2inn = col2inn


def print_order_table(table):
    for row in table:
        for col in row:
            batter  = col[0]
            pa      = col[1]
            sys.stdout.write("%2s  (%d)%-12s" %(batter.number, pa.out, pa.raw_str))
        sys.stdout.write('\n')

def print_batter(batters):
    for p in batters:
        sys.stdout.write("%2s  %2s " %(p.order, p.number) )
        for pa in p.PAs:
            sys.stdout.write("(%d)%-12s " %(pa.column, pa.raw_str) )
        sys.stdout.write('\n')


def parse_order_table(team):
        
    # parse inning information
    inning   = 1
    turn     = 0
    order    = 0
    out      = 0
    score    = 0    # score per inning
    nOrder = len(team.batters)
    curr_order = []
    for batter in team.batters:
        curr_order.append(batter)

    while(True):
        pa = parse_PA(team, team.order_table, order, turn, inning, curr_order)
        score += pa.run

        if( pa.endInning in ('#', '!') ):  # change inning
            team.scores.append(score)
            score = 0

        if( pa.endInning == '!' ):
            break

        order += 1
        if( order == nOrder ):
            order = 0
            turn += 1
    return team

def load_raw_record_data(fileName):

    raw_data = []
    with open(fileName) as f:
        print "Load " + fileName
        for line in f:
            data = list(line.split())
            if len(data) != 0:
                raw_data.append(data)
                
    return raw_data

def parse_game_data(game_data):

    game = Game()
    team1, team2 = parse_teams(game_data)

    game.team1 = parse_order_table(team1)
    game.team2 = parse_order_table(team2)
    
    parse_pitcher_info(game.team1, game.team2.pitchers[0])  
    parse_pitcher_info(game.team2, game.team1.pitchers[0])  
    
    return game

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i" , dest="input_file_name" , required=True, help="Specify input file name")
    parser.add_argument("-o" , dest="output_file_name", help="Specify output file name [default: print to screen]")
    parser.add_argument("-nc", dest="no_color", default=False, action="store_true", help="Close color mode [default: on]")
    opt = parser.parse_args(sys.argv[1:])
    
    recordFileName = opt.input_file_name
    outputFileName = opt.output_file_name
    isColor = not opt.no_color

    raw_data = load_raw_record_data(recordFileName)
    game = parse_game_data(raw_data)

    
    post_ptt = make_PTT_format(game, isColor)
    post_db  = make_database_format(game)
    if( outputFileName == None ):
        print post_ptt
   #     print post_db
    else:
        with open(outputFileName, 'w') as f:
            print "Dump %s" %outputFileName
            f.write(post_ptt)
            f.write(post_db)
    

if __name__ == "__main__":
    main()
