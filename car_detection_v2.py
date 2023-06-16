import cv2
import numpy as np
import depthai as dai
from pyvesc import VESC
import time
import sys
import math

#initially, we were going to park the car with this file
#that's the park.py file now
#this demonstrates hough lines and template matching with GUI now
#comments represent our workflow & debugging
#Team 14, Spring 2023

vesc = VESC("/dev/ttyACM0") # change to correct port

#this doesn't work with OAK-D; need a pipeline instead
#but, it works with a regular webcam, like our USB camera
# cap = cv2.VideoCapture(0)
# assert cap.isOpened()

# template = cv2.imread("/home/jetson/projects/depthai-python/jetson_final/car6.png", 0)
template = cv2.imread("/home/jetson/projects/depthai-python/jetson_final/handicap3.png", 0)
height, width = template.shape[::]


# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
# THE_4_K resolution is too high; much slower to process image
camRgb.setVideoSize(1920, 1080)
# camRgb.setVideoSize(3840, 2160)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

# Linking
camRgb.video.link(xoutVideo.input)

# flag for car/sign detected
car_detected = False
count = 0

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

    while True:
        videoIn = video.get()
        frame = videoIn.getCvFrame()
        src = frame.copy()
        #src is a copy, for hough_lines calcuation


        dst = cv2.Canny(src, 50, 200, None, 3)

        # Copy edges to the images that will display the results in BGR
        cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
        # cdstP = np.copy(cdst)
        # kernel = np.ones((5, 5), np.uint8)
        # edges_dilated = cv2.dilate(dst, kernel)
        # prin
        lines = cv2.HoughLines(dst, 1, np.pi / 180, 200, None, 0, 0)

        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

        # Get BGR frame from NV12 encoded video frame to show with opencv
        # Visualizing the frame on slower hosts might have overhead
        # cv2.imshow("video", videoIn.getCvFrame())

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(gray_frame, template, cv2.TM_SQDIFF)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = min_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)
        cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
        #demonstrates template matching!

        if max_val > 0.9999:
            # vesc.set_duty_cycle(0.035)
            # vesc.set_servo(0.5) #initially, to go forward

            if not car_detected:
                car_detected = True
                # vesc.set_duty_cycle(0.035)
                print("NOT DETECTED")

                # t_end = time.time() + 15 #t end is 15 seconds after current time
                # while time.time() < t_end:
                #     print("TURNING")
                #
                #     vesc.set_servo(0.95) #modify this; maybe theta2?
                #
                # t_end = time.time() + 15 #t end is 15 seconds after current time
                # while time.time() < t_end:
                #     print("STOPPED")
                #
                #     # maybe have this in here to constantly change the angle?
                #     # only if necessary
                #
                #     if lines is not None:
                #         for i in range(0, len(lines)):
                #             rho = lines[i][0][0]
                #             theta = lines[i][0][1] #angle of lines
                #             a = math.cos(theta)
                #             b = math.sin(theta)
                #             x0 = a * rho
                #             y0 = b * rho
                #             pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                #             pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                #             cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
                #
                #     theta1 = lines[0][0]1
                #     vesc.set_servo(theta1) #modify this
        #         t_end = time.time() + 8 #t end is 15 seconds after current time
        #         while time.time() < t_end:
        #             print("STRAIGHGt")

        #             # vesc.set_duty_cycle(0.035)


        #         vesc.set_duty_cycle(0)


            else:
                print("keep detecting car")

        #     #     #maybe put this in the above if statement, so this else
        #     #     #never gets activated

        #     #     vesc.set_duty_cycle(0)


        else:
            if car_detected:
                car_detected = False
                vesc.set_duty_cycle(0.0)
                print("DETECTED")
            else:
                print("DETECT MAX")



        cv2.imshow("Source", frame) #template matching!
        cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
        #^hough lines displayed in red!
        #two separate windows


        # cv2.imshow("Matched image", frame)
        # plt.figure(figsize = (20,10))
        # plt.imshow(frame)

        if cv2.waitKey(1) == ord('q'):
            break

#------------------------------------------------
# below was some code that was used for reference
# and not removed before the file was cleaned up
#------------------------------------------------
