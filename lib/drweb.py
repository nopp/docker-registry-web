from datetime import datetime
import dateutil.parser as dp
from flask import jsonify
import requests
import json

class Drweb:

    appConfig = json.load(open("/etc/registry-ui/config.json"))

    def bytes_to(self,bytes,to,bsize=1024):
        try:
            convertOptions = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
            newType = float(bytes)
            for i in range(convertOptions[to]):
                newType = newType / bsize
            return(newType)
        except:
            return "ErrorLib - Can't convert bytes to "+to

    def listCatalogs(self,url):
        try:
            listCatalogs = {}
            catalogs = json.loads(requests.get(self.appConfig["registry_url"]+"/v2/_catalog").text)
            for catalog in catalogs['repositories']:
                listCatalogs[catalog] = self.listTags(catalog)        
            return listCatalogs
        except Exception as e:
            return(str(e))

    def listTags(self,repo):
        try:
            tagsList = []
            tags = json.loads(requests.get(self.appConfig["registry_url"]+"/v2/"+repo+"/tags/list").text)
            for tag in tags['tags']:
                tagsList.append(tag)
            return tagsList
        except Exception as e:
            return(str(e))

    # Return size in MB
    def imageSize(self,layers):
        total = 0
        for layer in layers:
            total = total + layer["size"]
        return str(round(self.bytes_to(total,"m"),2))

    def infoTag(self,repo,version):
        try:
            tag = {}
            info = {}
            headers = {'accept': 'application/vnd.docker.distribution.manifest.v2+json'}   
            infoTag = requests.get(self.appConfig["registry_url"]+"/v2/"+repo+"/manifests/"+version).json()
            info["name"] = repo
            info["architecture"] = infoTag['architecture']
            info["history"] = infoTag['history']
            moreInfo = json.loads(info["history"][0]["v1Compatibility"])
            info["os"] = moreInfo["os"]
            info["created"] = dp.parse(moreInfo["created"])
            info["layers"] = requests.get(self.appConfig["registry_url"]+"/v2/"+repo+"/manifests/"+version,headers=headers).json()["layers"]
            info["totalSize"] = self.imageSize(info["layers"])
            tag[repo] = info
            return tag
        except Exception as e:
            return(str(e))