from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import cv2
import os
import csv
import numpy as np

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.present_ids = set()
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # GUI components
        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # Left image
        img_top = Image.open(r"college_images\face_detector1.jpg")
        img_top = img_top.resize((650, 700), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl_left = Label(self.root, image=self.photoimg_top)
        f_lbl_left.place(x=0, y=55, width=650, height=700)

        # Right image
        img_bottom = Image.open(r"college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
        img_bottom = img_bottom.resize((950, 700), Image.Resampling.LANCZOS)
        self.img_bottom = ImageTk.PhotoImage(img_bottom)
        f_lbl_right = Label(self.root, image=self.img_bottom)
        f_lbl_right.place(x=650, y=55, width=950, height=700)

        # Face Recognition button
        b1_1 = Button(f_lbl_right, text="Face Recognition", cursor="hand2", command=self.face_recog,
                     font=("times new roman", 18, "bold"), bg="darkgreen", fg="white")
        b1_1.place(x=375, y=620, width=200, height=40)

        btn_frame= Frame(self.root,bd=2,relief=RIDGE,bg="white",)
        btn_frame.place(x=250,y=650)

        update_btn = Button(btn_frame, text="Update Attendance", command=self.update_attendance_file, font=("times new roman", 12, "bold"), bg="blue", fg="white", width=20)
        update_btn.grid(row=0, column=1, padx=10, pady=10)

    def mark_attendance(self, student_id, roll, name, department):
        filename = "abc.csv"
        today = datetime.now().strftime("%d/%m/%Y")
        
        # Check if attendance already marked today
        exists = False
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 6 and row[0] == student_id and row[5] == today:
                        exists = True
                        break
        except FileNotFoundError:
            pass  # File doesn't exist yet, will create new

        if not exists:
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                current_time = datetime.now().strftime("%H:%M:%S")
                writer.writerow([student_id, roll, name, department, current_time, today, "Present"])

    def face_recog(self):
        def draw_boundary(img, classifier, clf):
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                id, confidence = clf.predict(gray_img[y:y+h, x:x+w])
                confidence = int((100 * (1 - confidence / 300)))

                # Database connection
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="wani321",
                    database="sys"
                )
                cursor = conn.cursor()

                # Fetch student details
                cursor.execute("SELECT Student_id, Name, Roll, Dep FROM student WHERE Student_id=%s", (id,))
                result = cursor.fetchone()

                if result and confidence > 77:
                    student_id, name, roll, department = result
                    self.mark_attendance(str(student_id), str(roll), name, department)
                    self.present_ids.add(str(id))

                    # Display info on frame
                    cv2.putText(img, f"ID: {student_id}", (x, y-75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll: {roll}", (x, y-55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name: {name}", (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Dept: {department}", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
                else:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)

            return img

        # Load face recognition components
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, frame = video_cap.read()
            if not ret:
                break

            frame = draw_boundary(frame, face_cascade, clf)
            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) == 13:  # Enter key to exit
                break

        video_cap.release()
        cv2.destroyAllWindows()


    def update_attendance_file(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="wani321",
                database="sys"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT Student_id, Name FROM student")
            all_students = cursor.fetchall()
            conn.close()

            present_ids= self.present_ids
            from datetime import datetime
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"attendance_{date_str}.csv"

            with open(filename, "w", newline="") as f:  
                writer = csv.writer(f)
                writer.writerow(["Student ID", "Name", "Status"])

                for student_id, name in all_students:
                    status = "Present" if str(student_id) in present_ids else "Absent"
                    writer.writerow([student_id, name, status])

            messagebox.showinfo("Success", "abc.csv updated with present and absent students", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)

   

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()












































# from tkinter import*
# from tkinter import ttk
# from PIL import Image,ImageTk
# from tkinter import messagebox
# import mysql.connector
# from time import strftime
# from datetime import datetime
# import cv2
# import os
# import numpy as np





# class Face_Recognition:
#     def __init__(self,root):
#         self.root=root
#         self.root.geometry("1530x790+0+0")
#         self.root.title("Face Recognition System")


#         title_lbl=Label(self.root,text="FACE RECOGNITION",font=("times new roman",35,"bold"),bg="white",fg="green")
#         title_lbl.place(x=0,y=0,width=1530,height=45)

#         img_top=Image.open(r"college_images\face_detector1.jpg")
#         img_top=img_top.resize((650,700),Image.Resampling.LANCZOS)
#         self.photoimg_top=ImageTk.PhotoImage(img_top)

#         f_lbl=Label(self.root,image=self.photoimg_top)
#         f_lbl.place(x=0,y=55,width=650,height=700)

#         img_bottom=Image.open(r"college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
#         img_bottom=img_bottom.resize((950,700),Image.Resampling.LANCZOS)
#         self.img_bottom=ImageTk.PhotoImage(img_bottom)

#         f_lbl=Label(self.root,image=self.img_bottom)
#         f_lbl.place(x=650,y=55,width=950,height=700)

#         b1_1=Button(f_lbl,text="Face Recognition",cursor="hand2",command=self.face_recog,font=("times new roman",18,"bold"),bg="darkgreen",fg="white")
#         b1_1.place(x=375,y=620,width=200,height=40)

#         #attendance
#     def mark_attendance(self,i,r,n,d):
#         with open("abc.csv","r+",newline="\n") as f:
#             myDataList=f.readlines()
#             name_list=[]
#             for line in myDataList:
#                 entry=line.split(',') 
#                 name_list.append(entry[0])
#             if(i not in name_list):
#                 now=datetime.now()
#                 d1=now.strftime("%d/%m/%Y")
#                 dtString=now.strftime("%H:%M:%S")
#                 f.seek(0,2)
#                 f.write(f"\n{i},{r},{n},{d},{dtString},{d1},Present")



#         #face recognition
#     # def face_recog(self):
#     #     def draw_boundary(img,classifier,scaleFactor,minneighbours,color,text,clf):
#     #         gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
#     #         features=classifier.detectMultiScale(gray_image,scaleFactor,minneighbours)

#     #         coord=[]

#     #         for (x,y,w,h) in features:
#     #             cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
#     #             id,predict=clf.predict(gray_image[y:y+h,x:x+w])
#     #             confidance=int((100*(1-predict/300)))

#     #             conn=mysql.connector.connect(host="localhost",username="root",password="wani321",database="sys")
#     #             my_cursor=conn.cursor()

#     #             my_cursor.execute("SELECT Name FROM student WHERE Student_id="+str(id))
#     #             n=my_cursor.fetchone()
#     #             n="+".join(n) if n else "Unknown"

#     #             my_cursor.execute("SELECT Roll FROM student WHERE Student_id="+str(id))
#     #             r=my_cursor.fetchone()
#     #             r="+".join(r) if r else "Unknown"

#     #             my_cursor.execute("SELECT Dep FROM student WHERE Student_id="+str(id))
#     #             d=my_cursor.fetchone()
#     #             d="+".join(d) if d else "Unknown"
                    
                    



#     #             if confidance>77:
#     #                 cv2.putText(img,f"R0ll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
#     #                 cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
#     #                 cv2.putText(img,f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
#     #             else:
#     #                 cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
#     #                 cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)

#     #             coord=[x,y,w,h]

#     #         return coord
#     #     def recognize(img,clf,faceCascade):
#     #         coord=draw_boundary(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
#     #         return img
#     #     faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#     #     clf=cv2.face.LBPHFaceRecognizer_create()
#     #     clf.read("classifier.xml")

#     #     video_cap=cv2.VideoCapture(0)

#     #     while True:
#     #         ret,img=video_cap.read()
#     #         img=recognize(img,clf,faceCascade)
#     #         cv2.imshow("Welcome To Face Recognition",img)

#     #         if cv2.waitKey(1)==13:
#     #             break
#     #     video_cap.release()
#     #     cv2.destroyAllWindows()

#     def face_recog(self):
#         def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
#             gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             features = classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#             coord = []

#             for (x, y, w, h) in features:
#                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
#                 id, predict = clf.predict(gray_image[y:y + h, x:x + w])
#                 confidence = int((100 * (1 - predict / 300)))

#                 conn = mysql.connector.connect(host="localhost", username="root", password="wani321", database="sys")
#                 my_cursor = conn.cursor()

#                 my_cursor.execute("select Name from student where Student_id=" + str(id))
#                 n = my_cursor.fetchone()
#                 n = "+".join(n) if n else "Unknown"

#                 my_cursor.execute("select Roll from student where Student_id=" + str(id))
#                 r = my_cursor.fetchone()
#                 r = "+".join(r) if r else "Unknown"

#                 my_cursor.execute("select Dep from student where Student_id=" + str(id))
#                 d = my_cursor.fetchone()
#                 d = "+".join(d) if d else "Unknown"

#                 my_cursor.execute("select Student_id from student where Student_id=" + str(id))
#                 i = my_cursor.fetchone()
#                 i = "+".join(i) if i else "Unknown"


#                 if confidence > 77:
#                     cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
#                     cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
#                     cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
#                     cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
#                     self.mark_attendance(i,r,n,d)
#                 else:
#                     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
#                     cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

#                 coord = [x, y, w, h]

#             return coord

#         def recognize(img, clf, faceCascade):
#             coord = draw_boundary(img, faceCascade, 1.1, 5, (255, 25, 255), "Face", clf)
#             return img

#         faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#         clf = cv2.face.LBPHFaceRecognizer_create()
#         clf.read("classifier.xml")

#         video_cap = cv2.VideoCapture(0)

#         while True:
#             ret, img = video_cap.read()
#             if not ret:
#                 break

#             img = recognize(img, clf, faceCascade)
#             cv2.imshow("Welcome To Face Recognition", img)

#             if cv2.waitKey(1) == 13:  # Press Enter to exit
#                 break

#         video_cap.release()
#         cv2.destroyAllWindows()

        








# if __name__ == "__main__":
#     root=Tk()
#     obj=Face_Recognition(root)
#     root.mainloop()
