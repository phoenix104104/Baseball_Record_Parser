#!/usr/bin/python
from flask import Flask, render_template, request, jsonify
from StringIO import StringIO

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("form.html")

@app.route('/test.json', methods=["POST"])
def pass_content():
    print "get content from html:"
    txt = request.form["text"]
    print txt
    return jsonify({'result': txt})

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

