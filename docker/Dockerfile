FROM alpine:3.9

LABEL maintainer "Carlos Augusto Malucelli <malucellicarlos@gmail.com>"

RUN apk update \
		&& apk add python3 py3-pip git bash \
		&& git clone https://github.com/nopp/registry-ui.git \
		&& cd registry-ui \
		&& pip3 install -r requirements.txt \
		&& mkdir /etc/registry-ui \
		&& mv config.json /etc/registry-ui/config.json

WORKDIR /registry-ui

COPY docker/run.sh /registry-ui/run.sh

RUN chmod +x /registry-ui/run.sh

EXPOSE 8083

ENTRYPOINT ["./run.sh"]

