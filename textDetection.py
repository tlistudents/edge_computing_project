import cv2
import pytesseract
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=False,
                default='usa-street.mp4',
                help = 'path to input image')
ap.add_argument('-c', '--config', required=False,
                default='yolov3-tiny.cfg',
                help = 'path to yolo config file')
ap.add_argument('-w', '--weights', required=False,
                default='yolov3-tiny.weights',
                help = 'path to yolo pre-trained weights')
args = ap.parse_args()

cap = cv2.VideoCapture(args.input)
frame_id = 0
config = ('-l eng --oem 1 --psm 3')
while True:
    try:
        _, frame = cap.read()
        frame_id += 1
        #height, width, channels = frame.shape
    except:
        # Loading image again
        cap = cv2.VideoCapture(args.input)
        font = cv2.FONT_HERSHEY_PLAIN
        starting_time = time.time()
        frame_id = 0
        _, frame = cap.read()
        frame_id += 1
        #height, width, channels = frame.shape

    try:
        text = pytesseract.image_to_string(frame, config=config)
        # print text
        text = text.split('n')
    except:
        continue

cap.release()

