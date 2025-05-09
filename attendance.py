
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
# import mysql.connector # Removed for execution in this environment
import cv2
import os
import csv
from tkinter import filedialog

mydata = []

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # variables
        self.var_atten_id = tk.StringVar()
        self.var_atten_roll = tk.StringVar()
        self.var_atten_name = tk.StringVar()
        self.var_atten_dep = tk.StringVar()
        self.var_atten_time = tk.StringVar()
        self.var_atten_date = tk.StringVar()
        self.var_atten_attendance = tk.StringVar()

        img1 = Image.open(r"college_images\smart-attendance.jpg")
        img1 = img1.resize((800, 200), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = tk.Label(self.root, image=self.photoimg1)
        f_lbl.place(x=0, y=0, width=800, height=200)

        img2 = Image.open(r"college_images\iStock-182059956_18390_t12.jpg")
        img2 = img2.resize((800, 200), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = tk.Label(self.root, image=self.photoimg2)
        f_lbl.place(x=800, y=0, width=800, height=200)

        # Using a simple background color instead of an image for better compatibility
        bg_img = tk.Frame(self.root, bg="lightblue") # Changed from Label to Frame and set background color
        bg_img.place(x=0, y=200, width=1550, height=710)


        title_lbl = tk.Label(bg_img, text="ATTENDANCE MANAGEMENT SYSTEM", font=("times new roman", 35, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame = tk.Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=20, y=55, width=1480, height=600)

        # left label frame
        Left_frame = tk.LabelFrame(main_frame, bd=2, bg="white", relief=tk.RIDGE, text="student details", font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=730, height=580)

        img_left = Image.open(r"college_images\face-recognition.png")
        img_left = img_left.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl = tk.Label(Left_frame, image=self.photoimg_left)
        f_lbl.place(x=5, y=0, width=720, height=130)

        left_inside_frame = tk.Frame(Left_frame, bd=2, relief=tk.RIDGE, bg="white")
        left_inside_frame.place(x=0, y=135, width=720, height=370)

        # label and entry
        # student id
        attendance_label = tk.Label(left_inside_frame, text="Attendanceid:", font=("times new roman", 13, "bold"), bg="white")
        attendance_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        attendance_entry = ttk.Entry(left_inside_frame, width=20, textvariable=self.var_atten_id, font=("times new roman", 13, "bold"))
        attendance_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        rollLabel = tk.Label(left_inside_frame, text="Roll:", font=("comicsansns", 11, "bold"), bg="white")
        rollLabel.grid(row=0, column=2, padx=4, pady=8)

        atten_roll = ttk.Entry(left_inside_frame, textvariable=self.var_atten_roll, width=20, font=("comicsansns", 11, "bold"))
        atten_roll.grid(row=0, column=3, pady=8)

        nameLabel = tk.Label(left_inside_frame, text="Name:", font=("comicsansns", 11, "bold"), bg="white")
        nameLabel.grid(row=1, column=0)

        atten_name = ttk.Entry(left_inside_frame, textvariable=self.var_atten_name, width=22, font=("comicsansns", 11, "bold"))
        atten_name.grid(row=1, column=1, pady=8)

        depLabel = tk.Label(left_inside_frame, text="Department:", font=("comicsansns", 11, "bold"), bg="white")
        depLabel.grid(row=1, column=2)

        atten_dep = ttk.Entry(left_inside_frame, textvariable=self.var_atten_dep, width=22, font=("comicsansns", 11, "bold"))
        atten_dep.grid(row=1, column=3, pady=8)

        timeLabel = tk.Label(left_inside_frame, text="Time:", font=("comicsansns", 11, "bold"), bg="white")
        timeLabel.grid(row=2, column=0)

        atten_time = ttk.Entry(left_inside_frame, textvariable=self.var_atten_time, width=22, font=("comicsansns", 11, "bold"))
        atten_time.grid(row=2, column=1, pady=8)

        dateLabel = tk.Label(left_inside_frame, text="Date:", font=("comicsansns", 11, "bold"), bg="white")
        dateLabel.grid(row=2, column=2)

        atten_date = ttk.Entry(left_inside_frame, textvariable=self.var_atten_date, width=22, font=("comicsansns", 11, "bold"))
        atten_date.grid(row=2, column=3, pady=8)

        attendance_label = tk.Label(left_inside_frame, text="Attendance Status", bg="white", font="comicsansns 11 bold")
        attendance_label.grid(row=3, column=0)

        self.atten_status = ttk.Combobox(left_inside_frame, textvariable=self.var_atten_attendance, width=20, font="comicsansns 11 bold", state="readonly")
        self.atten_status["values"] = ("Status", "Present", "Absent")
        self.atten_status.grid(row=3, column=1, pady=8)
        self.atten_status.current(0)

        # buttons frame
        btn_frame = tk.Frame(left_inside_frame, bd=2, relief=tk.RIDGE, bg="white")
        btn_frame.place(x=0, y=300, width=715, height=35)

        save_btn = tk.Button(btn_frame, text="Import csv", command=self.importCsv, width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        save_btn.grid(row=0, column=0, )

        update_btn = tk.Button(btn_frame, text="Export csv", command=self.exportCsv, width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        update_btn.grid(row=0, column=1, )

        # Modified Update button with command
        delete_btn = tk.Button(btn_frame, text="Update", command=self.update_data, width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        delete_btn.grid(row=0, column=2, )

        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_data, width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        reset_btn.grid(row=0, column=3, )

        # right label frame
        Right_frame = tk.LabelFrame(main_frame, bd=2, bg="white", relief=tk.RIDGE, text="attendance Details", font=("times new roman", 12, "bold"))
        Right_frame.place(x=750, y=10, width=720, height=580)

        table_frame = tk.Frame(Right_frame, bd=2, relief=tk.RIDGE, bg="white")
        table_frame.place(x=5, y=5, width=700, height=455)

        # scrollbar
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.AttendanceReportTable = ttk.Treeview(table_frame, column=("id", "roll", "name", "department", "time", "date", "attendance"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id", text="Attendance ID")
        self.AttendanceReportTable.heading("roll", text="Roll")
        self.AttendanceReportTable.heading("name", text="Name")
        self.AttendanceReportTable.heading("department", text="Department")
        self.AttendanceReportTable.heading("time", text="Time")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("attendance", text="Attendance")

        self.AttendanceReportTable["show"] = "headings"

        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("roll", width=100)
        self.AttendanceReportTable.column("name", width=100)
        self.AttendanceReportTable.column("department", width=100)
        self.AttendanceReportTable.column("time", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)

        self.AttendanceReportTable.pack(fill=tk.BOTH, expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)

    # fetch data
    def fetchData(self, rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("", tk.END, values=i)

    # import csv
    def importCsv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("ALL File", "*.*")), parent=self.root)
        if not fln: # Added check if file selection was cancelled
            return
        with open(fln, mode='r', newline='') as myfile: # Added mode='r', newline=''
            csvread = csv.reader(myfile) # Removed delimiter as comma is default
            # Skip header row if present
            try:
                header = next(csvread)
                # Optional: Check if header matches expected columns
                # print(f"Header: {header}") # For debugging
            except StopIteration:
                messagebox.showinfo("Info", "The selected CSV file is empty.", parent=self.root)
                return

            for i in csvread:
                # Pad rows with empty strings if they have fewer columns than expected (7)
                padded_row = i + [""] * (7 - len(i))
                mydata.append(padded_row[:7]) # Ensure we only keep the first 7 elements

            self.fetchData(mydata)
            messagebox.showinfo("Success", "CSV file imported successfully", parent=self.root)


    # export csv
    def exportCsv(self):
        try:
            if len(mydata) < 1:
                messagebox.showerror("No Data found to export", parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("ALL File", "*.*")), parent=self.root)
            if not fln: # Added check if file saving was cancelled
                return
            with open(fln, mode="w", newline="") as myfile:
                exp_write = csv.writer(myfile) # Removed delimiter as comma is default
                # Optional: Write header row
                exp_write.writerow(["Attendance ID", "Roll", "Name", "Department", "Time", "Date", "Attendance"])
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export", "Your data exported to " + os.path.basename(fln) + " successfully")
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    # Modified get_cursor with index error handling and corrected syntax
    def get_cursor(self, event=""):
        cursor_row = self.AttendanceReportTable.focus()
        content = self.AttendanceReportTable.item(cursor_row)
        rows = content['values']

        # Safely access list elements by checking the length
        if len(rows) > 0 and rows[0] is not None: # Added check for None
            self.var_atten_id.set(rows[0])
        else:
            self.var_atten_id.set("")

        if len(rows) > 1 and rows[1] is not None: # Added check for None
            self.var_atten_roll.set(rows[1])
        else:
            self.var_atten_roll.set("")

        if len(rows) > 2 and rows[2] is not None: # Added check for None
            self.var_atten_name.set(rows[2])
        else:
            self.var_atten_name.set("")

        if len(rows) > 3 and rows[3] is not None: # Corrected syntax: len(rows)
            self.var_atten_dep.set(rows[3])
        else:
            self.var_atten_dep.set("")

        if len(rows) > 4 and rows[4] is not None: # Added check for None
            self.var_atten_time.set(rows[4])
        else:
            self.var_atten_time.set("")

        if len(rows) > 5 and rows[5] is not None: # Added check for None
            self.var_atten_date.set(rows[5])
        else:
            self.var_atten_date.set("")

        if len(rows) > 6 and rows[6] is not None: # Added check for None
            self.var_atten_attendance.set(rows[6])
        else:
            self.var_atten_attendance.set("")

    # New method to update data
    def update_data(self):
        global mydata
        atten_id = self.var_atten_id.get()

        if not atten_id:
            messagebox.showerror("Error", "Please select a record to update by clicking on it in the table.", parent=self.root)
            return

        updated = False
        # Find the index of the record with the matching Attendance ID
        update_index = -1
        for i in range(len(mydata)):
            # Ensure the row has at least one element before accessing index 0
            if len(mydata[i]) > 0 and str(mydata[i][0]) == str(atten_id): # Convert to string for comparison
                update_index = i
                break

        if update_index != -1:
            # Update the record in mydata at the found index
            # Ensure the list has enough elements before attempting to update
            while len(mydata[update_index]) < 7:
                mydata[update_index].append("") # Pad with empty strings if necessary

            mydata[update_index][0] = self.var_atten_id.get()
            mydata[update_index][1] = self.var_atten_roll.get()
            mydata[update_index][2] = self.var_atten_name.get()
            mydata[update_index][3] = self.var_atten_dep.get()
            mydata[update_index][4] = self.var_atten_time.get()
            mydata[update_index][5] = self.var_atten_date.get()
            mydata[update_index][6] = self.var_atten_attendance.get()

            updated = True

        if updated:
            self.fetchData(mydata) # Refresh the Treeview
            messagebox.showinfo("Success", "Attendance record updated successfully", parent=self.root)
            self.reset_data() # Clear input fields after update
        else:
            messagebox.showerror("Error", f"Record with Attendance ID '{atten_id}' not found in the imported data.", parent=self.root)


    def reset_data(self):
        self.var_atten_id.set("")
        self.var_atten_roll.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("Status") # Reset combobox to default


if __name__ == "__main__":
    root = tk.Tk()
    obj = Attendance(root)
    root.mainloop()