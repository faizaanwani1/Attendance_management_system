
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np


class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="TRAIN DATA SET", font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"college_images/facialrecognition.png")
        img_top = img_top.resize((1530, 325), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=325)

        b1_1 = Button(self.root, text="TRAIN DATA", command=self.train_classifier, cursor="hand2",
                      font=("times new roman", 30, "bold"), bg="red", fg="white")
        b1_1.place(x=0, y=380, width=1530, height=60)

        img_bottom = Image.open(r"college_images/opencv_face_reco_more_data.jpg")
        img_bottom = img_bottom.resize((1530, 325), Image.Resampling.LANCZOS)
        self.img_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.img_bottom)
        f_lbl.place(x=0, y=440, width=1530, height=325)

    def train_classifier(self):
        data_dir = "data"

        # Check if the data directory exists
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", f"Directory '{data_dir}' not found!")
            return

        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.jpg') or file.endswith('.png')]

        if len(path) == 0:
            messagebox.showwarning("Warning", "No valid images found for training.")
            return

        faces = []
        ids = []

        cv2.namedWindow("Training", cv2.WINDOW_NORMAL)

        for image in path:
            img = Image.open(image).convert('L')
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)

            cv2.imshow("Training", imageNp)
            if cv2.waitKey(1) == 13:  # Press Enter to stop
                break

        cv2.destroyAllWindows()

        if len(faces) == 0 or len(ids) == 0:
            messagebox.showwarning("Warning", "No valid faces found for training.")
            return

        ids = np.array(ids)

        # Train the classifier and save
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")

        messagebox.showinfo("Result", "Training dataset completed!!!")


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()