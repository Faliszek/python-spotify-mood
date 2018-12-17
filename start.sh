
#usr#!/bin/sh

APP_NAME=spotify-mood

docker stop "$APP_NAME" &&
echo "Stoping container ..."
docker rm "$APP_NAME" &&
echo "Removing container ..."
docker build -t "$APP_NAME" . &&

docker run -i --name spotify-mood \
-p 8080:8080 \
-v $(pwd)/app:/app \
-e FLASK_APP=main.py \
-e FLASK_DEBUG=1 spotify-mood flask run --host=0.0.0.0 --port=8080