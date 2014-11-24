#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from parse_record import parse_game_record
from player import Game

import re

app = Flask(__name__)

def text_to_table(text):
    
    table = []
    lines = text.split('\n')
    for line in lines:
        data = line.split()
        data = filter(None, data)
        if len(data) != 0:
            table.append(data)
    
    return table

def gather_team_info(request, HA, record_str):

    team_name  = request.form[HA + "_team_name"]
    scores = []
    for i in range(1, 8):
        score = request.form[HA + "_score_" + str(i)]
        if( not score ):
            break
        scores.append(int(score))

    table = text_to_table(record_str)

    return (team_name, scores, table)

@app.route('/', methods=["GET","POST"])
def index():
    
    game = Game()
    away_record = ""
    home_record = ""    
    print request.form
    if( request.method == "POST" ):

        game_type   = request.form["game_type"].encode('utf8')
        date        = request.form["date"]
        location    = request.form["location"].encode('utf8')
        game_id     = request.form["game_id"]
        game_id = str(date).replace("-", "") + str(game_id)
        away_record = request.form["away_record"]
        home_record = request.form["home_record"]
    
        (away_team_name, away_scores, away_table) = gather_team_info(request, "away", away_record)
        (home_team_name, home_scores, home_table) = gather_team_info(request, "home", home_record)
        
        game, err = parse_game_record(away_team_name, away_scores, away_table, \
                                      home_team_name, home_scores, home_table)
        
        game.game_type  = game_type
        game.date       = date
        game.location   = location
        game.game_id    = game_id
    
    '''
    if( 'download' in request.form and err == "" ):
        filename = '%s.txt' %game.game_id
        filepath = 'rd/%s' %filename

        with open(filepath, 'w') as f:
            f.write(game.post_ptt)
            print "Save %s" %filepath

        response = HttpResponse(FileWrapper( file(filepath) ), content_type=mimetypes.guess_type(filepath)[0] )
        response['Content-Disposition'] = 'attachment; filename=%s' %filename
        response['Content-Length'] = os.path.getsize(filepath)
        
        return response
    '''
    #print "parse game data..."
    #raw_data = load_data_from_string(data_all)
    #game = parse_game_data(raw_data)
    #post_ptt = make_PTT_format(game, 0)
    return render_template("index.html", game=game, away_record=away_record, home_record=home_record, warning=err)




if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

