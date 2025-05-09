import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def install_dependencies():
    try:
        print("Installing required packages...")
        # Install regular OpenCV
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow', 'opencv-python'])
        # Install OpenCV contrib which contains face recognition modules
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-contrib-python'])
        print("All dependencies installed successfully.")
        return True
    except Exception as e:
        print(f"Failed to install dependencies: {e}")
        return False

def run_application():
    try:
        # Create the root window
        root = tk.Tk()
        root.geometry("1530x790+0+0")
        root.title("Face Recognition System")
        
        # Create a message label
        message = tk.Label(root, text="Face Recognition Attendance System", 
                          font=("times new roman", 30, "bold"), bg="white", fg="blue")
        message.pack(fill=tk.X, pady=20)
        
        # Add a message about database configuration
        instructions = tk.Label(root, text="Database Configuration Required", 
                                font=("times new roman", 16), fg="red")
        instructions.pack(pady=10)
        
        details = tk.Label(root, text="This system requires MySQL database setup before full functionality can be used.\n"
                                  "Please make sure MySQL is installed and set up with the following:\n"
                                  "1. Create a database named 'sys'\n"
                                  "2. Update the MySQL connection details in the code files\n"
                                  "Current connection parameters in the code:\n"
                                  "Host: localhost\n"
                                  "User: root\n"
                                  "Password: wani321\n"
                                  "Database: sys",
                          font=("times new roman", 12), justify=tk.LEFT)
        details.pack(pady=20)
        
        # Add a note about OpenCV contrib
        cv_note = tk.Label(root, text="This system also requires OpenCV with contrib modules for face recognition.\n"
                                 "Run 'pip install opencv-contrib-python' if face recognition features don't work.",
                          font=("times new roman", 12), fg="blue")
        cv_note.pack(pady=20)
        
        # Exit button
        exit_btn = tk.Button(root, text="Exit", command=root.destroy, 
                            font=("times new roman", 15, "bold"), bg="red", fg="white",
                            width=15, height=2)
        exit_btn.pack(pady=30)
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error running application: {e}")
        
if __name__ == "__main__":
    if install_dependencies():
        run_application() 