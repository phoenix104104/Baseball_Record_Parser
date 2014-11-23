#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from parse_record import load_data_from_string, parse_game_data
from dump_record import make_PTT_format, make_database_format
import re

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    
    if( request.method == "POST" ):
        print "get content from html..."

        game_type   = request.form["game_type"].encode('utf8')
        date        = request.form("date")
        location    = request.form("location")
        game_id     = request.form("game_id")
        away_record = request.form["away_record"].encode('utf8')
        home_record = request.form["home_record"].encode('utf8')
        
        print date
    else:
        data_all = 'hello'

    #print "parse game data..."
    #raw_data = load_data_from_string(data_all)
    #game = parse_game_data(raw_data)
    #post_ptt = make_PTT_format(game, 0)
    
    print data_all
    return render_template("index.html", data=data_all)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)

