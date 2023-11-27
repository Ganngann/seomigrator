#!/bin/bash

# Start the service if it's not already running
if [ "$(docker-compose ps -q web)" = "" ]; then
  docker-compose up -d web
fi

# Enter the Docker container
docker-compose exec web bash
