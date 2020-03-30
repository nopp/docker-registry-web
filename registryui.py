#!/usr/bin/python3
from flask import Flask,render_template
from lib.drweb import *

app = Flask(__name__)

drweb = Drweb()

@app.route("/repo/<repo>",methods=['GET'])
def repo(repo):
    realName = repo.replace(".","/") # little hammer for repository with slashes ex: juca/loco -> juca.loco -> juca/loco
    return render_template('repo.html',tags=drweb.listTags(realName),repo=realName,drweb=drweb)

@app.route("/image/<repo>/<version>",methods=['GET'])
def image(repo,version):
    return drweb.infoTag(repo,version)

@app.route("/")
def index():
    return render_template('index.html',catalogs=drweb.listCatalogs(drweb.appConfig["registry_url"]),drweb=drweb)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8083)