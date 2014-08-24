#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, os

def make_PTT_format(game, isOneTeam=False, isAddColor=True):
    
    posts = ""
    if( isOneTeam ):
        posts += make_team_table(game.team1, isAddColor)
    else:
        posts += make_PTT_score_board(game)
        posts += "\n"
        posts += game.team1.name + "\n"
        posts += make_team_table(game.team1, isAddColor)
        posts += "\n\n"
        posts += make_pitcher_table(game.team1.pitchers)
        posts += "--------------------------------------------------------------------------------\n\n"
        posts += game.team2.name + "\n"
        posts += make_team_table(game.team2, isAddColor)
        posts += "\n\n"
        posts += make_pitcher_table(game.team2.pitchers)
        posts += '\n'

    return posts


def make_database_format(game, isOneTeam=False):

    if( isOneTeam ):
        posts = dump_player_statistic(game.team1)
    else:
        posts = make_score_board(game)
        posts += "\n"
        posts += dump_player_statistic(game.team1)
        posts += "\n"
        posts += dump_player_statistic(game.team2)
    return posts

def make_score_board(game):

    posts = ""
    posts += "%s\t" %(game.team1.name)
    for s in game.team1.scores:
        posts += "%4d" %s
    posts += "\n"
    posts += "%s\t" %(game.team2.name)
    for s in game.team2.scores:
        posts += "%4d" %s
    posts += "\n"
    return posts

def make_PTT_score_board(game): 
    
    hh = "─"
    vv = "│"
    vh = "┼"
    posts  = "      %s１%s２%s３%s４%s５%s６%s７%s　%sＲ%sＨ%sＥ\n" %(vv, vv, vv, vv, vv, vv, vv, vv, vv, vv, vv)
    posts += "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n" %(hh, hh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh)
    posts += " %s %s%2d%s%2d%s%2d%s%2d%s%2d%s%2d%s%2d%s　%s%2d%s%2d%s%2d\n" %(game.team1.name, vv, game.team1.scores[0], vv, game.team1.scores[1], vv, game.team1.scores[2], vv, game.team1.scores[3], vv, game.team1.scores[4], vv, game.team1.scores[5], vv, game.team1.scores[6], vv, vv, game.team1.Runs(), vv, game.team1.H, vv, game.team1.E)
    posts += "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n" %(hh, hh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh, vh, hh)
    posts += " %s %s%2d%s%2d%s%2d%s%2d%s%2d%s%2d%s%2d%s　%s%2d%s%2d%s%2d\n" %(game.team2.name, vv, game.team2.scores[0], vv, game.team2.scores[1], vv, game.team2.scores[2], vv, game.team2.scores[3], vv, game.team2.scores[4], vv, game.team2.scores[5], vv, game.team2.scores[6], vv, vv, game.team2.Runs(), vv, game.team2.H, vv, game.team2.E)

    return posts

def big5len(string):
    return len(string.decode('utf8').encode('big5') )


def make_team_table(team, isAddColor=True):

    col2inn = team.col2inn
    nPlayer = team.nBatter()
    player  = team.batters

    posts = " "*15
    posts += (digit2FullWidth(1) + "局    ")
        
    for n in range(1, len(col2inn)):
        if( col2inn[n] == col2inn[n-1] ):
            posts += (" "*10)
        else:
            posts += (digit2FullWidth(col2inn[n]) + "局    ")

    posts += '\n'
    
    for n in range(nPlayer):
        if( player[n].order == 'R' ):
            order = "代"
        else:
            order = player[n].order

        posts += "%2s. " %order

        if( player[n].number == 'N' ):
            num = "新生"
        else:
            num = player[n].number

        space = " " * (6 - big5len(num) ) 
        posts += "%s%s%3s  " %(num, space, player[n].pos)

        column = 0
        for i in range(len(player[n].PAs) ):
            
            pa = player[n].PAs[i]

            # append white space
            k = pa.column - column
            posts += ( " "*8*k )

            column = pa.column + 1
            word, word_len = PA2Character(pa, isAddColor)

            space = " " * (8 - word_len)
            posts += "%s%s" %(word, space)


        posts += '\n'

    return posts

def make_pitcher_table(pitchers):

    posts = ""
    posts += "  投    投局 面打  被   被   四  三  失  自  滾  飛   Ｅ\n"
    posts += "  手    球數 對席 安打 全壘  壞  振  分  責  地  球   RA\n"
    for pitcher in pitchers:
        posts += "  %-4s   %3s  %2d   %2d   %2d   %2d  %2d  %2d  %2d  %2d  %2d  %.2f\n" %(pitcher.number, pitcher.IP(), pitcher.TBF, pitcher.H, pitcher.HR, pitcher.BB, pitcher.K, pitcher.Run, pitcher.ER, pitcher.GO, pitcher.FO, pitcher.getERA())
    
    return posts


def digit2FullWidth(n):
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
    elif( n == 10 ):
        return "十"
    else:
        print "Error! Unsupported digit %d!" %n
        sys.exit(0)

def pos2word(pos, res):
    word = ""
    if( pos == "1" ):
        if( res == "1B" ):
            word = "內"
        else:
            word = "投"
    elif( pos == "2" ):
        if( res == "1B" ):
            word = "內"
        else:
            word = "補"
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

def res2word(pa, wordLen):
    res = pa.result
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
        elif( res == "FO" ):
            word = "界飛"
        else:
            print "Error! Unknown res notation %s" %res
            sys.exit(0)  

    n = 0
    if( pa.rbi != 0 ):
        word += str(pa.rbi)
        n += 1
    if( pa.run != 0 ):
        word += "r"
        n += 1

    return word, n

def end2word(pa):
    word = ""
    if( pa.endInning in ["#", "!"] ):
        word += "#"
    if( (pa.note != 0) & (pa.note != 'X') ):
        word += pa.note

    return word, len(word)

def PA2Character(pa, isAddColor):
    if( not pa.isPlay ):
        word = ("　　") # Full-Width white
        word_len = 4
    else:
        if( pa.pos == 0 or pa.pos == None ):
            word, n = res2word(pa, 2)
        else:
            pos_word = pos2word(pa.pos, pa.result)
            res_word, n = res2word(pa, 1)
            word = pos_word + res_word

        word_len = 4 + n
        if( isAddColor ):
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



def dump_player_statistic(team):
    
    # Batter Statistic
    posts = "Team: %s\n" %team.name
    posts += "Batting:\n"
    posts += "          PA  AB  1B  2B  3B  HR  DP RBI RUN  BB   K  SF\n"
    for p in team.batters:
        space = " " * (6 - big5len(p.number) )
        line = "%2s. %s%s" %(p.order, p.number, space)
        line += "%2d  %2d  %2d  %2d  %2d  %2d  %2d %3d %3d  %2d   %d  %2d\n" %(p.PA, p.AB, p.B1, p.B2, p.B3, p.HR, p.DP, p.RBI, p.RUN, p.BB, p.K, p.SF)
        posts += line

    posts += '\nPitching:\n'
    posts += " No.    IP  PA   H  HR  BB   K  Run  ER  GO  FO\n" 
    # Pitcher Statistic
    for p in team.pitchers:
        posts += " %-8s%3s  %2d  %2d  %2d  %2d  %2d  %3d  %2d  %2d  %2d\n" %(p.number, p.IP(), p.TBF, p.H, p.HR, p.BB, p.K, p.Run, p.ER, p.GO, p.FO)

    return posts


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


