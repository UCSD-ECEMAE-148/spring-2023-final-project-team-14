import cv2
import numpy as np
import depthai as dai
from pyvesc import VESC
import time
import sys
import math

# this is the file that actually parks the car
#Team 14, Spring 2023

vesc = VESC("/dev/ttyACM0") # change to correct port

#the handicap sign template
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

# flag for car detected
sign_detected = False

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)



    while True:
        videoIn = video.get()
        frame = videoIn.getCvFrame()
        src = frame.copy() #for hough_lines calcuation

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(gray_frame, template, cv2.TM_SQDIFF)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = min_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)

        #A DEVTOOL. comment this out on final project, because it takes away resources
        #but it displays a rectangle over image of the template match
        # cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)

        if max_val > 0.9999:
            if sign_detected == False:
                sign_detected = True
                # vesc.set_duty_cycle(0.035)#move forward


                #super advanced debug statement
                # print("DETECTED NOW")

                dst = cv2.Canny(src, 50, 200, None, 3)

                # Copy edges to the images that will display the results in BGR
                cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
                # cdstP = np.copy(cdst)
                # ^Probabilistic hough lines doesnt work

                # lines = cv2.HoughLinesP(dst, 1, np.pi / 180, 600, None, 0, 0)
                lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)


                if lines is not None:
                    for i in range(0, len(lines)):
                        rho = lines[i][0][0]
                        theta = lines[i][0][1] #angle of lines
                        a = math.cos(theta)
                        b = math.sin(theta)
                        x0 = a * rho
                        y0 = b * rho
                        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                        cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

                theta1 = lines[0][0][1]
                for i in range(0, len(lines)):
                        theta = lines[i][0][1] #angle of lines

                        #THETA IS GIVEN IN RADIANS
                        # print("----\nTHETA i="+str(i)+ "is: " + str(theta) + "\n --------")

                        if(theta < 2.8 and theta >1.7):
                            theta1 = theta
                            # print("IT CHANGED")


                #convert theta to degrees
                theta1 = (theta1*180)/np.pi
                theta1 = 180 - theta1 #account for heading of robot = 180 degrees
                #because the camera is facing sideways

                #convert degree angle to servo_angle for set servo
                #0 to 90 degrees convert to 0.5 to 1
                servo_angle = ((90 * 0.5) / 90) + 0.5
                vesc.set_servo(servo_angle)

                t_end = time.time() + 15 #t end is 15 seconds after current time
                    while time.time() < t_end:
                        #     print("TURNING")
                        vesc.set_duty_cycle(0.035)


                t_end = time.time() + 8 #t end is 15 seconds after current time
                    while time.time() < t_end:
                    # print("STRAIGHT")
                    vesc.set_servo(0.5) #straighten out to finish parking
                    vesc.set_duty_cycle(0.035)


                vesc.set_duty_cycle(0)
                break



            else:
                #shouldn't happen; should work in if statement and kick out of loop by this point
                #sign detected is already true, and has been matched




        else:
            if sign_detected:
                sign_detected = False
                vesc.set_duty_cycle(0)
                        #     print("INITIAL MOVEMENT")
                vesc.set_servo(0.5) #start off moving STRAIGHGt
                vesc.set_duty_cycle(0.035)

                # print("UN DETECTED")


            else:
                vesc.set_duty_cycle(0)
                # print("Still UNDETECT")



        # cv2.imshow("Matched image", frame)
        # plt.figure(figsize = (20,10))
        # plt.imshow(frame)

        if cv2.waitKey(1) == ord('q'):
            break
