#!/usr/bin/python
from flask import Flask, render_template, request, jsonify
from StringIO import StringIO

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/convert.json', methods=["POST"])
def convert():
    print "get content from html:"
    data1 = request.form["text1"]
    data2 = request.form["text2"]
    print data1
    print data2
    
    return jsonify({'result': "got data!"})

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

