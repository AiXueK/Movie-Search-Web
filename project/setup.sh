#!/bin/bash

echo "This script will download and setup all the backend dependencies"
echo
echo "Installing pip..."
echo

version=$(which pip)
path="/usr/bin/pip"

if [ "$path" == "$version" ];
then
  echo "PIP is already installed"
  echo
else
  sudo apt update
  sudo apt install python3-pip
fi

echo "Installing psql..."
echo

version=$(which psql)
path="/usr/bin/psql"

if [ "$path" == "$version" ];
then
  echo "PSQL is already installed"
  echo
else
  sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
  sudo apt-get update
  sudo apt-get -y install postgresql
fi

echo "Changing password for user postgres to 'admin'..."
echo

echo "If asked [sudo] password for lubuntu:"
echo "Enter lubuntu"
echo

echo "Please enter admin for the new password"
echo

sudo passwd postgres

#sudo service postgresql start

sudo -i -u postgres psql << EOF
       alter user postgres with password 'admin';
       CREATE DATABASE "MovieFinder";


EOF

echo
echo "SUCCESS"
echo

echo "Creating tables MovieFinder, users and importing movies_initial.csv into MovieFinder"
echo

sudo psql postgresql://postgres:admin@localhost/MovieFinder << EOF
       create table if not exists "MovieFinder"(id INT, name text, genre text, director text, actor text, poster text, description text, rating real, year INT);

       create table if not exists users(uid INT PRIMARY KEY NOT NULL, email CHAR(50) NOT NULL, pass_hash CHAR(64), otc CHAR(6), tmp INT, username text, token text, wishlist text, review jsonb[], banlist text);

       \copy "MovieFinder" (id, name, genre, director, actor, poster, description, rating, year) FROM '/home/lubuntu/cs3900/capstone-project-3900-m18a-sigmagrindset/project/movies_initial.csv' CSV HEADER DELIMITER ',';

       alter table "MovieFinder" add ratings jsonb[];
       alter table "MovieFinder" add review jsonb[];


EOF

echo "SUCCESS"
echo

echo "Downloading nltk..."
echo

sudo pip3 install nltk

echo
echo "SUCCESS"
echo

echo "Downloading scikit-learn..."
echo

sudo pip install -U scikit-learn

echo
echo "SUCCESS"
echo

echo "Downloading flask..."
echo

sudo pip install flask

echo
echo "SUCCESS"
echo

echo "Downloading sqlalchemy..."
echo
sudo apt-get install python3-sqlalchemy

echo "SUCCESS"
echo

echo "Downloading flask-sqlalchemy..."
echo
pip3 install flask-sqlalchemy

echo "SUCCESS"
echo

echo "Downloading pandas..."
echo
pip install pandas

echo "SUCCESS"
echo

echo "Downloading psycopg..."
echo
pip install psycopg2-binary

echo "SUCCESS"
echo

echo "Downloading flask-cors..."
echo
pip install -U flask-cors

echo "SUCCESS"
echo
