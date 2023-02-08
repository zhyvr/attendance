from tkinter import *
import tkinter
import cv2
import os
from datetime import datetime
import numpy as np
import face_recognition
import csv

d = datetime.now().strftime("%d%m%Y")

class Register(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('700x400')
        self.title('AViaFace - Register')

        def clicked():
            #lbl.configure(text="Button was clicked !!")
            fff(namefill.get(),idfill.get(),deptfill.get())

        ######################################################################### Buttons
        # Creating a Button
        b1 = Button(self, text='Capture and Register', command=clicked, width=17, height=3)
        # Set the position of button to coordinate (x=225, y=100)
        b1.place(x=275, y=150)

        # Creating a Button
        b3 = Button(self, text='EXIT', command=self.destroy, width=17, height=3)
        # Set the position of button to coordinate (x=225, y=300)
        b3.place(x=275, y=225)
        #########################################################################

        ######################################################################### Labels
        # Creating a Labels
        l1 = Label(self, text="Name: ", font=('tahoma', 13, ' bold '))
        l1.place(x=80, y=10)

        l2 = Label(self, text="Department: ", font=('tahoma', 13, ' bold '))
        l2.place(x=80, y=60)

        l3 = Label(self, text="ID: ", font=('tahoma', 13, ' bold '))
        l3.place(x=80, y=110)


        help = Label(self, text="Click on 'Capture and Register' then 'SPACE' To capture and 'ESC' to Exit ",
                     font=('tahoma', 13))
        help.place(x=50, y=340)

        namefill = Entry(self, width=40)
        namefill.place(x=200, y=10)

        deptfill = Entry(self, width=40)
        deptfill.place(x=200, y=60)

        idfill = Entry(self, width=40)
        idfill.place(x=200, y=110)

        #########################################################################


        def fff(name, id,dept):
            cam = cv2.VideoCapture(0)

            cv2.namedWindow("test")

            while True:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("test", frame)

                k = cv2.waitKey(1)
                if k % 256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k % 256 == 32:
                    # SPACE pressed
                    img_name = name + "_" + dept + "_" + id + ".jpg"

                    path = os.getcwd() + "/attendanceImages"
                    cv2.imwrite(os.path.join(path, img_name), frame)
                    print("captured")
                    break

            cam.release()

            cv2.destroyAllWindows()

class Markattendance:
    def __init__(self):

        print(d)

        attendancefile = "attendance"+"_"+d+ ".csv"

        fileexist = os.path.exists(attendancefile)

        if fileexist == True:
            print("haya")
        else:
            f = open(attendancefile, "w")
            f.write("Name, Department, ID, Date, Time \n")
            f.close()


        path = 'attendanceImages'
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f"{path}/{cl}")
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markAttendance(name):
            namez = name.split("_")
            namee = namez[0]
            deptt = namez[1]
            idd = namez[2]
            with open(attendancefile, 'r+') as f:
                myDataList = f.readlines()
                # print(myDataList)
                nameList = []
                for line in myDataList:
                    entry = line.split(" , ")
                    nameList.append(entry[0])
                if namee not in nameList:
                    now = datetime.now()
                    timee = now.strftime("%H:%M:%S")
                    datee = datetime.now().strftime("%d/%m/%Y")
                    f.writelines(f"\n{namee} , {deptt}, {idd} , {datee} , {timee}")

        encodeListKnown = findEncodings(images)
        # print(len(encodeListKnown))
        print("Encoding Completed!")

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            imgS  = cv2.resize(img, (0,0), None, 0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)
    
                if faceDis[matchIndex] < 0.50:
                    name = classNames[matchIndex].upper()
                    markAttendance(name)
                else:
                    name = 'Unknown'
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name.split("_")[0], (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                cv2.imshow("Webcam", img)
                cv2.waitKey(1)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                cap.release()
                cv2.destroyAllWindows()
                break


class Display(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('800x400')
        self.title('AViaFace - View')

        # create main frame
        main_frame = Frame(self)
        main_frame.pack(fill=BOTH, expand=1)

        # craete a canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # create a scrollbar to canvas
        my_scrollbar = tkinter.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # configure the canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # create another frame in the canvas
        second_frame = Frame(my_canvas)

        # add that new frame to a window in the canvas

        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        # open file
        with open("attendance"+"_"+d+ ".csv", newline="") as file:
            reader = csv.reader(file)

            # r and c tell us where to grid the labels
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    # i've added some styling
                    label = tkinter.Label(second_frame, width=16, height=2, text=row, relief=tkinter.RIDGE)
                    label.grid(row=r, column=c)
                    c += 1
                r += 1


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('800x600')
        self.title('AViaFace')

        ######################################################################### Buttons
        # Creating a Button
        b1 = Button(self, text = 'MARK ATTENDANCE', command = self.MARK_ATTENDANCE,width=17, height=3)
        # Set the position of button to coordinate (x=333, y=100)
        b1.place(x=333, y=110)

        # Creating a Button
        b2 = Button(self, text = 'VIEW ATTENDANCE', command = self.DISPLAY, width=17, height=3)
        # Set the position of button to coordinate (x=333, y=175)
        b2.place(x=333, y=185)

        # Creating a Button
        b3 = Button(self, text = 'REGISTER', command = self.REGISTER,width=17, height=3)
        # Set the position of button to coordinate (x=333, y=250)
        b3.place(x=333, y=260)

        # Creating a Button
        b4 = Button(self, text='EXIT', command=self.destroy, width=17, height=3)
        # Set the position of button to coordinate (x=333, y=325)
        b4.place(x=333, y=335)
        #########################################################################

        ######################################################################### Labels
        # Creating a Labels
        l1 = Label(text="Face Recognition based Attendance System",font=('tahoma', 20, ' bold '))
        l1.place(x=125, y=20)

        #l2 = Label(text="Made with <3 By Dyaree, Sako and Zhyar",font=('tahoma', 13))
        #l2.place(x=275, y=460)
        #########################################################################

    def MARK_ATTENDANCE(self):
        Markattendance()

    def REGISTER(self):
        window = Register(self)
        window.grab_set()

    def DISPLAY(self):
        window = Display(self)
        window.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()