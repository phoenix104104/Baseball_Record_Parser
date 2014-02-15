#!/usr/bin/python
from flask import Flask, render_template, request, jsonify
from StringIO import StringIO

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/record.json', methods=["POST"])
def pass_content():
    print "get content from html:"
    data = request.form
    print data
    for key in data.keys():
        print key
    
    #arr = data.getlist("data[0][PA][]")
    #print arr
    return jsonify({'result': "got data!"})

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

