#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from parse_record import parse_record_from_web
import re

app = Flask(__name__)

def gather_team_info(request, HA):

    record_str = request.form[HA + "_record"]
    team_name  = request.form[HA + "_team_name"]
    scores = []
    for i in range(1, 8):
        score = request.form[HA + "_score_" + str(i)]
        if( not score ):
            score = 0
        scores.append(int(score))

    return (team_name, scores, record_str)

@app.route('/', methods=["GET","POST"])
def index():
    
    if( request.method == "POST" ):
        print "get content from html..."

        game_type   = request.form["game_type"].encode('utf8')
        date        = request.form["date"]
        location    = request.form["location"].encode('utf8')
        game_id     = request.form["game_id"]
        game_id = str(date).replace("-", "") + str(game_id)

        (away_team_name, away_scores, away_record) = gather_team_info(request, "away")
        (home_team_name, home_scores, home_record) = gather_team_info(request, "home")
        
        record, err = parse_record_from_web(away_team_name, away_scores, away_record, \
                                            home_team_name, home_scores, home_record)

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

