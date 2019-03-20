# Registry UI
  Simple Docker registry v2 viewer
  
  Under development ;)
  
Running local
=============
1) pip3 install -r requirements.txt
2) Edit config.json with your informations
3) Create /etc/registry-ui
4) Copy config.json to /etc/registry-ui
5) python3 registryui.py

Running with local Docker
=========================
1) docker build -t registry-ui .
2) docker run -d -e title='titleOfthisApp' -e registryurl="http://registry.url.com" -p 8083:8083 registry-ui

To access: http://localhost:8083

Running from hub.docker.com image
==================================
1) docker run -d -e title='titleOfthisApp' -e registryurl="http://registry.url.com" -p 8083:8083 nopp/registry-ui:0.1

Screenshot v0.1
===============
![Image Alt](https://i.imgur.com/W2BXzAI.png)
![Image Alt](https://i.imgur.com/7NYdak1.png)

