import cv2
import numpy as np
import dlib
from imutils import face_utils
import time
import RPi.GPIO as GPIO

# GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

LCD_RS = 7
LCD_E  = 11
LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 15
LCD_D7 = 16
buzzer_pin = 36
LED_PIN = 29

GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(0.5)

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    lcd_toggle_enable()
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(0.0005)
    GPIO.output(LCD_E, True)
    time.sleep(0.0005)
    GPIO.output(LCD_E, False)
    time.sleep(0.0005)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

# Camera Initialization
cap = cv2.VideoCapture(0)
hog_face_detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Status tracking
sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)

def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)
    return 2 if ratio > 0.25 else (1 if 0.21 <= ratio <= 0.25 else 0)

lcd_init()
lcd_string("Welcome", LCD_LINE_1)
time.sleep(2)
lcd_string("Drowsiness", LCD_LINE_1)
lcd_string("Detection System", LCD_LINE_2)
time.sleep(2)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = hog_face_detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)
            left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            if left_blink == 0 or right_blink == 0:
                sleep += 1
                drowsy = active = 0
                if sleep > 1:
                    status = "SLEEPING!"
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    lcd_string("Wake Up!", LCD_LINE_1)
                    time.sleep(0.5)
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    GPIO.output(LED_PIN, GPIO.LOW)

            elif left_blink == 1 or right_blink == 1:
                sleep = active = 0
                drowsy += 1
                if drowsy > 1:
                    status = "Drowsy"
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    lcd_string("Wake Up!", LCD_LINE_1)
                    time.sleep(0.5)
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    GPIO.output(LED_PIN, GPIO.LOW)

            else:
                drowsy = sleep = 0
                active += 1
                if active > 1:
                    status = "Active"
                    lcd_string("All OK", LCD_LINE_1)
                    lcd_string("Drive Safe", LCD_LINE_2)
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    GPIO.output(LED_PIN, GPIO.LOW)

            cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
