#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from parse_record import load_data_from_string, parse_game_data
from dump_record import make_PTT_format, make_database_format
import re

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/convert.json', methods=["POST"])
def convert():
    print "get content from html..."
    data1 = request.form["text1"].encode('utf8')
    data2 = request.form["text2"].encode('utf8')
    
    data_all = data1 + '\n' + data2

    print "parse game data..."
    raw_data = load_data_from_string(data_all)
    game = parse_game_data(raw_data)
    post_ptt = make_PTT_format(game, 0)

    return jsonify({'result': post_ptt})

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

