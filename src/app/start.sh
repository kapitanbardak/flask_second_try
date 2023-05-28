#!/bin/bash
  sleep 15
  if [ ! -d './app/migrations' ]; then
    flask db init
  fi
  flask db migrate
  flask db upgrade
  python -m flask run --host=0.0.0.0
