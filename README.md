# Cardinal Planner
This is the main code repository for the cardinal planner project.

View current production version: http://cardinalplanner.com/

## Setting up your local environment

Follow the below checklist to setup your local Django environment:

- Set up and enter a [new virtual environment
](https://hackercodex.com/guide/python-development-environment-on-mac-osx/)- Clone the repository into a new folder
- Go into the new folder
- Install all pip requirements: `pip install -r requirements.txt`
- Run all migrations: `python manage.py migrate`
- Copy the file `planner/local_settings_sample.py` into `planner/local_settings.py`
- Start the server by running: `python manage.py runserver`.  It'll be up at `localhost:8080`
- Create yourself an admin user account for testing: `python manage.py createsuperuser`.

## Central Goal
The **central goal** to create the best way (by far) for students to plan their long term and short term schedules.

## Specific Functionality Goals

_features in italics_ = Nice to have features that aren't mission-critical.

- Course catalog
  - Great search, sorting, and filtering abilities
  - Useful short descriptions
  - Beautiful and fast
  - AJAX support
  - Comprehensive and up-to-date (crawls official site regularly)
  - Ability to star / save classes to list
  - _Helpful tags in search results_
- Course reviews / course page
  - Amazon-level review functionality (helpful/not helpful, verified student, replies, etc)
  - Sensible display of grade breakdown
  - Comments and comment replies, _sorting_ and likes
  - Sensible display of class times and available quarters (parse the text)
  - Ability to star / save classes to lists
  - _Intelligent ‘related courses’ view_
- Login / users
  - Only necessary for saving classes / planner
  - Quick login with Facebook / SUNet (maybe Google) => popover like reddit
  - _Allow Facebook login to find (invite?) & connect with friends_
- Planner
  - Specify major / minors / subjects you like
  - Displays your coverage of graduation requirements (general and for major/minor)
  - Trello-like dragging and dropping of classes (w/ AJAX)
  - _Pulls from axess to fill in classes you’ve already taken => verifies_
  - _Allow users to sign up for classes directly within platform (queries Axess API)_
  - _Learns from other users to suggest classes => some AI involved here_
- General
  - Homepage dashboard that's not just a search bar
  - _Interactive welcome walkthrough/tour_
  - _Review gamification => incentivize participation_
