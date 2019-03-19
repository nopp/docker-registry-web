#!/bin/bash
sed -i s/xxx/"$title"/ /etc/registry-ui/config.json
sed -i "s|yyy|$registryurl|" /etc/registry-ui/config.json

/usr/bin/python3 drweb.py