import cv2
import sys
from os import listdir
import MySQLdb
from datetime import datetime
#from PIL import Image, ImageTk
import PIL.Image, PIL.ImageTk
from tkinter import *


def face_detector(img):
    global noFaceMsg
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if faces is ():
        noFaceMsg = "Couldn't detect any faces"
        return img, []
    rois = []
    count = 0
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (300, 300))
        rois.append(roi)
        count += 1
    noFaceMsg = "Detected faces: {}".format(count)
    img = cv2.resize(img, (600, 600))
    return img, rois


def recognizePerson(grayFace):
    # Pass face to prediction model
    # "results" comprises of a tuple containing the label and the confidence value
    results = model.predict(grayFace)

    print("{}, {}".format(results[0], results[1]))
    if results[1] < 50:
        confidence = int( 100 * (1 - (results[1])/500) )
        results[0], confidence
    else:
        return results[0], 0


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
        cv2.imwrite("img.jpg", frame)
        originalImg, faces = face_detector(frame)

def update():
    global noFaceMsg
    ret, frame = cap.read()
    if ret:
        #print("Captured")
        imgtk = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        #canvas.create_image(50, 10, image = imgtk, anchor = NW)
        #cv2.imshow('Video', frame )
        frameContainer.imgtk = imgtk
        frameContainer.configure(image = imgtk)
        image, faces = face_detector(frame)

        if face == []:
            noFaceMsg = "Detected faces: 0"

        for face in faces:
            recognizedName, confidence = recognizePerson(face)
            if confidence == 0:
                print(recognizedName)
            else:
                showResult(recognizedName, confidence, face)

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
    noFaceMsg = "Detected faces: 0"

    # host = "localhost"
    # user = "root"
    # password = ""
    # database = "amsrf"
    # db = MySQLdb.connect(host, user, password, database)

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
    detectedLabel = Label(root, text=noFaceMsg, font=("helvetica ",20), fg='#212121',bg="#D7CCC8")
    detectedLabel.grid(row=2)

    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

    root.mainloop()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Couldn't capture any frame")
            break
        #print("Captured")
        image, faces = face_detector(frame)

        if face == []:
            noFaceMsg = "Detected faces: 0"
            continue

        imgtk = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        #canvas.create_image(50, 10, image = imgtk, anchor = NW)
        #cv2.imshow('Video', frame )
        frameContainer.imgtk = imgtk
        frameContainer.configure(image = imgtk)
        for face in faces:
            recognizedName, confidence = recognizePerson(face)
            if confidence == 0:
                print(recognizedName)
            else:
                showResult(recognizedName, confidence, face)

        else:
            noFaceMsg = "detected faces: {}".format(len(face))
            #recognizePerson(face)
            recognizedName, confidence = recognizePerson(face)
            if confidence > 85:
                noFaceMsg = "Recognized: "+recognizedName
            else:
                noFaceMsg = "Confident: "+confidence
        detectedLabel.configure(text=noFaceMsg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Clicked")
            # cap.release()
            # cv2.destroyAllWindows()
            root.destroy()
            break

    cap.release()
    cv2.destroyAllWindows()