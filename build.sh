#!/bin/bash

# Exit in case of error
set -e

# Build and run containers
docker-compose -f docker-compose-dev.yml up -d

# Hack to wait for postgres container to be up before running alembic migrations
sleep 5;

# Run migrations
# docker-compose run --rm api alembic downgrade base

docker-compose -f docker-compose-dev.yml run --rm api alembic upgrade head


# Create initial data
# docker-compose run --rm api python3 app/initial_data.py