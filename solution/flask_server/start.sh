#!/bin/bash

app="docker.test"
docker build -t ${app} .
docker run -d -p 56733:80 \
    --name=${app} \
    -e FLASK_DEBUG=1 \
    -e FLASK_ENV=development \
    -v $PWD:/app ${app}
