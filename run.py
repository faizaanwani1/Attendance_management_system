import os
import sys
import subprocess

def install_dependencies():
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("All dependencies installed successfully.")
        return True
    except Exception as e:
        print(f"Failed to install dependencies: {e}")
        return False

def run_application():
    try:
        print("Starting Face Recognition System...")
        import main
        root = main.Tk()
        obj = main.Face_Recognition_System(root)
        root.mainloop()
    except Exception as e:
        print(f"Error running application: {e}")
        
if __name__ == "__main__":
    if install_dependencies():
        run_application() 