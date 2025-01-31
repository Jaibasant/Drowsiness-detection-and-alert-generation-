
### Dependencies

1) import cv2
2) import imutils
3) import dlib
4) import cv2
5) import numpy 
6) import RPi.GPIO as GPIO



# Description 

A computer vision system that can automatically detect driver drowsiness in a real-time video stream and then play an alarm if the driver appears to be drowsy.

### Algorithm 

Each eye is represented by 6 (x, y)-coordinates, starting at the left-corner of the eye (as if you were looking at the person), and then working clockwise around the eye.

It checks 20 consecutive frames and if the Eye Aspect ratio is less than 0.25, Alert is generated.

