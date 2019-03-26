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
    global unknowns
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
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (300, 300))
        rois.append(roi)
        unknowns += 1
    img = cv2.resize(img, (600, 600))
    return img, rois


def recognizePerson(grayFace):
    global unknowns
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
            unknowns -= 1
        # else:
        #     #unknowns +=1
        #     pass
    else:
        print("Unknown with Confident-> ",results[1])
        #unknowns += 1
        #return results[0], 0


def getStudentID(semesterID):
    cursor = db.cursor()
    sql = "SELECT std_id FROM student_semester WHERE semester_id = %s;"
    cursor.execute(sql, (semesterID,))
    result = cursor.fetchall()
    cursor.close()

    return result


def removeDuplicates():
    global recognized
    global unknowns
    length = len(recognized)
    tempArray = []
    seen = set()
    for value in recognized:
        if value not in seen:
            tempArray.append(value)
            seen.add(value)
    recognized = tempArray
    unknowns += length - len(tempArray)
    noFaceMsg = "{} unknown person detected".format(unknowns)
    detectedLabel.configure(text=noFaceMsg)


def takePicture(frame):
    #print("Before starting recognition", datetime.now())
    global rectImg
    #cv2.imwrite("img.jpg", frame)
    rectImg, faces = face_detector(frame)
    if faces == []:
        noFaceMsg = "Couldn't detect any faces"
        detectedLabel.configure(text=noFaceMsg)
        return

    for face in faces:
        #recognizedName, confidence = recognizePerson(face)
        recognizePerson(face)
        #cv2.waitKey(10)

    #print("After end of the recognition", datetime.now())
    #print("Recognized {} person(s)".format(len(recognized)))
    removeDuplicates()
    #print(recognized)

    if len(recognized) > 0:
        btnSave.configure(state=NORMAL)
    btnView.configure(state=NORMAL)
    noFaceMsg = "{} unknown person detected".format(unknowns)
    detectedLabel.configure(text=noFaceMsg)
    indicatorMsg = "{} person(s) recognized successfully!".format(len(recognized))
    indicatorLabel.configure(text=indicatorMsg)
    #showResult(rectImg)


def showResult():
    cv2.imshow("Detected Faces", rectImg)

def insertAttendance():
    #print("107: Length", len(recognized))
    if len(recognized) == 0:
        print("Empty")
        return
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
        #print("Error:", e)
        messagebox.showerror(title="Error", message="Error: {}".format(e))
        db.rollback()
    finally:
        cursor.close()
        messagebox.showinfo(title="Success", message="Successfully saved attendance information!")

def showLive():
    if selectedSemID == 0:
        messagebox.showerror(title="Invalid Input", message="Please select semester")
        return

    inputImage = cv2.imread("test4.jpg")
    #inputImage = cv2.imread("test.jpg")
    takePicture(inputImage)

def closeAll():
    try:
        if db.open == 1:
            db.close()
    except Exception as e:
        print("ErrorDB:",e)
    try:
        cv2.destroyAllWindows()
    except Exception as e:
        print("ErrorCV2:",e)
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

    #Get classifier to detect faces
    face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')

    #LBPH Face recognizer
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("trained_model.yml")

    #Eigen face recognizer
    # model = cv2.face.EigenFaceRecognizer_create()
    # model.read("trained_data1_eigen.yml")

    #Fisher face recognizer
    # model = cv2.face.FisherFaceRecognizer_create()
    # model.read("trained_data1_fisher.yml")

    #cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

    noFaceMsg = "Select Semester"
    indicatorMsg = ""
    recognized = []
    confidenceArray = []
    unknowns = 0
    selectedSemID = 0
    rectImg = []

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

    btnSnap = Button(root, text = "Take Attendance", font=("times new roman",18), width=30, command = showLive, fg="white",bg="#3E2723")
    btnSnap.grid(row = 3, column=0, padx=5, pady=5,sticky=E+W+N+S)
    btnView = Button(root, text = "View Detected Faces", font=("times new roman",18), command = showResult, state=DISABLED, fg="white",bg="#3E2723")
    btnView.grid(row = 4, column=0, padx=5, pady=5,sticky=E+W+N+S)
    btnSave = Button(root, text = "Save Attendance", font=("times new roman",18), command = insertAttendance, state=DISABLED, fg="white",bg="#3E2723")
    btnSave.grid(row = 5, column=0, padx=5, pady=5,sticky=E+W+N+S)
    #btnSnap.pack(anchor = CENTER, expand = True)
    # btnExit = Button(root, text = "EXIT", width = 50, command = closeAll, fg="white",bg="#3E2723")
    # btnExit.grid(row = 6, column=0, padx=5, pady=5)
    btnExit = Button(root,text="EXIT",font=("times new roman",18), fg="white",bg="#3E2723",command=closeAll)#root.quit
    btnExit.grid(row=7,column=0, pady=5,padx=5,sticky=E+W+N+S)
    detectedLabel = Label(root, text=noFaceMsg, font=("helvetica ",18), fg='#212121',bg="#D7CCC8")
    detectedLabel.grid(row=1, column = 0, padx=5, pady=5)

    indicatorLabel = Label(root, text=indicatorMsg, font=("helvetica ",18), fg='#212121',bg="#D7CCC8")
    indicatorLabel.grid(row=0, column = 0, padx=5, pady=5)

    semesterChoice = []
    #Label(root, text="Select Semester", font=("helvetica ",15), fg='#212121',bg="#D7CCC8").grid(row=2, column=0)
    spSemester = Combobox(root, values=semesterChoice, state='readonly', font=("helvetica ",15))
    semesterData = getSemesterData(spSemester)
    spSemester.grid(row=2,pady=5,padx=5, sticky=E+W+N+S)
    spSemester.bind('<<ComboboxSelected>>', changeSemester)

    root.mainloop()