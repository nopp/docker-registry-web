#!/usr/bin/python3
from flask import Flask,render_template, jsonify
import urllib.request
import requests
import json

app = Flask(__name__)

url = "http://registry.preventsenior.com.br"

def bytes_to(bytes,to,bsize=1024):
    try:
        convertOptions = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
        newType = float(bytes)
        for i in range(convertOptions[to]):
            newType = newType / bsize
        return(newType)
    except:
        return "ErrorLib - Can't convert bytes to "+to

def listCatalogs(url):
    try:
        listCatalogs = {}
        catalogs = json.loads(urllib.request.urlopen(url+"/v2/_catalog").read())
        for catalog in catalogs['repositories']:
            listCatalogs[catalog] = listTags(catalog)        
        return listCatalogs
    except Exception as e:
        return(str(e))

def listTags(repo):
    try:
        tagsList = []
        tags = json.loads(urllib.request.urlopen(url+"/v2/"+repo+"/tags/list").read())
        for tag in tags['tags']:
            tagsList.append(tag)
        return tagsList
    except Exception as e:
        return(str(e))

# Return size in MB
def imageSize(layers):
    total = 0
    for layer in layers:
        total = total + layer["size"]
    return str(round(bytes_to(total,"m"),2))

def infoTag(repo,version):
    try:
        tag = {}
        info = {}
        headers = {'accept': 'application/vnd.docker.distribution.manifest.v2+json'}   
        infoTag = requests.get(url+"/v2/"+repo+"/manifests/"+version).json()
        info["name"] = repo
        info["architecture"] = infoTag['architecture']
        info["history"] = infoTag['history']
        info["layers"] = requests.get(url+"/v2/"+repo+"/manifests/"+version,headers=headers).json()["layers"]
        info["totalSize"] = imageSize(info["layers"])
        tag[repo] = info
        return jsonify(tag)
    except Exception as e:
        return(str(e))

@app.route("/image/<repo>/<version>",methods=['GET'])
def image(repo,version):
    return infoTag(repo,version)

@app.route("/")
def index():
    return render_template('index.html',catalogs=listCatalogs(url),base=url)

if __name__ == "__main__":
    app.run(debug=True)