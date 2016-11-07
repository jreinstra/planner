# Cardinal Planner
This is the main code repository for the cardinal planner project.

View current production version: https://www.cardinalplanner.com/

## Setting up your local environment

Follow the below checklist to setup your local Django environment:

1. Set up and enter a [new virtual environment
](https://hackercodex.com/guide/python-development-environment-on-mac-osx/). Stay in this virtual environment when working.
- Clone the repository into a new folder
- Go into the new folder
- Install all pip requirements: `pip install -r requirements.txt`
- Copy the file `planner/local_settings_sample.py` into `planner/local_settings.py`
- Run all migrations: `python manage.py migrate`
- Start the server by running: `python manage.py runserver`.  It'll be up at `localhost:8080`
- Create yourself an admin user account for testing: `python manage.py createsuperuser`.
- Create some test data: `python manage.py setup_data`.

If you have any trouble with the checklist, feel free to suggest changes to the checklist to make this easier for future people!