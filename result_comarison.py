import cv2
import sys
from os import listdir


def face_detector(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(30, 30)
    )

    if faces is ():
        #noFaceMsg = "Couldn't detect any faces"
        return img, []
    rois = []
    count = 0
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (300, 300))
        rois.append(roi)
        count += 1
        #print(count)
        cv2.imshow("img"+str(count), roi)
    img = cv2.resize(img, (600, 600))
    return img, rois


def recognizePerson(grayFace):
    global unknowns
    # Pass face to prediction model
    # "results" comprises of a tuple containing the label and the confidence value
    results = model.predict(grayFace)
    print("Label->{}, Confidence->{}".format(results[0], results[1]))
    if results[1] < 50:
        confidence = int( 100 * (1 - (results[1])/500))
        #results[0], confidence
        if confidence > 85:
            recognized.append(results[0])
            confidenceArray.append(confidence)
        else:
            unknowns +=1
    else:
        print("50: Label, Confident-> ",results[0], results[1])
        unknowns += 1
        #return results[0], 0


def takePicture(frame):
    originalImg, faces = face_detector(frame)
    if faces == []:
        print("54: No face")
        return

    for face in faces:
        #recognizedName, confidence = recognizePerson(face)
        recognizePerson(face)
        #print("74: conf-> ", confidence)
        # if confidence == 0:
        #     print(recognizedName)
        #     unknowns += 1
        # else:
        #     recognized.append(recognizedName)
        #     confidenceArray.append(confidence)
    showResult()


def showResult():
    print("recognized", recognized)
    print("confidence", confidenceArray)
    print("unknowns", unknowns)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()


if __name__ == '__main__':

    #print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    #Get classifier to detect faces
    face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
    #face_classifier = cv2.CascadeClassifier('cascade/haarcascades/haarcascade_frontalface_alt2.xml')
    #face_classifier = cv2.CascadeClassifier('cascade/lbpcascades/lbpcascade_frontalface_improved.xml')

    #LBPH Face recognizer
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("trained_data1_lbph.yml")

    #Eigen face recognizer
    # model = cv2.face.EigenFaceRecognizer_create()
    # model.read("trained_data1_eigen.yml")

    #Fisher face recognizer
    # model = cv2.face.FisherFaceRecognizer_create()
    # model.read("trained_data1_fisher.yml")

    #cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    #cap = cv2.VideoCapture(0)

    recognized = []
    confidenceArray = []
    unknowns = 0

    inputImage = cv2.imread("test_image2.jpg")
    takePicture(inputImage)