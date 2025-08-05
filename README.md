# Runnr.ai integration developer assessment
This repository contains working Django code. Run your code locally, you don't need any external services.

## Prerequisites:
- use Python version 3.13
- install dependencies by running: `pip install -r requirements.txt`

## Migrate database and run server
`python manage.py migrate`
`python manage.py createsuperuser`
`python manage.py init_data`
`python manage.py runserver 0.0.0.0:8000`

## Relevant information for backend developers
- The file `views.py` contains a webhook endpoint to receive updates from the PMS. These updates don't contain any details of the actual reservations. They require you to fetch additional details of any reservation.
- The file `external_api.py` mocks API calls that are available to you to get additional guest and reservation details. Note that the API calls sometimes generate errors, or invalid data. You should deal with those in the way you see fit.
- The file `pms_systems.py` contains an AbstractBaseClass and a ChildClass of a `PMS`. You will find explanations of what all the methods do inside the methods of the ABC.
- The file `models.py` contains your database models. The models should be mostly self-explanatory. Relations are defined and some columns have `help_text`.

## Relevant information for frontend developers
- The file `views.py` contains an endpoint that renders the a chat page called `chat`. It also contains an endpoint that returns a json with chat data called `chat_data`.
