#!/bin/bash

docker build -t fastapi .
docker run -d -p 8080:8080 -e BIND="0.0.0.0:8080" fastapi
