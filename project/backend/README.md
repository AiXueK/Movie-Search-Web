First install psql on your system and make sure the psql server is running. You can search online how to start a psql server on your os


How to create the user database
In the project/backend directory there is a shell script called datashell.sh.

First make sure you have executable permissions on the shell using 'chmod 755 datashell.sh' if you're on linux

Make sure the password of the user 'postgres' on your system is 'admin'
Then run the shell using ./datashell.sh


If you want to manually create the database yourself it is called moviefinder and the table is called users. The table has the following columns,
uid INT PRIMARY KEY
email CHAR(50) NOT NULL
pass_hash CHAR(64)
otc CHAR(6)
tmp INT
