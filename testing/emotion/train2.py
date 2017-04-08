import cv2
import glob
import numpy as np

#EMOTIONS = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Emotion list
#EMOTIONS = ["neutral", "anger", "happy", "surprise", "sadness"]
EMOTIONS = ["neutral", "happy"]
#EMOTIONS = ["neutral", "happy", "surprise"]
MODEL_FILE = "model.mdl"

FACEDETECT = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
FACEDETECT2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
FACEDETECT3 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
FACEDETECT4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")
FACEDETECT5 = cv2.CascadeClassifier("haarcascade_profileface.xml")


data = {}

def load_images():
    training_data = []
    training_labels = []
    for emotion in EMOTIONS:
        training = glob.glob("webcam/%s/*" %emotion)
        #Append data to training and prediction list, and generate labels 0-7
        for item in training:
            image = cv2.imread(item) #open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
            training_data.append(gray) #append image array to training data list
            training_labels.append(EMOTIONS.index(emotion))

    return training_data, np.asarray(training_labels)

def train():
    images, labels = load_images()
    model = cv2.createFisherFaceRecognizer()
    model.train(images,labels)
    model.save(MODEL_FILE)


def to_grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #gray = cv2.equalizeHist(gray)
    return gray
"""
def detect(img, cascade):
    gray = to_grayscale(img)
    rects = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)

    if len(rects) == 0:
        return []
    return rects
"""
def detect_faces(img):
    face = FACEDETECT.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(face) > 0:
        return face

    face2 = FACEDETECT2.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(face2) > 0:
        return face2

    face3 = FACEDETECT3.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(face3) > 0:
        return face3

    face4 = FACEDETECT4.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(face4) > 0:
        return face4

    face5 = FACEDETECT5.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(face5) > 0:
        return face5

    return []

def crop_faces(img, faces):
    for face in faces:
        x, y, h, w = [result for result in face]
        return img[y:y+h,x:x+w]

def predict(cv_image, model):
    faces = detect_faces(cv_image)
    result = None
    if len(faces) > 0:
        print len(faces)
        cropped = to_grayscale(crop_faces(cv_image, faces))
        resized = cv2.resize(cropped, (350,350))

        prediction = model.predict(resized)

        result = {
            'face': {
                'name': EMOTIONS[prediction[0]],
                'id': prediction[0],
                'distance': prediction[1],
                'coords': {
                    'x': str(faces[0][0]),
                    'y': str(faces[0][1]),
                    'width': str(faces[0][2]),
                    'height': str(faces[0][3])
                }
            }
        }
    return result

#train()
#exit()

camera = cv2.VideoCapture(0)
ret = camera.set(3, 640)
ret = camera.set(4, 480)

model = cv2.createFisherFaceRecognizer()
model.load(MODEL_FILE)

while True:
    ret, image = camera.read()

    prediction = predict(image, model)

    if (prediction != None):
        coords = prediction['face']['coords']
        textStr = "{} - {}".format(prediction['face']['name'], prediction['face']['distance'])
        print textStr
        cv2.rectangle(image, (int(coords['x']), int(coords['y'])), (int(coords['x']) + int(coords['width']), int(coords['y']) + int(coords['height'])), (0, 0, 255), 1)
        cv2.putText(image, textStr, (int(coords['x']) - 10, int(coords['y']) - 10), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 255), 1)

    cv2.imshow("image", image)



