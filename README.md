[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/M2_fO6fJ)

# Final Report: Team 14, ECE/MAE 148, Spring 2023

## The Team: Self-Parking Car (Rocky McQueen)



- Manoel Aguirre Lara (ME)
- Allison Moya (ECE)
- Rohan Sreedhar (ECE:CE)


## Final Project Overview

The car will park itself in a free handicap parking spot with lane detection and LIDAR

It will use cameras, not other sensors (Adafruit TOF sensor) that previous teams have used.


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


### Bird's Eye


### Front


### Side


### Bird's Eye


### Back


### Schematic


###Software and Hardware List

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
  - It will generate another live image, a black and white version generated using cv.canny() and focusing on edges
  - On this second image, red lines representing the detecting hough lines are present


## For the Future
- If you have a similar project, we recommend YOLO over template matching! Template matching was slow and had many false positives on images pulled from the OAKD live feed


### Gantt Chart

### Presentation
- Linked in this repository, at the root, in pdf form.


## Autonomous Laps

- DonkeyCar, OpenCV, and GPS: [youtube link]




## Acknowledgements
- Huge shoutout to our TAs Kishore Nukala and Moises Lopez! We also want to thank the professor, Dr. Jack Silberman!
