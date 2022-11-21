# Project-Hospital

## Contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Current Status](#current-status)

### General Info
This is a medical facility management application written in the Django framework. It is used for managing doctors' time, making appointments by patients. 
It is designed for three types of users who are assigned different functions:
- admin - Adding doctors, deleting reviews, approving working hours. (It is not the standard Django admin panel)
- pacient - Ability to add reviews, make appointments 
- doctor - Set working time, add notes to visits
### Technologies
Main technologies I used in the project.
* Python 3.10
* Django 4.1.1 

To slightly improve the look of the site.
* django-crispy-forms 1.14.0
* Bootstrap 5

Technologies used during the writing of the test.
* pytest 7.1.3
* pytest-django 4.5.2

Used exclusively to write commands that fill data for the database.
* Faker 15.0.0 

I also used a relational database SQL.
* SQLite 3
### My tips during setup
1. After cloning the repository, you need to configure "Settings.py" at the start. You need to add a database connection and configure the application's email. The best way to do this is to create a file named "local_settings.py" and place it in the website directory. 

My "local_settings.py"

![Zrzut ekranu 2022-11-21 o 01 55 35](https://user-images.githubusercontent.com/102543225/202936976-fad4f0e8-b77d-4ccd-bf3a-74f403b1d0a6.png)

2. To fill the database with users, you can use:
```
python3 manage.py setdefaultdatabase
```
This command creates users:

login: admin, password: admin<br />
login: doctor, password: doctor<br />
login: patient, password: patient<br />
You can use them to test applications.

3. The command above doesn't create the desired appointments, so I recommend logging in as a doctor, setting your working hours, then using admin to confirm that. Next you should login as a patient and try to make an appointment.

### Current Status
My three next development paths:
1. Writing tests in Pytest / At the moment I'm focusing on this.
2. Adding the ability to write articles by doctor. (Django CKEditor)
3. Expansion with another type of user (receptionist).
