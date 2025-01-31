
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

This image shows the GPIO (General Purpose Input/Output) pin configuration of the Raspberry Pi Zero.
It highlights crucial connections for peripherals like the camera, HDMI, USB ports, and power.
The GPIO pins are essential for interfacing with sensors, including those needed for drowsiness detection, such as an infrared camera or an eye-tracking module.

![Image](https://github.com/user-attachments/assets/80ee09e6-5551-4ee7-b1b8-0d2ae795270b)

This circuit diagram demonstrates how a Raspberry Pi 2 can be connected to various components like a camera module, LCD display, buzzer, and LED using a breadboard.
The camera module is crucial for detecting eye movement and signs of drowsiness.
The buzzer and LED can serve as alert mechanisms when drowsiness is detected.
The LCD display can show system status or warning messages.

![Image](https://github.com/user-attachments/assets/2fbc782a-7400-47c0-9afe-13a3ac6dbb5a)

