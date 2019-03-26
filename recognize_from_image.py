import cv2
import sys
from os import listdir

#Get classifier to detect faces
face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')

#Get image names
data_path = 'D:/Image Processing Tutorial/Practices/amsrf/face_database/'

#LBPH Face recognizer
model = cv2.face.LBPHFaceRecognizer_create()
model.read("trained_data.yml")

#Eigen face recognizer
# model = cv2.face.EigenFaceRecognizer_create()
# model.read("trained_data_eigen.yml")

noFaceMsg = ""

def face_detector(img):
    global noFaceMsg
    # Convert image to grayscale
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = img
    faces = face_classifier.detectMultiScale(
        gray,
        scaleFactor=1.9,
        minNeighbors=8,
        minSize=(30, 30)
    )

    if faces is ():
        #print("Couldn't detect any faces")
        noFaceMsg = "Couldn't detect any faces"
        return img, []
    rois = []
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (300, 300))
        rois.append(roi)
    img = cv2.resize(img, (600, 600))
    return img, rois

def getNames(folder_path):
    seen = set()
    for files in listdir(folder_path):
        temp = files.split("_")
        if temp[0] not in seen:
            Labels.append(temp[2].split(".")[0])
            IDs.append(temp[0])
            seen.add(temp[0])

def removeDuplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def recognizePerson(grayFace):
    # Pass face to prediction model
    # "results" comprises of a tuple containing the label and the confidence value
    results = model.predict(grayFace)

    #print("line68")
    #print(""+str(results[1]))
    #print("line70")
    #print("{}, {}".format(results[0], results[1]))
    if results[1] < 500:
        confidence = int( 100 * (1 - (results[1])/500) )
        #print("cf = ".format(confidence))
        #print(format(results[0])+"test")
        #print("line76")
        recognizedName = ""
        for i, ids in enumerate(IDs):
            #print(str(results[0])+", "+ids)
            if int(results[0]) == int(ids):
                recognizedName = Labels[i]
                #print(recognizedName)
                break
            else:
                recognizedName = "Unknown"
        #print("line86")
        #print("{}, {}".format(results[0], results[1]))
        return recognizedName, confidence
    else:
        return "False positive",0

def showResult(label, confidence, face, increment):
    display_string = format(confidence) + '% Confident'
    message = "Recognized {0}".format(label)
    errorMessage = "Unknown person detected"
    cv2.putText(face, display_string, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,120,150), 1)
    #print("Line125")
    if confidence > 85:
        #print("Line127")
        recognized.append(label)
        cv2.putText(face, message, (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,120,150), 1)
        #print("Line129")
        cv2.imshow('Face Recognition'+str(increment), face )
    else:
        cv2.putText(face, errorMessage, (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,120,150), 1)
        cv2.imshow('Face Recognition'+str(increment), face )

if __name__ == '__main__':

    Labels = []
    IDs = []
    recognized = []


    #getNames(data_path)
    # Labels = removeDuplicates(Labels)
    # IDs = removeDuplicates(IDs)
    # print(Labels)
    # print(IDs)

    inputImage = cv2.imread("test_image2.jpg", cv2.IMREAD_GRAYSCALE)

    image, faces = face_detector(inputImage)

    if faces == []:
        cv2.putText(image, noFaceMsg, (100, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        cv2.imshow('Face Recognition', image )
        
    else:
        print("Length {}".format(len(faces)))
        #recognizedName, confidence = recognizePerson(faces[0])
        increment = 0
        for face in faces:
            # display_string = ""
            # confidence = 0.0
            # recognizedName = ""
            increment += 1
            recognizedName, confidence = recognizePerson(face)
            if confidence == 0:
                print(recognizedName)
            else:
                showResult(recognizedName, confidence, face, increment)
            #print("line122")
            # display_string = format(confidence) + '% Confident'
            # cv2.putText(face, display_string, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)
            # #print("Line125")
            # if confidence > 85:
            #     #print("Line127")
            #     cv2.putText(face, "Recognized {0}".format(recognizedName), (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            #     #print("Line129")
            #     cv2.imshow('Face Recognition'+str(increment), face )
            # else:
            #     cv2.putText(face, "Unknown person detected", (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            #     cv2.imshow('Face Recognition'+str(increment), face )
    cv2.waitKey(1000)
    cv2.destroyAllWindows()