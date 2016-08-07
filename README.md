# Cardinal Planner
This is the main code repository for the cardinal planner project.

## Central Goal
The **central goal** to create the best way (by far) for students to plan their long term and short term schedules.

## Specific Functionality Goals

- Course catalog
  - Great search, sorting, and filtering abilities
  - Helpful tags in search results
  - Useful short descriptions
  - Beautiful and fast
  - AJAX support
  - Comprehensive and up-to-date (crawls official site regularly)
  - Ability to star / save classes to list
- Course reviews / course page
  - Amazon-level review functionality (helpful/not helpful, verified student, replies, etc)
  - Sensible display of grade breakdown
  - Comments and comment replies, sorting and likes
  - Sensible display of class times and available quarters (parse the text)
  - Intelligent ‘related courses’ view
  - Ability to star / save classes to lists
- Login / users
  - Only necessary for saving classes / planner
  - Quick login with Facebook / SUNet (maybe Google) => popover like reddit
  - Allow Facebook login to find (invite?) & connect with friends
- Planner
  - Learns from other users to suggest classes => some AI involved here
  - Pulls from axess to fill in classes you’ve already taken => verifies
  - Specify major / minors / subjects you like
  - Displays your coverage of graduation requirements (general and for major/minor)
  - Trello-like dragging and dropping of classes (w/ AJAX)
  
## Conceptual Development Plan Outline
- August 7
  - Finish crawling for course & reviews data
  - Implement basic course search & info frontend
- August 14
  - Implement reviews & comments functionality
  - Add pages for instructors
- August 21
  - Fully implement user authentication with Stanford WebAuth
  - Add user settings & profile
  - Add aggregate course & instructor data
