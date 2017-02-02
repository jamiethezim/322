assignment 3
app.py -> THIS CODE RUNS PYTHON FLASK WEBSERVER not the apache wsgi. this code runs the app that launches the login process, queries the database, outputs the results, and runs the logout process.

config.py -> parse the json config file to get the necessary configuration for the database specification

config.json -> holds the configurations for the database. I hard coded them with my own for testing use

templates/index.html -> welcome page, asks for username log in

templates/filter.html -> report specification filtering, asks for facility/date/etc

templates/facility.html -> displays inventory at specific facilities

templates/transit.html -> displays inventory currently in transit

templates/logout.html -> displays log out message, session data is cleared by this point
