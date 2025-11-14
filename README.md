[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2024_project

## Description

Context: Kerbal Space Program is a spaceflight simulator game about launching sentient (?) froglike
creatures into space, with semi-(semi-(semi-realistic)) physics.

A spacecraft's ability to get somewhere, and the cost of any maneuver, is measured in how much it can 
change its velocity, referred to as delta-v. For example, a ship may have 1500 m/s of delta-v left; after a
maneuver where it changes its velocity by 500 m/s, with the remaining fuel it will have 1000 m/s of delta-v left.
Going from Earth orbit to Lunar orbit, in the real world, takes about 4.3 km/s  of delta-v.

This application will calculate the amount of delta-v needed to travel a route between some planets (or moons)
in the Kerbolar system.

## Setup

```
# if you do not have the flask and request libraries:
pip install -r requirements.txt

# create the image and run the application within the container:
docker build -t server .
docker run -p 80:8080 -d server

# test that the server is running within the container:
python3 client.py

```

## Requirements

* Python 3.11 (or higher?...)
* Flask library
* Requests library
* Docker

## Features

* The user can select multiple locations (planets, moons) in the KSP solar system
* (Maybe the orbital altitudes at each waypoint could be entered too?)
* The application will calculate the amount of delta-v needed to make the maneuvers
to traverse this route
* The application prints the resulting number in a text field

## Git

The latest version of the application is stored in the main branch of the repository

## Success Criteria

* The application does not crash
* The application can take in and process user input in some form
* The application can display the info about the correct route (the one the user entered) 
* The information about maneuver costs that the application outputs should be at least close to being correct