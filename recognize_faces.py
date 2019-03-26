import cv2
import sys
from os import listdir

#Get classifier to detect faces\
face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
#Get image names
data_path = 'D:/Image Processing Tutorial/Practices/amsrf/face_database/'

#LBPH Face recognizer
model = cv2.face.LBPHFaceRecognizer_create()
model.read("trained_model.yml")

#Eigen face recognizer
# model = cv2.face.EigenFaceRecognizer_create()
# model.read("trained_data_eigen.yml")

#Fisher face recognizer
# model = cv2.face.FisherFaceRecognizer_create()
# model.read("trained_data_fisher.yml")

noFaceMsg = ""

def face_detector(img):
    global noFaceMsg
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=8,
        minSize=(30, 30)
    )

    if faces is ():
        noFaceMsg = "Couldn't detect any faces"
        return img, []
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (300, 300))

    return img, roi

def getNames(folder_path):
    seen = set()
    for files in listdir(folder_path):
        temp = files.split("_")
        #print(temp)
        if temp[0] not in seen:
            #Labels.append(temp[1].split(".")[0])
            Labels.append(temp[0])

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
        return results[0], confidence
    else:
        return results[0],results[1] 


if __name__ == '__main__':

    Labels = []
    IDs = []


    getNames(data_path)
    # Labels = removeDuplicates(Labels)
    # IDs = removeDuplicates(IDs)
    # print(Labels)
    # print(IDs)

    # Open Webcam
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

    while True:

        ret, frame = cap.read()

        if not ret:
            continue
        
        image, face = face_detector(frame)

        if face == []:
            cv2.putText(image, noFaceMsg, (100, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            cv2.imshow('Face Recognition', image )
            #continue
        else:
            try:
                
                recognizedName, confidence = recognizePerson(face)
                #print("line122")
                display_string = format(confidence) + '% Confident'
                cv2.putText(image, display_string, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)
                #print("Line125")
                if confidence > 85:
                    #print("Line127")
                    cv2.putText(image, "Recognized {0}".format(recognizedName), (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                    #print("Line129")
                    cv2.imshow('Face Recognition', image )
                else:
                    cv2.putText(image, "Unknown person detected", (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                    cv2.imshow('Face Recognition', image )

            except:
                #cv2.putText(image, "No Face Found", (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                #cv2.putText(image, "Couldn't Recognize", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                #cv2.imshow('Face Recognition', image )
                print("Unexpected error: ", sys.exc_info()[0])
                #raise
                break
            
        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break
            
    cap.release()
    cv2.destroyAllWindows()