#! /bin/bash

psql postgresql://postgres:postgres@localhost << EOF
       create database moviefinder;
EOF
psql -d moviefinder << EOF
       create table users(uid INT PRIMARY KEY, email CHAR(50) NOT NULL, pass_hash CHAR(64), otc CHAR(6), tmp INT);
EOF
