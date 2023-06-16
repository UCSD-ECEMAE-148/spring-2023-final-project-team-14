[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/M2_fO6fJ)

# Final Report: Team 14, ECE/MAE 148, Spring 2023

## The Team: Self-Parking Car (Rocky McQueen)

<img width="639" alt="image" src="https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-14/assets/20979077/9c9aeb30-52e7-4e99-9f56-ff2aadb0dcfd">


- Manoel Aguirre Lara (ME)
- Allison Moya (ECE)
- Rohan Sreedhar (ECE:CE)


## Final Project Overview

The car will park itself in a free handicap parking spot with lane detection and LIDAR

It will use cameras, not other sensors (Adafruit TOF sensor) that previous teams have used.

### Demo Video!
https://youtube.com/shorts/hF-dNfn05qA?feature=share

### What We Promised


#### Must Have

- Car will park itself in a free parking spot, using image recognition
- Uses cameras, not Adafruit TOF sensor like previous projects

#### Nice to Have (Stretch Goals):

- Parallel Parking
- Lidar integration

### What Was Delivered

- Car moves forward, through the parking lot
- If it sees a handicap sign, it decides to park in that parking space
- It turns, throttles, then straightens out, throttles again, and stops

- Accomplished using Hough Lines, Template Matching, and PyVesc

## Our Robot


### Images


#### Front

<img width="187" alt="image" src="https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-14/assets/20979077/ec0e9d3f-6783-446c-a0e0-2db0734580a4">

#### Side

<img width="296" alt="image" src="https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-14/assets/20979077/32cec242-eb7c-4d90-a908-c374f82b98e2">


#### Bird's Eye

<img width="207" alt="image" src="https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-14/assets/20979077/c156e517-e69a-4517-8d1a-846bcc21be54">


### Schematic

<img width="552" alt="image" src="https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-14/assets/20979077/c7afd0c6-ca3d-4ff5-b0c7-85958b561f81">


### Software and Hardware List

- Hardware
  - Jetson Nano
  - 64GB MicroSD Card
  - OAKD Camera
  - USB Camera
  - HDMI Adapter
  - WiFi Adapter
  - VESC
  - DC-DC Converter
  - 4V Battery
  - Servo Motor
  - BLDC
  - Car Chassis


### Source Code
- Linked in this repository, at the root.

- park.py is the actual code used to park the car
  - It constantly is template matching, for the handicap sign
  - If the template is matched, it starts hough_lines detection
  - Calculating the angle using hough_lines, it sets the servo angle
  - Throttles at the angle, then straightens out and throttles longer to pull into the parking space
    
- car_detection.py demonstrates the technologies we are using: HoughLines, Template Matching, and PyVESC
  - It pulls a frame, using .cvFrame(), from the pipelined live feed of the OAK-D
  - It will generate a live image, with a blue rectangle around a template match
    <img width="506" alt="image" src="https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-14/assets/20979077/f4be20a2-abbd-4792-aa25-2397b8fe4eb0">

  - It will generate another live image, a black and white version generated using cv.canny() and focusing on edges
    <img width="432" alt="image" src="https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-14/assets/20979077/551d2ef2-5774-4813-bad6-92bbd271716e">

  - On this second image, red lines representing the detecting hough lines are present

### Gantt Chart

<img width="1237" alt="image" src="https://github.com/UCSD-ECEMAE-148/spring-2023-final-project-team-14/assets/20979077/0bfe83cc-6a4c-4122-a594-7877743cddfb">


### Presentation
- Linked in this repository, at the root, in pdf form.

## For the Future
- If you have a similar project, we recommend YOLO over template matching! Template matching was slow and had many false positives on images pulled from the OAKD live feed



## Earlier in the Quarter: Autonomous Laps

- DonkeyCar, OpenCV, and GPS (YouTube Playlist): https://youtube.com/playlist?list=PLk6ssglDhUEqm6P5aKJ0jK8jdhAzEwMPw



## Acknowledgements
- Huge shoutout to our TAs Kishore Nukala and Moises Lopez! We also want to thank the professor, Dr. Jack Silberman
- We also want to give credit to our former teammate, Shravan Suresh, for his contributions to our team
