from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import MySQLdb
import collect_data as cd


root=Tk()
root.title("Student Details")
root.configure(bg="#D7CCC8")
root.focus_set()

host = "localhost"
user = "root"
password = ""
database = "amsrf"

db = MySQLdb.connect(host, user, password, database)

#img = cv2.imread("test_image2.jpg", cv2.IMREAD_GRAYSCALE)

def validateInput():
    if selectedSemID == 0:
        messagebox.showerror(title="Invalid Input", message="Please select semester")
        return
    if sessionID == 0:
        messagebox.showerror(title="Invalid Input", message="Please select session")
        return
    #stdId = std_id_entry.get()
    stdName = name_entry.get()
    if len(stdName) == 0:
        messagebox.showerror(title="Invalid Input", message="Please enter student name")
        return
    stdPhone = std_phone_entry.get()
    email = std_email_entry.get()
    #getInput()
    #saveStudent(stdId, stdName, sessionID, selectedSemID, stdPhone, email)
    insertStudent(stdName, sessionID, selectedSemID, stdPhone, email)

def isNumber(stdId):
    try:
        float(stdId)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(stdId)
        return True
    except (TypeError, ValueError):
        print("Error parsing data.")
 
    return False

def checkIfUserExist(stdId):
    cursor = db.cursor()
    #sql = "SELECT * FROM student WHERE std_id = "+stdId+";"
    sql = "SELECT * FROM student WHERE std_id = %s;"
    val = (stdId,)
    cursor.execute(sql, val)
    sessionResult = cursor.fetchall()
    cursor.close()
    if len(sessionResult) > 0:
        return True
    else:
        return False

def getInput():
    global stdId
    stdId = std_id_entry.get()
    if len(stdId) == 0:
        messagebox.showerror(title="Invalid Input", message="Please enter student ID")
        return
    if not isNumber(stdId):
        messagebox.showerror(title="Invalid ID", message="Invalid student ID. Please enter valid (numeric) ID")
        return
    exist = checkIfUserExist(stdId)
    if exist:
        msgText = "ID "+stdId+" already exist in database. Try another one."
        messagebox.showerror(title="Student exist", message=msgText)
        return

    if captureBtn["text"] == "CAPTURE IMAGE":
        captureBtn.configure(text="CAPTURE AGAIN")
    captured = captureImage(stdId)
    if captured:
        saveBtn['state'] = NORMAL
    else:
        print("Capture failed")

def changeDropdown(*args):
    global selectedSemID
    # print(spSemester.get())
    selectedSemID = semesterData[spSemester.current()][0]

def changeSession(*args):
    global sessionID
    sessionID = sessionData[spSession.current()][0]

def getSpinnerData(spSemester, spSession):
    cursor = db.cursor()
    sql = "SELECT * FROM semester"
    cursor.execute(sql)
    semesterResult = cursor.fetchall()
    cursor.close()

    semesterChoice = []
    for val in semesterResult:
        semesterChoice.append(val[1])
    spSemester['values'] = semesterChoice

    cursor2 = db.cursor()
    sql = "SELECT * FROM session"
    cursor2.execute(sql)
    sessionResult = cursor2.fetchall()
    cursor.close()
    sessionChoice = []
    for val in sessionResult:
        sessionChoice.append(val[1])
    #sessionData = sessionResult
    spSession['values'] = sessionChoice

    return semesterResult, sessionResult

def getSemesterData(spSemester):
    global semesterChoice
    cursor = db.cursor()
    sql = "SELECT * FROM semester"
    cursor.execute(sql)
    semesterResult = cursor.fetchall()
    cursor.close()

    semesterChoice = []
    for val in semesterResult:
        semesterChoice.append(val[1])
    spSemester['values'] = semesterChoice

    return semesterResult

def getSessionData(spSession):
    global sessionChoice
    cursor = db.cursor()
    sql = "SELECT * FROM session"
    cursor.execute(sql)
    sessionResult = cursor.fetchall()
    cursor.close()
    sessionChoice = []
    for val in sessionResult:
        sessionChoice.append(val[1])
    #sessionData = sessionResult
    spSession['values'] = sessionChoice

    return sessionResult

def insertStudent(stdName, sessionID, selectedSemID, phone, email):
    global stdId
    try:
        cursor = db.cursor()
        sql = "INSERT INTO student (std_id, name, session_id, phone, email) VALUES(%s,%s,%s,%s,%s)"
        val = (stdId, stdName, sessionID, phone, email)
        cursor.execute(sql, val)
        #db.commit()
        print(cursor.rowcount, "row was inserted.")
        if cursor.rowcount > 0:
            insertStudentSemester(cursor, stdId, selectedSemID)
    except Exception as e:
        print("Error:", e)
        messagebox.showerror(title="Error", message="Error: {}".format(e))
        db.rollback()
        cursor.close()
    # finally:
    #     cursor.close()

def insertStudentSemester(cursor, stdId, selectedSemID):
    try:
        #cursor = db.cursor()
        sql = "INSERT INTO student_semester (std_id, semester_id) VALUES(%s,%s)"
        val = (stdId, selectedSemID)
        cursor.execute(sql, val)
        db.commit()
        print(cursor.rowcount, "row was inserted.")
        messagebox.showinfo(title="Success", message="Successfully added student information!")
    except Exception as e:
        print("Error:", e)
        messagebox.showerror(title="Error", message="Error: {}".format(e))
        db.rollback()
    finally:
        cursor.close()

def captureImage(stdId):
    try:
        cd.startCapturing(stdId)
        return True
    except Exception as e:
        messagebox.showerror(title="Error", message="Error: {}".format(e))
        return False

def closeAll():
    if db.open == 1:
        db.close()
    root.destroy()


if __name__ == '__main__':

    selectedSemID = 0
    sessionID = 0
    stdId = ""

    Label(root,text="Enter Student Details", fg='white', bg='#424242', font=("helvetica",30),width=23).grid(rowspan=2,columnspan=3,sticky=E+W+N+S,padx=5,pady=5)

    Label(root, text="ID: ", font=("helvetica ",20), fg='#212121',bg="#D7CCC8").grid(row=2,sticky=E,column=0)

    Label(root, text="Name: ", font=("helvetica ",20), fg='#212121',bg="#D7CCC8").grid(row=3,sticky=E,column=0)

    Label(root, text="Session: ", font=("helvetica ",20), fg='#212121',bg="#D7CCC8").grid(row=4,sticky=E,column=0)

    Label(root, text="Semester: ", font=("helvetica ",20), fg='#212121',bg="#D7CCC8").grid(row=5,sticky=E,column=0)

    Label(root, text="Phone: ", font=("helvetica ",20), fg='#212121',bg="#D7CCC8").grid(row=6,sticky=E,column=0)

    Label(root, text="Email: ", font=("helvetica ",20), fg='#212121',bg="#D7CCC8").grid(row=7,sticky=E,column=0)

    std_id_entry=Entry(root)
    name_entry=Entry(root)
    std_phone_entry=Entry(root)
    std_email_entry=Entry(root)

    std_id_entry.grid(row=2,column=1,columnspan=2,sticky=W)
    name_entry.grid(row=3,column=1,columnspan=2,sticky=W)
    std_phone_entry.grid(row=6,column=1,columnspan=2,sticky=W)
    std_email_entry.grid(row=7,column=1,columnspan=2,sticky=W)

    clearBtn = Button(root,text="EXIT",font=("times new roman",20), fg="white",bg="#3E2723",command=closeAll)#root.quit
    clearBtn.grid(row=8,column=0, pady=5,padx=5,sticky=E+W+N+S)

    captureBtn =Button(root,text="CAPTURE IMAGE",font=("times new roman",20), fg="white",bg="#3E2723",command=getInput)
    captureBtn.grid(row=8,column=1,pady=5,padx=5,sticky=E+W+N+S)

    saveBtn =Button(root,text="SAVE",font=("times new roman",20), fg="white",bg="#3E2723",command=validateInput, state=DISABLED)
    saveBtn.grid(row=8,column=2,pady=5,padx=5,sticky=E+W+N+S)
    #saveBtn.visibility = False

    #tkvar = StringVar(root)
    # choices = ['First Semester', 'Second Semester', 'Third Semester', 'Fourth Semester',
    # 'Fifth Semester', 'Sixth Semester', 'Seven Semester', 'Eight Semester', 'MS First Semester']
    semesterChoice = []
    sessionChoice = []
    # tkvar.set(choices[0])

    # spinner = OptionMenu(root, tkvar, *choices)
    # spinner.grid(row=4,column=1, pady=5,padx=5,sticky=E+W+N+S)
    # #Linking function to spinner
    # tkvar.trace('w', changeDropdown)

    spSemester = ttk.Combobox(root, values=semesterChoice, state='readonly')

    spSession = ttk.Combobox(root, values=sessionChoice, state='readonly')

    #semesterData, sessionData = getSpinnerData(spSemester, spSession)
    semesterData = getSemesterData(spSemester)
    sessionData = getSessionData(spSession)

    spSemester.grid(row=5,column=1, pady=5,padx=5,sticky=E+W+N+S)
    #spSemester.current(0)
    spSemester.bind('<<ComboboxSelected>>', changeDropdown)
    #print(spSemester.current(), spSemester.get())

    #getSpinnerData(spSemester)

    spSession.grid(row=4,column=1, pady=5,padx=5,sticky=E+W+N+S)
    #spSession.current(0)
    spSession.bind('<<ComboboxSelected>>', changeSession)

    root.mainloop()