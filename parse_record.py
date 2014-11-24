#!/usr/bin/python
# -*- coding: utf8 -*-

import sys, os
import argparse
from player import Game, Team, Batter, Pitcher, PA
from dump_record import make_PTT_format, make_database_format

def check_least_out(pa):
    out = 0
    one_out = ["G", "F", "K", "SF", "IF", "CB", "IB", "FO"]
    if( pa.result in one_out ):
        out = 1
    elif( pa.result == "DP" ):
        out = 2

    return out

def parse_base(pa, str):
    
    err = ""
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
        elif( (s == '*') | (s == '?') ):
            note = s
        else:
            err = "Unknown base notation %s (%s)" %(s, pa.raw_str)
            break

    pa.rbi = rbi
    pa.run = run
    pa.out = out
    pa.endInning = isEnd
    pa.note = note
    return pa, err

def change_pitcher(pa_strs):
    if( pa_strs[0][0] == 'P' ):
        return True
    else:
        return False

def change_batter(pa_strs):
    if( pa_strs[0][0] == 'R' and len(pa_strs[0]) != 1 ): # s[0] = 'R + no', not only 'R'(Right)
        return True
    else:
        return False
        

def parse_PA(team, order, turn, inning, curr_order):
    
    err = ""
    pa_str = team.order_table[order][turn].upper()
    s = pa_str.split('/')
    
    pa = PA()
    pa.inning = inning
    pa.raw_str = pa_str
    batter = curr_order[order] # pointer to current batter
    

    if( s[0] == 'N' ): # no play
        pa.isPlay = False

    else:
        pa.isPlay = True
        while( change_pitcher(s) or change_batter(s) ):

            if( change_pitcher(s) ):
                no = s[0][1:].upper()
                pa.change_pitcher = no
                s = s[1:]

            if( change_batter(s)  ):  # change batter
                no = s[0][1:].upper()
                idx = team.batters.index(batter) # current batter index

                batter = team.find_batter(no)
                if( batter == None or no == "OB" ): # may exist multiple OB
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
                pa, err = parse_base(pa, s[1])

        elif( len(s) == 3 ):    # pos-res-end
            pa.pos    = s[0]
            pa.result = s[1]
            pa, err = parse_base(pa, s[2])

        else:
           err = "Incorrect PA format %s\n" %pa.raw_str
           return pa, err



    least_out = check_least_out(pa)
    if( pa.out < least_out ):
        pa.out = least_out

    err = batter.AddPA(pa)
    order_table[order][turn] = [batter, pa]
    return pa, err


def parse_teams(game_data):

    team_list = []

    for data in game_data:
        
        if data[0] == 'T':
            team = Team()
            team.name = data[1]
            team_list.append(team)

        elif data[0].upper() == 'P':
            no = data[1].upper()
            team.pitchers.append( Pitcher(no) )

        elif data[0].isdigit():
            order = data[0].upper()
            pos   = data[1]
            no    = data[2]
            PAs   = data[3:]
            team.batters.append( Batter(order, no, pos) )
            team.order_table.append( PAs )

    return team_list

def parse_column(team):
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
        pa.column = column

        if( pa.endInning == '!'): # end of game
            col2inn.append(inning)
            break

        pa_count += 1
        if( pa_count % nOrder == 0 and pa.endInning != '#' ):
            col2inn.append(inning)
            column += 1

        if( pa.endInning == '#' ): # change inning
            pa_count = 0
            col2inn.append(inning)
            inning += 1
            column += 1

        order += 1
        if( order == nOrder ):
            order = 0
            turn += 1
    
    team.col2inn = col2inn



def parse_pitcher_info(team, pitchers):
    
    err = ""
    # parse inning information
    turn     = 0
    order    = 0
    isER     = True
    nOrder   = len(team.order_table)
    nBatter  = team.nBatter()
    supp_out = 0    # supposed out
    
    pitcher = pitchers[0]

    while(True):
        pa = team.order_table[order][turn][1]
        
        # change pitcher
        if( pa.change_pitcher != None ):
            no = pa.change_pitcher

            # find whether pitcher had been on field before
            is_new_pitcher = True
            for p in pitchers:
                if p.number == no:
                    pitcher = p
                    is_new_pitcher = False
                    break
                    
            if( is_new_pitcher ):
                pitcher = Pitcher(no)
                pitchers.append( pitcher )

        err = pitcher.AddPa(pa, isER)
        if( err != "" ):
            break

        if( pa.endInning == '!'): # end of game
            break

        supp_out += pa.out
        if( pa.result == "E" ):
            supp_out += 1
        
        if( supp_out >= 3 ):
            isER = False

        if( pa.endInning == '#' ): # change inning
            supp_out = 0
            isER = True

        order += 1
        if( order == nOrder ):
            order = 0
            turn += 1
    
    return err

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
    
    err = ""
    # parse inning information
    inning      = 1
    turn        = 0
    order       = 0
    out         = 0
    score       = 0    # score per inning
    nOrder      = len(team.batters)
    curr_order  = []
    for batter in team.batters:
        curr_order.append(batter)
    
    team_H = 0
    opp_E = 0
    while(True):
        pa, err = parse_PA(team, team.order_table, order, turn, inning, curr_order)
        if( err != "" ):
            err += " - row %d" %(order+1)
            break
        
        score += pa.run

        if( pa.result in ("1B", "2B", "3B", "HR") ):
            team_H += 1

        if( pa.result == "E" ):
            opp_E += 1

        if( pa.endInning in ('#', '!') ):  # change inning
            team.scores[inning] = score
            inning += 1
            score = 0

        if( pa.endInning == '!' ):
            break

        order += 1
        if( order == nOrder ):
            order = 0
            turn += 1
    
    team.H  = team_H

    return opp_E, err

def load_data_from_file(fileName):

    raw_data = []
    with open(fileName) as f:
        print "Load " + fileName
        for line in f:
            data = list(line.split())
            if len(data) != 0:
                raw_data.append(data)
                
    return raw_data

def load_data_from_string(string_data):
    
    raw_data = []
    lines = string_data.split('\n')
    for line in lines:
        data = line.split()
        data = filter(None, data)
        if len(data) != 0:
            raw_data.append(data)
    
    return raw_data

def make_team(team_name, scores, str_table):

    team = Team()
    team.name = team_name

    if( scores == None ):
        scores = [0] * 7
    if( len(scores) < 7 ):
        scores = scores + [0] * (7 - len(scores))

    team.scores = scores

    for r in range(len(str_table)):

        row = str_table[r]

        order = str(r+1)
        no    = row[0]
        pos   = row[1].upper()
        PAs   = row[2:]
        team.batters.append( Batter(order, no, pos) )
        team.order_table.append( PAs )

        if( pos == 'P' ):
            team.pitchers.append( Pitcher(no) )

    return team

def parse_game_data(game_data):

    game = Game()
    team = make_team('RB', game_data)
    
    #if( len(team_list) == 1 ):
    game.team1 = parse_order_table(team)
    parse_column(game.team1)
    '''
    elif( len(team_list) == 2 ):
        team1 = team_list[0]
        team2 = team_list[1]
        game.team1 = parse_order_table(team1, team2)
        game.team2 = parse_order_table(team2, team1)
    
        parse_pitcher_info(game.team1, game.team2.pitchers)  
        parse_pitcher_info(game.team2, game.team1.pitchers)  
    '''
    return game


def make_game(away, home):

    game = Game()
    err = ""

    if( not away.hasRecord() and not home.hasRecord() ):
        err = "Both record not exist"
        return game, err

    if( len(away.pitchers) == 0 ):
        err = away.name + "沒有先發投手"
        return game, err

    if( len(home.pitchers) == 0 ):
        err = home.name + "沒有先發投手"
        return game, err
    
    if( away.hasRecord() ):
        away, home.E, err = parse_order_table(away)

    if( err != "" ):
        err += " in Away Record"
        return game, err

    if( home.hasRecord() ):
        home, away.E, err = parse_order_table(home)

    if( err != "" ):
        err += " in Home Record"
        return game, err
        
    err = parse_pitcher_info(away, home.pitchers)  
    if( err != "" ):
        err += " in Away Record"
        return game, err
        
    err = parse_pitcher_info(home, away.pitchers)  
    if( err != "" ):
        err += " in Home Record"
        return game, err
        
    # calculate total scores
    away.compute_statistic()
    home.compute_statistic()

    game.away = away
    game.home = home

    return game, err

def seperate_web_string(string_data):
    
    str_table = []
    lines = string_data.split('\n')
    for line in lines:
        data = line.split()
        data = filter(None, data)
        if len(data) != 0:
            str_table.append(data)
    
    return str_table
    
def parse_record_from_web(away_team_name, away_scores, away_record, home_team_name, home_scores, home_record):
    
    away_str_table = seperate_web_string(away_record)
    home_str_table = seperate_web_string(home_record)
    
    away = make_team(away_team_name, away_scores, away_str_table)
    home = make_team(home_team_name, home_scores, home_str_table)

    game, err = make_game(away, home)

    '''   
    game, err = make_game(away_team_name, away_str_table, home_team_name, home_str_table)
    
    if( err != "" ):
        return None, err

    game.away.compute_statistic()
    game.home.compute_statistic()

    make_web_table(game.away)
    make_web_table(game.home)

    isColor = True
    post_ptt = make_PTT_format(game, isColor)
    post_ptt = post_ptt.replace('\x1b', '\025')
    game.post_ptt = post_ptt
    #post_db  = make_database_format(game)

    return game, err
    '''
    return 0, 0

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i" , dest="input_file_name" , required=True, help="Specify input file name")
    parser.add_argument("-o" , dest="output_file_name", help="Specify output file name [default: print to screen]")
    parser.add_argument("-nc", dest="no_color", default=False, action="store_true", help="Close color mode [default: on]")

    opts = parser.parse_args(sys.argv[1:])
    
    recordFileName = opts.input_file_name
    outputFileName = opts.output_file_name
    isColor = not opts.no_color

    raw_data = load_data_from_file(recordFileName)
    game = parse_game_data(raw_data)

    if( game.team2 == None ):
        isOneTeam = True
    else:
        isOneTeam = False

    post_ptt = make_PTT_format(game, isOneTeam, isColor)
    post_db  = make_database_format(game, isOneTeam)
    if( outputFileName == None ):
        print post_ptt
        print post_db
    else:
        with open(outputFileName, 'w') as f:
            print "Dump %s" %outputFileName
            # replace ESC to ^U
            post_ptt = post_ptt.replace('\x1b', '\025')
            f.write(post_ptt)

        with open(outputFileName + '.db', 'w') as f:
            print "Dump %s" %(outputFileName + '.db')
            f.write(post_db)
    

if __name__ == "__main__":
    main()
