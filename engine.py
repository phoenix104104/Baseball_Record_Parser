#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from parse_record import parse_game_record
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

def gather_team_info(request, HA):

    team_name  = request.form[HA + "_team_name"]
    scores = []
    for i in range(1, 8):
        score = request.form[HA + "_score_" + str(i)]
        if( not score ):
            break
        scores.append(int(score))

    record_str = request.form[HA + "_record"]
    table = text_to_table(record_str)

    return (team_name, scores, table)

@app.route('/', methods=["GET","POST"])
def index():
    
    if( request.method == "POST" ):
        print "get content from html..."

        game_type   = request.form["game_type"].encode('utf8')
        date        = request.form["date"]
        location    = request.form["location"].encode('utf8')
        game_id     = request.form["game_id"]
        game_id = str(date).replace("-", "") + str(game_id)

        (away_team_name, away_scores, away_table) = gather_team_info(request, "away")
        (home_team_name, home_scores, home_table) = gather_team_info(request, "home")
        
        record, err = parse_game_record(away_team_name, away_scores, away_table, \
                                        home_team_name, home_scores, home_table)

    else:
        data_all = 'hello'

    #print "parse game data..."
    #raw_data = load_data_from_string(data_all)
    #game = parse_game_data(raw_data)
    #post_ptt = make_PTT_format(game, 0)
    
    return render_template("index.html")




if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

