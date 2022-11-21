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
* PostgreSQL
### Setup 
### Current Status
My three next development paths:
1. Writing tests in Pytest / At the moment I'm focusing on this.
2. Adding the ability to write articles by doctor. (Django CKEditor)
3. Expansion with another type of user (receptionist).
