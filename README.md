## Django Expense Tracker

A Django application for tracking expenses in various categories.

### Installation

These steps will guide you through setting up this app using the minimum requirements (sqlite3 database, hosted at localhost).

It is recommended to install the requirements into and run python from a virtual env. Adjust the name of your pip/python binaries or paths as needed.

#### 1. Clone this repo

Clone this repo into a directory where you would like to store the source files.

`git clone git@github.com:skymaya/django-expense-tracker.git .`

#### 2. Install requirements

Navigate to the directory where you cloned the source. You should be at the same level as requirements.txt and manage.py. Use the following command to install any required python packages:

`pip install -r requirements.txt`

#### 3. Database migrations

Use the following command to set up the database:

`python manage.py migrate`

#### 4. Static files

Use the following command to collect the static files:

`python manage.py collectstatic`

#### 5. Create a superuser

Use the following command to create a superuser:

`python manage.py createsuperuser`

#### 6. Run tests

Use the following command to run tests:

`python manage.py test`

The tests should all pass. Please file an issue if they don't.

#### 7. Run application

Use the following command to run the application on localhost:

`python manage.py runserver`

Your should then be able to access http://127.0.0.1:8000/ in a browser and see a login screen. Please file an issue if you are unable to after performing all of the above steps.
