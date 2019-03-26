import cv2
import sys
from os import listdir
import MySQLdb
from datetime import datetime
#from PIL import Image, ImageTk
import PIL.Image, PIL.ImageTk
from tkinter import *


def face_detector(img):
    #global noFaceMsg
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=8,
        minSize=(30, 30)
    )

    if faces is ():
        #print("Couldn't detect any faces")
        #noFaceMsg = "Couldn't detect any faces"
        return img, []
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (300, 300))

    return img, roi


def recognizePerson(grayFace):
    # Pass face to prediction model
    # "results" comprises of a tuple containing the label and the confidence value
    results = model.predict(grayFace)

    #print("{}, {}".format(results[0], results[1]))
    if results[1] < 500:
        confidence = int( 100 * (1 - (results[1])/500) )
        results[0], confidence
    else:
        return results[0],results[1] 


def getStudentID(semesterID):
    cursor = db.cursor()
    sql = "SELECT std_id FROM student_semester WHERE semester_id = %s;"
    cursor.execute(sql, (semesterID,))
    result = cursor.fetchall()
    cursor.close()

    return result


def takePicture():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("img.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

def update():
    global count
    ret, frame = cap.read()
    if ret:
        #print("Captured")
        imgtk = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        #canvas.create_image(50, 10, image = imgtk, anchor = NW)
        #cv2.imshow('Video', frame )
        frameContainer.imgtk = imgtk
        frameContainer.configure(image = imgtk)
        image, face = face_detector(frame)

        if face == []:
            count = "detected faces: 0"
            #continue
        else:
            count = "detected faces: {}".format(len(face))
            recognizePerson(face)
            # recognizedName, confidence = recognizePerson(face)
            # if confidence > 85:
            #     count += ", Recognized: "+recognizedName
            # else:
            #     count += ", Confident: "+recognizedName
    detectedLabel.configure(text=count)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Clicked")
        cap.release()
        cv2.destroyAllWindows()
        root.destroy()
        return
    root.after(delay, update)

if __name__ == '__main__':


    #print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    #Get classifier to detect faces
    face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')

    #LBPH Face recognizer
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("trained_data.yml")
    noFaceMsg = ""

    host = "localhost"
    user = "root"
    password = ""
    database = "amsrf"
    db = MySQLdb.connect(host, user, password, database)

    root = Tk()
    root.title("Student Details")
    root.configure(bg="#D7CCC8")
    root.focus_set()

    # canvas = Canvas(width = 600, height = 600, bg='black')
    # canvas.pack(expand = YES, fill=BOTH)
    frameContainer = Label(root)
    frameContainer.grid(row = 0, column = 0)

    btnSnap = Button(root, text = "Capture", width = 50, command = takePicture)
    btnSnap.grid(row = 1)
    #btnSnap.pack(anchor = CENTER, expand = True)
    count = "detected faces: "
    detectedLabel = Label(root, text=count, font=("helvetica ",20), fg='#212121',bg="#D7CCC8")
    detectedLabel.grid(row=2)

    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

    delay = 50
    update()

    root.mainloop()


    # Labels = []
    # #IDs = []


    # IDs = getStudentID(9)
    # #getNames(data_path)
    # # Labels = removeDuplicates(Labels)
    # # IDs = removeDuplicates(IDs)
    # # print(Labels)
    # # print(IDs)

    # # Open Webcam
    # cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

    # while True:

    #     ret, frame = cap.read()

    #     if not ret:
    #         continue
        
    #     image, face = face_detector(frame)

    #     if face == []:
    #         cv2.putText(image, noFaceMsg, (100, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    #         cv2.imshow('Face Recognition', image )
    #         #continue
    #     else:
    #         try:
                
    #             recognizedName, confidence = recognizePerson(face)
    #             #print("line122")
    #             display_string = format(confidence) + '% Confident'
    #             cv2.putText(image, display_string, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)
    #             #print("Line125")
    #             if confidence > 85:
    #                 #print("Line127")
    #                 cv2.putText(image, "Recognized {0}".format(recognizedName), (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    #                 #print("Line129")
    #                 cv2.imshow('Face Recognition', image )
    #             else:
    #                 cv2.putText(image, "Unknown person detected", (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    #                 cv2.imshow('Face Recognition', image )

    #         except:
    #             #cv2.putText(image, "No Face Found", (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    #             #cv2.putText(image, "Couldn't Recognize", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    #             #cv2.imshow('Face Recognition', image )
    #             print("Unexpected error: ", sys.exc_info()[0])
    #             #raise
    #             break
            
    #     if cv2.waitKey(1) == 13: #13 is the Enter Key
    #         break
            
    # cap.release()
    # cv2.destroyAllWindows()