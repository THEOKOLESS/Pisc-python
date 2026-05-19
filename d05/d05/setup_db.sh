#!/bin/bash
sudo service postgresql start
sudo -u postgres psql -c "CREATE USER djangouser WITH PASSWORD 'secret';"
sudo -u postgres psql -c "CREATE DATABASE formationdjango OWNER djangouser;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE formationdjango TO djangouser;"
