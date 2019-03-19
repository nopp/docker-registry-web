#!/usr/bin/python3
from flask import Flask,render_template, jsonify
import urllib.request
import requests
import json

app = Flask(__name__)

url = "http://registry.lalala.com"

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

# @app.route("/size")
# def size():
#     teste = {"layers": [
#       {
#         "digest": "sha256:6ae821421a7debccb4151f7a50dc8ec0317674429bec0f275402d697047a8e96", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 22500288
#       }, 
#       {
#         "digest": "sha256:187061ad2a2978b8c52f307ede3a915e9134a3bb8f6ea795e67ad31524381cdd", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 454874
#       }, 
#       {
#         "digest": "sha256:c3e07dee1e7e6bfded60c645d3d9e45bcebe2f8b44e74bf72e08dc1e4fb8c43a", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 223
#       }, 
#       {
#         "digest": "sha256:9703bd99cc4e2d2c93c7346046d96e5ca406f66233267e835c3bee7591a8b092", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 247
#       }, 
#       {
#         "digest": "sha256:9f0990bb7f893767d87d3ccbed0f56dbfe766648ac7231b2c36b1a9a4d109a35", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 130
#       }, 
#       {
#         "digest": "sha256:b8143d8fede809da5eb5a9f62c7b1eb6dcdff7251d06f38b681a3bd292a9cf5e", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 77134485
#       }, 
#       {
#         "digest": "sha256:0eb0dd4925e1f05b09788d659dfcd3114818f649d82360b10d417fa08ce3ca9c", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 126
#       }, 
#       {
#         "digest": "sha256:7bb28543650936a119a8085ef7665c865f3930fadba42d701803b03cd8c73d40", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 16914811
#       }, 
#       {
#         "digest": "sha256:4083577e996ef5d6a25d19a6ddf21be64d6263e840da45203f8fdb6b7e0959b4", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 599
#       }, 
#       {
#         "digest": "sha256:36de04108fd5ef9fb8af7ffb236b4ead900ed970f2487f43157add1be85bfeff", 
#         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip", 
#         "size": 60558432
#       }
#     ]}
#     size = imageSize(teste)
#     return size

@app.route("/")
def index():
    return render_template('index.html',catalogs=listCatalogs(url),base=url)

if __name__ == "__main__":
    app.run(debug=True)
