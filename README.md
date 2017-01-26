# ApplesAndOranges
# Theatres and Shows Matching System
# Team Members: Xueguang Lu, Ran Liu, Patrick Zhang, Yuan Xie








## Requirements
Python 3.4+
Django 1.9.6


## Installation
If you're on windows and need psycopg package installed use this pre-compiled version:
http://stickpeople.com/projects/python/win-psycopg/

## This setup uses django built-in sqlite, so we will skip setting up DB

## Environment

#Install Virtualenv
pip3 install virtualenv

#check your python3
which python

#Activate your own vitualenv.
virtualenv $PATH -p python3
(Note that when you modify backend, do not commit/push your virtualenv-related files)

#Syncdb
python3 manage.py syncdb
python3 manage.py createsuperuser    # admin / manager


#when ORM changed:
python3 manage.py makemigrations (--name changed_my_model your_app_label)
python3 manage.py migrate

#Runserver
python3 manage.py runserver $IP_ADDR:PORT_NUM


#Install dependency
pip3 install -r reqreuiments.txt

## Contributors
* Patrick Zhang, patdujour@gmail.com
* Xueguang Lu, xueguang.lu@gmail.com
* Ran Liu,
* Yuan Xie,

