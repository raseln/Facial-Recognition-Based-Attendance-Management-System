import cv2
#import sys
#from os import listdir
import MySQLdb
from datetime import datetime
#from PIL import Image, ImageTk
#import PIL.Image, PIL.ImageTk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
#from time import sleep


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
        return img, []
    rois = []
    count = 0
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (300, 300))
        rois.append(roi)
        count += 1
    indicatorMsg = "Detected faces: {}".format(count)
    img = cv2.resize(img, (600, 600))
    return img, rois


def recognizePerson(grayFace):
    # Pass face to prediction model
    # "results" comprises of a tuple containing the label and the confidence value
    results = model.predict(grayFace)
    #print("43: {}, {}".format(results[0], results[1]))
    if results[1] < 50:
        confidence = int( 100 * (1 - (results[1])/500) )
        #results[0], confidence
        if confidence > 85:
            recognized.append(results[0])
            confidenceArray.append(confidence)
        else:
            unknowns +=1
    else:
        print("54: Confident-> ",results[1])
        unknowns += 1
        #return results[0], 0


def getStudentID(semesterID):
    cursor = db.cursor()
    sql = "SELECT std_id FROM student_semester WHERE semester_id = %s;"
    cursor.execute(sql, (semesterID,))
    result = cursor.fetchall()
    cursor.close()

    return result


def takePicture(frame):
    cv2.imwrite("img.jpg", frame)
    originalImg, faces = face_detector(frame)
    if faces == []:
        indicatorMsg = "Couldn't detect any faces"
        indicatorLabel.configure(text=indicatorMsg)
        return

    for face in faces:
        recognizePerson(face)
    showResult()


def showResult():
    # print(recognized)
    # print(confidenceArray)
    #print("unknowns", unknowns)
    indicatorMsg = "{} person(s) recognized successfully!\n{} unknown person detected".format(len(recognized), unknowns)
    indicatorLabel.configure(text=indicatorMsg)
    if len(recognized) > 0:
        response = messagebox.askyesno("Save Attendance", "Do you want to save this attendance?")
        if response:
            insertAttendance(recognized)

def insertAttendance(recognized):
    dt = "datetime"
    dtVal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = db.cursor()
        sql = "INSERT INTO attendance (std_id, semester_id, {0}) VALUES(%s,%s,%s)".format(dt)
        for ids in recognized:
            val = (ids, 9, dtVal)
            cursor.execute(sql, val)
        db.commit()
        print(cursor.rowcount, "row was inserted.")
    except Exception as e:
        print("Error:", e)
        messagebox.showerror(title="Error", message="Error: {}".format(e))
        db.rollback()
    finally:
        cursor.close()
        messagebox.showinfo(title="Success", message="Successfully added attendance information!")

def showLive():
    if selectedSemID == 0:
        messagebox.showerror(title="Invalid Input", message="Please select semester")
        return
    option = 0#default is zero, save is 1, quit is 2
    img = []
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Couldn't capture any frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if faces is ():
            continue
        faceCount = 0
        imgCopy = frame.copy()
        for (x,y,w,h) in faces:
            cv2.rectangle(imgCopy,(x,y),(x+w,y+h),(0,255,0),2)
            faceCount += 1
            #imgCopy = imgCopy[y:y+h, x:x+w]
            #roi = cv2.resize(roi, (300, 300))
        cv2.putText(imgCopy, "Press S to capture, ESC to stop capturing", (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)
        cv2.imshow("Video", imgCopy)

        # imgtk = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(cv2.resize(frame, (300, 300)), cv2.COLOR_BGR2RGB)))
        # #canvas.create_image(50, 10, image = imgtk, anchor = NW)
        # #cv2.imshow('Video', frame )
        # frameContainer.imgtk = imgtk
        # frameContainer.configure(image = imgtk)
        
        key = cv2.waitKey(30)
        if key == 27:
            #print("ESC Clicked")
            option = 2
            indicatorMsg = "Press Capture to start"
            indicatorLabel.configure(text=indicatorMsg)
            break
        elif key == ord('s'):
            #print("Before 183")
            option = 1
            img = frame
            indicatorMsg = "{} face(s) detected".format(faceCount)
            indicatorLabel.configure(text=indicatorMsg)
            #print("After 189")
            break

    cap.release()
    cv2.destroyAllWindows()
    if option == 1:
        takePicture(img)

def update():
    #global noFaceMsg
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
            indicatorMsg = "Detected faces: 0"

        for face in faces:
            recognizedName, confidence = recognizePerson(face)
            if confidence == 0:
                print(recognizedName)
            else:
                showResult(recognizedName, confidence, face)

        else:
            #count = "detected faces: {}".format(len(face))
            recognizePerson(face)
    #detectedLabel.configure(text=count)
    indicatorMsg.configure(text=indicatorMsg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #print("Clicked")
        cap.release()
        cv2.destroyAllWindows()
        root.destroy()
        return
    root.after(delay, update)


def closeAll():
    try:
        if db.open == 1:
            db.close()
    except Exception as e:
        print("Error:",e)
    root.destroy()


def getSemesterData(spSemester):
    cursor = db.cursor()
    sql = "SELECT * FROM semester"
    cursor.execute(sql)
    semesterResult = cursor.fetchall()
    cursor.close()
    semesterChoice
    for val in semesterResult:
        semesterChoice.append(val[1])
    spSemester['values'] = semesterChoice

    return semesterResult

def changeSemester(*args):
    global selectedSemID
    selectedSemID = semesterData[spSemester.current()][0]


if __name__ == '__main__':

    #print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    #Get classifier to detect faces
    face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')

    #LBPH Face recognizer
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("trained_model.yml")
    #cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    #cap = cv2.VideoCapture(0)

    #noFaceMsg = "Select Semester"
    indicatorMsg = "Select Semester and \nthen press capture to start"
    recognized = []
    confidenceArray = []
    unknowns = 0
    selectedSemID = 0

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
    # frameContainer = Label(root, width=5, height=5)
    # frameContainer.grid(row = 0, column = 1)

    btnSnap = Button(root, text = "CAPTURE", font=("helvetica",18), width=30, command = showLive, fg="white",bg="#3E2723")
    btnSnap.grid(row = 3, column=0, padx=5, pady=5,sticky=E+W+N+S)
    btnExit = Button(root, text = "EXIT", width = 30, font=("helvetica ",18), command = closeAll,fg="white",bg="#3E2723")
    btnExit.grid(row = 4, column=0, padx=5, pady=5)
    # detectedLabel = Label(root, text=noFaceMsg, font=("helvetica ",18), fg='#212121',bg="#D7CCC8")
    # detectedLabel.grid(row=1, column = 0, padx=5)

    indicatorLabel = Label(root, text=indicatorMsg, font=("helvetica ",18), fg='#212121',bg="#D7CCC8")
    indicatorLabel.grid(row=0, column = 0, padx=5, pady=5)

    semesterChoice = []
    spSemester = Combobox(root, values=semesterChoice, state='readonly',font=("helvetica ",18))
    semesterData = getSemesterData(spSemester)
    spSemester.grid(row=2,pady=5,padx=5, sticky=E+W+N+S)
    spSemester.bind('<<ComboboxSelected>>', changeSemester)

    root.mainloop()