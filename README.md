# Registry UI
  Simple Docker registry v2 viewer
  
  Under development ;)

Docker local
============
  docker build -t registry-ui .
  
  docker run -d -e title='titleOfthisApp' -e registryurl="http://registry.url.com" -p 8083:8083 registry-ui

  To access: http://localhost:8083

Docker image from hub.docker.com
================================
  docker run -d -e title='titleOfthisApp' -e registryurl="http://registry.url.com" -p 8083:8083 nopp/registry-ui:0.1

Screenshot v0.1
===============
![Image Alt](https://i.imgur.com/W2BXzAI.png)
![Image Alt](https://i.imgur.com/7NYdak1.png)

