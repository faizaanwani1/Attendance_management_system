from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector # Needed to fetch student names potentially - still here but not used in this code
import cv2 # Original import, might not be needed for detention list specifically - still here
import os
import csv
from datetime import datetime, timedelta

class Developer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Developer Info & Attendance Alert") # Updated title

        # --- Top Title ---
        title_lbl = Label(self.root, text="DEVELOPER & ATTENDANCE ALERT", font=("times new roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # --- Background Image ---
        try:
            # Use forward slashes or os.path.join
            image_path = "college_images/dev.jpg"
            img_top = Image.open(image_path)
            img_top = img_top.resize((1530, 720), Image.Resampling.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)

            f_lbl = Label(self.root, image=self.photoimg_top)
            f_lbl.place(x=0, y=55, width=1530, height=720)
        except FileNotFoundError:
            f_lbl = Label(self.root, text=f"Background image not found:\n{image_path}", font=("times new roman", 18), fg="red", bg="white")
            f_lbl.place(x=0, y=55, width=1530, height=720)
        except Exception as e:
            f_lbl = Label(self.root, text=f"An error occurred loading image: {e}", font=("times new roman", 18), fg="red", bg="white")
            f_lbl.place(x=0, y=55, width=1530, height=720)


        # --- Original Developer Info Frame (Right Side) ---
        dev_info_frame = Frame(f_lbl, bd=2, relief=RIDGE, bg="lightblue") # Changed background slightly
        dev_info_frame.place(x=1000, y=20, width=500, height=250) # Adjusted position/size

        try:
            # Developer icon
            img_icon_path = r"college_images/facialrecognition (1).png"
            img_top1 = Image.open(img_icon_path)
            img_top1 = img_top1.resize((100, 100), Image.Resampling.LANCZOS)
            self.photoimg_top1 = ImageTk.PhotoImage(img_top1)
            icon_lbl = Label(dev_info_frame, image=self.photoimg_top1, bg="lightblue")
            icon_lbl.place(x=380, y=5, width=100, height=100)
        except FileNotFoundError:
             icon_lbl = Label(dev_info_frame, text="Icon\nNot Found", font=("times new roman", 10), fg="red", bg="lightblue")
             icon_lbl.place(x=380, y=5, width=100, height=100)
        except Exception as e:
             icon_lbl = Label(dev_info_frame, text=f"Icon Error:\n{e}", font=("times new roman", 10), fg="red", bg="lightblue")
             icon_lbl.place(x=380, y=5, width=100, height=100)


        # Developer names
        dev_label_title = Label(dev_info_frame, text="Developed by:", font=("times new roman", 15, "bold", "underline"), bg="lightblue", fg="darkblue")
        dev_label_title.place(x=10, y=10)

        dev_label1 = Label(dev_info_frame, text="Faizaan Wani", font=("times new roman", 13, "bold"), bg="lightblue", fg="black")
        dev_label1.place(x=20, y=45)
        dev_label2 = Label(dev_info_frame, text="Sahil Kumar", font=("times new roman", 13, "bold"), bg="lightblue", fg="black")
        dev_label2.place(x=20, y=70)
        dev_label3 = Label(dev_info_frame, text="Rahul Thappa", font=("times new roman", 13, "bold"), bg="lightblue", fg="black")
        dev_label3.place(x=20, y=95)
        dev_label4 = Label(dev_info_frame, text="Muneeb Awan", font=("times new roman", 13, "bold"), bg="lightblue", fg="black")
        dev_label4.place(x=20, y=120)

        # Placeholder for the lower image if needed
        # img2=Image.open(r"college_images\KPIs-and-Agile-software-development-metrics-for-teams-1.jpg")
        # img2=img2.resize((500,400),Image.Resampling.LANCZOS)
        # self.photoimg2=ImageTk.PhotoImage(img2)
        # f_lbl2=Label(dev_info_frame,image=self.photoimg2)
        # f_lbl2.place(x=0,y=200,width=500,height=400) # Adjust as needed


        # --- Detention List Frame (Left Side) ---
        detention_frame = Frame(f_lbl, bd=2, relief=RIDGE, bg="white")
        detention_frame.place(x=50, y=20, width=900, height=680) # Adjusted size

        detention_title = Label(detention_frame, text="Weekly Attendance Alert (< 75%)", font=("times new roman", 20, "bold"), bg="white", fg="red")
        detention_title.pack(side=TOP, pady=10)

        # Button to trigger calculation
        calc_button = ttk.Button(detention_frame, text="Show Last Week's Low Attendance", command=self.display_detention_list, style="Info.TButton")
        calc_button.pack(pady=10)

        # Style for the button
        style = ttk.Style()
        style.configure("Info.TButton", font=("times new roman", 12, "bold"), foreground="black", background="orange")
        style.map("Info.TButton", background=[('active', 'darkorange')])


        # Frame for the Treeview and Scrollbar
        tree_frame = Frame(detention_frame, bd=2, relief=RIDGE)
        tree_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

        # Scrollbar
        scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
        scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)

        # Treeview for displaying the list
        # --- MODIFIED: Changed column name from 'roll' to 'student_id' ---
        self.detention_table = ttk.Treeview(tree_frame,
                                            columns=("student_id", "name", "present", "total_days", "percentage"),
                                            yscrollcommand=scroll_y.set,
                                            xscrollcommand=scroll_x.set)

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.detention_table.yview)
        scroll_x.config(command=self.detention_table.xview)

        # Define Headings
        # --- MODIFIED: Changed heading text for the first column ---
        self.detention_table.heading("student_id", text="Student ID")
        self.detention_table.heading("name", text="Student Name")
        self.detention_table.heading("present", text="Days Present")
        self.detention_table.heading("total_days", text="Total Days")
        self.detention_table.heading("percentage", text="Attendance %")

        self.detention_table['show'] = 'headings' # Show only headings, not the default first column

        # Define Column Widths
        # --- MODIFIED: Changed column identifier for width ---
        self.detention_table.column("student_id", width=120, anchor=CENTER) # Adjusted width slightly
        self.detention_table.column("name", width=250)
        self.detention_table.column("present", width=100, anchor=CENTER)
        self.detention_table.column("total_days", width=100, anchor=CENTER)
        self.detention_table.column("percentage", width=120, anchor=CENTER)

        self.detention_table.pack(fill=BOTH, expand=True)

    # --- Functions for Detention List ---

    def get_last_week_dates(self):
        """Calculates the start (Monday) and end (Friday) dates of the previous week."""
        today = datetime.today().date()
        # Go back to the beginning of the current week (Monday is 0, Sunday is 6)
        start_of_current_week = today - timedelta(days=today.weekday())
        # Go back one more week to get the start of the last week
        start_of_last_week = start_of_current_week - timedelta(days=7)
        # End of last week is Friday (4 days after Monday)
        end_of_last_week = start_of_last_week + timedelta(days=4)
        return start_of_last_week, end_of_last_week

    def calculate_attendance(self, start_date, end_date):
        """
        Reads attendance CSVs for the given date range, calculates percentages,
        and returns a list of students below the threshold.
        Uses 'Student ID' as the identifier.
        """
        # Dictionary: {student_id: {'name': name, 'present': count}}
        attendance_data = {}
        report_folder = "." # Assuming CSVs are in the current directory. Change if needed.

        dates_in_range = []
        current_date = start_date
        while current_date <= end_date:
            # Only consider weekdays (Monday=0 to Friday=4) for processing attendance files
            if current_date.weekday() < 5:
                 dates_in_range.append(current_date)
            current_date += timedelta(days=1)

        print(f"Checking for attendance files for dates: {sorted([d.strftime('%Y-%m-%d') for d in dates_in_range])}") # Debug print

        actual_days_processed = set() # Keep track of dates for which we found data

        for report_date in dates_in_range:
            file_name = f"attendance_{report_date.strftime('%Y-%m-%d')}.csv"
            file_path = os.path.join(report_folder, file_name)

            print(f"Attempting to read: {file_path}") # Debug print

            if os.path.exists(file_path):
                print(f"File found: {file_path}") # Debug print
                try:
                    with open(file_path, 'r', newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        print(f"Headers in {file_name}: {reader.fieldnames}") # Debug print

                        # --- FIX: Check for "Student ID" header ---
                        if 'Student ID' not in reader.fieldnames or 'Name' not in reader.fieldnames or 'Status' not in reader.fieldnames:
                             print(f"Warning: Skipping {file_name} - missing required columns (Student ID, Name, Status). Fieldnames found: {reader.fieldnames}")
                             continue # Skip file if columns are missing

                        actual_days_processed.add(report_date) # Count this day as processed
                        print(f"Processed data for date: {report_date.strftime('%Y-%m-%d')}. Total processed dates so far: {len(actual_days_processed)}") # Debug print


                        for row in reader:
                            # --- FIX: Get data using "Student ID" key ---
                            student_id = row.get('Student ID')
                            name = row.get('Name')
                            status = row.get('Status', '').strip().lower()

                            # print(f"  Processing row: Student ID={student_id}, Name={name}, Status={status}") # More verbose debug print

                            if not student_id: # Skip rows without a student ID
                                print(f"Skipping row in {file_name}: No Student ID found.")
                                continue

                            # Use student_id as the key in the dictionary
                            if student_id not in attendance_data:
                                attendance_data[student_id] = {'name': name, 'present': 0}

                            # Update name if it's different (take the latest one encountered)
                            attendance_data[student_id]['name'] = name

                            if status == 'present':
                                attendance_data[student_id]['present'] += 1
                                # print(f"  Student ID {student_id}: Status is 'present'. Present count is now {attendance_data[student_id]['present']}") # More verbose debug print

                except Exception as e:
                    print(f"ERROR reading {file_name}: {e}")
            else:
                 print(f"Info: Attendance file not found for {report_date.strftime('%Y-%m-%d')}") # Debug print for missing files


        print("\n--- Finished reading files ---") # Debug print
        print(f"Actual dates with data found: {sorted([d.strftime('%Y-%m-%d') for d in list(actual_days_processed)])}") # Debug print
        total_days_with_data = len(actual_days_processed)
        print(f"Total days processed with data: {total_days_with_data}") # Debug print
        print("Aggregated attendance data before percentage calculation:") # Debug print
        for student_id, data in attendance_data.items():
             print(f"  Student ID {student_id}: Name={data['name']}, Days Present={data['present']}")


        detention_list = []

        if total_days_with_data == 0:
            print("No attendance data found for the last week.")
            return [] # Return empty list if no data was found

        for student_id, data in attendance_data.items(): # Iterate using student_id as key
            days_present = data['present']
            # Calculate percentage based on the number of days data was actually found
            percentage = (days_present / total_days_with_data) * 100 # if total_days_with_data > 0 else 0 # Handled by the if check above

            print(f"Calculating percentage for Student ID {student_id} ({data['name']}): Present={days_present}, Total Processed Days={total_days_with_data}, Percentage={percentage:.2f}%") # Debug print

            if percentage < 75:
                print(f"  --> Adding {data['name']} (Student ID {student_id}) to detention list.") # Debug print
                detention_list.append({
                    'student_id': student_id, # Use 'student_id' key to match Treeview
                    'name': data['name'],
                    'present': days_present,
                    'total_days': total_days_with_data,
                    'percentage': round(percentage, 2) # Round to 2 decimal places
                })

        # Sort list by percentage (lowest first) or by name/student_id
        detention_list.sort(key=lambda x: x['percentage'])

        print(f"\nFinal Detention List Count: {len(detention_list)}") # Debug print
        return detention_list

    def display_detention_list(self):
        """Fetches and displays the detention list in the Treeview."""
        # Clear existing data
        for item in self.detention_table.get_children():
            self.detention_table.delete(item)

        try:
            start_date, end_date = self.get_last_week_dates()
            print(f"Calculating attendance for week: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}") # Debug print

            detention_students = self.calculate_attendance(start_date, end_date)

            if not detention_students:
                messagebox.showinfo("Attendance Alert", f"No students found with less than 75% attendance for the week {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.", parent=self.root)
                print("Detention list is empty. Showing info message.") # Debug print
                return

            # Populate the table
            print("Populating Treeview with detention students...") # Debug print
            for student in detention_students:
                # --- MODIFIED: Use 'student_id' key to get the value ---
                self.detention_table.insert("", END, values=(
                    student['student_id'],
                    student['name'],
                    student['present'],
                    student['total_days'],
                    f"{student['percentage']}%" # Add % sign for display
                ))
            print(f"Successfully populated Treeview with {len(detention_students)} students.") # Debug print

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating attendance: {e}", parent=self.root)
            print(f"Error details: {e}") # Debug print the error

# Example of how to run this window independently (for testing)
if __name__ == "__main__":
    root = Tk()
    obj = Developer(root)
    root.mainloop()