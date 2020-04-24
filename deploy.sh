#!/bin/sh

printf 'Starting Building Docker Container'
docker build -t text2meme-bot .

docker stop text2meme-bot && docker rm text2meme-bot && docker image prune -f

printf 'Running Docker Container'
docker run -d \
	--name=text2meme-bot \
	--network=host \
	--restart=always \
	-p 5005:5005 \
	-v /etc/localtime:/etc/localtime:ro \
	-v /etc/timezone:/etc/timezone:ro \
text2meme-bot

exit 0