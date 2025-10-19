#!/bin/sh
flask --app cms_api.db_migrate db upgrade
gunicorn -b 0.0.0.0:5000 -w 4 "cms_api.catechism_app_api:create_app()"