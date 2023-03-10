import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=False,
                default='src_room.jpg',
                help = 'path to input image')
ap.add_argument('-c', '--config', required=False,
                default='yolov3-tiny.cfg',
                help = 'path to yolo config file')
ap.add_argument('-w', '--weights', required=False,
                default='yolov3-tiny.weights',
                help = 'path to yolo pre-trained weights')
args = ap.parse_args()


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

# Load Yolo
net = cv2.dnn.readNet(args.weights, args.config)
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
#layer_names = net.getLayerNames()
#output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
output_layers = get_output_layers(net)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
img = cv2.imread(args.input)
img = cv2.resize(img, None, fx=0.8, fy=0.7)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Showing informations on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
print(indexes)
font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 2)


#cv2.imshow("Image", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()