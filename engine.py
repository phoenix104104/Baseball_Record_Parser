#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, make_response, send_from_directory
from parse_record import parse_game_record, load_record_file
from player import Game
import sys, os, re, mimetypes

app = Flask(__name__)
upload_folder = 'upload'
allowed_extensions = set(['txt', 'rd'])
app.config['UPLOAD_FOLDER'] = upload_folder

def table_to_text(table):
    lines = ""
    for row in table:
        for col in row:
            lines += "%s\t" %col
        lines += "\n"
    
    return lines

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

    team_name  = request.form[HA + "_team_name"].encode('utf8')
    scores = []
    for i in range(1, 8):
        score = request.form[HA + "_score_" + str(i)]
        if( not score ):
            break
        scores.append(int(score))

    table = text_to_table(record_str)

    return (team_name, scores, table)

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions

@app.route('/', methods=["GET","POST"])
def index():

    game_type   = ""
    date        = None
    game_id     = ""
    location    = ""
    away_team_name  = ""
    away_scores     = []
    away_table      = []
    away_record     = ""
    home_team_name  = ""
    home_scores     = []
    home_table      = []
    home_record     = ""

    warning = ""
    load_file  = False
    parse_game = False
        
    if( "reset" in request.form ):
        return render_template("index.html", game=Game(), id='', away_record='', home_record='', warning='')

    if( request.method == "POST" ):
    
        # parse from upload file
        if( 'upload_file' in request.files ):
            f = request.files['upload_file']
            
            if( f ):
                load_file = True
                if is_allowed_file(f.filename):
                    filepath = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
                    f.save(filepath)
                    print "save %s\n" %filepath
                    warning = 'upload %s' %f.filename
        
                
                    game_type, date, game_id, location, \
                    away_team_name, away_scores, away_table, \
                    home_team_name, home_scores, home_table = load_record_file(filepath)
                    
                    away_record = table_to_text(away_table)
                    home_record = table_to_text(home_table)
                    parse_game = True
                else:
                    warning = 'Not allowed file extension: %s' %os.path.splitext(f.filename)[-1]
             
        # parse from web
        if( not load_file ):
            game_type   = request.form["game_type"].encode('utf8')
            date        = request.form["date"]
            location    = request.form["location"].encode('utf8')
            game_id     = request.form["game_id"].encode('utf8')
            away_record = request.form["away_record"]
            home_record = request.form["home_record"]
        
            (away_team_name, away_scores, away_table) = gather_team_info(request, "away", away_record.encode('utf8'))
            (home_team_name, home_scores, home_table) = gather_team_info(request, "home", home_record.encode('utf8'))
    
            parse_game = True
    
    if( parse_game ):
        print "parse_game" 
        game, err = parse_game_record(away_team_name, away_scores, away_table, \
                                      home_team_name, home_scores, home_table)
        
        game.game_type  = game_type
        game.date       = date
        game.location   = location
        game.game_id    = game_id
        game.away.raw_record = away_record.encode('utf8')
        game.home.raw_record = home_record.encode('utf8')

        if( err == "" ):
            
            filename = '%s-%s-%s' %(game.game_id, away_team_name, home_team_name)

            # save record file
            filepath = 'rd/%s.rd' %filename
            game.save_game(filepath)
            
            # save output file (PTT format + statistic results)        
            filepath = 'rd/%s.txt' %filename
      
            output = ""
            output += "%s %s (%s)\n\n" %(str(date), game_type, location)
            output += game.post_ptt
            output += "\n"
            output += game.post_db

            with open(filepath, 'w') as f:
                f.write(output)
                print "Save %s" %filepath

            return render_template("index.html", game=game, id=game_id, away_record=away_record, home_record=home_record, warning=err, preview=True)

        else:
            return render_template("index.html", game=game, id=game_id, away_record=away_record, home_record=home_record, warning=err)

    

    if( 'download_ptt' in request.form and err == "" ):
        print "download ptt"
        filepath = 'rd/%s.txt' %filename
        with open(filepath, 'r') as f:
            output = f.read()
            response = make_response(output)
            response.headers['Content-Type'] = mimetypes.guess_type(filepath)[0]
            response.headers['Content-Disposition'] = 'attachment; filename=%s.txt' %filename
            response.headers['Content-Length'] = os.path.getsize(filepath)
            return response


    if( 'download_rd' in request.form and err == "" ):
        print "download_rd"
        filepath = 'rd/%s.rd' %filename
        with open(filepath, 'r') as f: 
            output = f.read()
            response = make_response(output)
            response.headers['Content-Type'] = mimetypes.guess_type(filepath)[0]
            response.headers['Content-Disposition'] = 'attachment; filename=%s.rd' %filename
            response.headers['Content-Length'] = os.path.getsize(filepath)
            return response


    return render_template("index.html", game=Game(), id='', away_record='', home_record='', warning=warning)


if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding('utf8')
    app.debug = True
    app.run(host='0.0.0.0', port=80)

