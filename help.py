from tkinter import *
from tkinter import ttk, scrolledtext # Added scrolledtext import
from PIL import Image, ImageTk
# Removed unused imports like messagebox, mysql.connector, cv2 if not needed elsewhere in this file

class Help:
    def __init__(self, root):
        """
        Initializes the Help Desk window with an integrated chatbot.

        Args:
            root: The Tkinter Toplevel window for the Help Desk.
        """
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Help Desk & Chatbot") # Updated title

        # --- Top Title ---
        title_lbl = Label(self.root, text="HELP DESK", font=("times new roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # --- Background Image ---
        try:
            # Ensure the image path is correct
            # Use forward slashes or os.path.join for better cross-platform compatibility
            image_path = "college_images/1_5TRuG7tG0KrZJXKoFtHlSg.jpeg"
            img_top = Image.open(image_path)
            img_top = img_top.resize((1530, 720), Image.Resampling.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)

            # Label to hold the background image
            f_lbl = Label(self.root, image=self.photoimg_top)
            f_lbl.place(x=0, y=55, width=1530, height=720) # Covers the area below the title

            # --- Chatbot UI Elements (Placed on top of f_lbl) ---

            # Frame to contain the chatbot elements for better positioning
            # Position this frame on the left side
            chatbot_frame = Frame(f_lbl, bg='#E0E0E0', bd=2, relief=RIDGE) # Light grey background, subtle border
            chatbot_frame.place(x=50, y=50, width=450, height=600) # Adjust x, y, width, height as needed

            # Chatbot Title within its frame
            chat_title = Label(chatbot_frame, text="Help Assistant", font=("times new roman", 18, "bold"), fg="white", bg="#0078D7", pady=8)
            chat_title.pack(side=TOP, fill=X)

            # Conversation Area
            self.conversation_area = scrolledtext.ScrolledText(chatbot_frame, wrap=WORD, state='disabled',
                                                               font=("times new roman", 11), bg="#FFFFFF", fg="#333333",
                                                               bd=1, relief=SOLID)
            self.conversation_area.pack(pady=10, padx=10, expand=True, fill=BOTH)

            # Frame for Input and Send Button within chatbot_frame
            input_frame = Frame(chatbot_frame, bg='#E0E0E0') # Match chatbot_frame background
            input_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)

            # User Input Entry
            self.user_input = ttk.Entry(input_frame, font=("times new roman", 11), width=35)
            self.user_input.grid(row=0, column=0, padx=(0, 5), ipady=4, sticky="ew")
            self.user_input.bind("<Return>", self.send_message_event) # Bind Enter key

            # Send Button
            self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message, style="Send.TButton")
            self.send_button.grid(row=0, column=1, ipady=1)

            # Configure input_frame grid column weights
            input_frame.grid_columnconfigure(0, weight=1)

            # Style for the Send button (ensure ttk.Style is initialized if not already)
            style = ttk.Style()
            # --- MODIFIED: Changed foreground to black ---
            style.configure("Send.TButton", font=("times new roman", 11, "bold"), background="#0078D7", foreground="black")
            # --- END MODIFICATION ---
            style.map("Send.TButton", background=[('active', '#005a9e')]) # Keep hover effect

            # Initial greeting in chatbot
            self.add_to_conversation("Bot: Hello! How can I help you with the attendance system today?\nAsk questions like 'How to add a student?', 'How to take attendance?', etc.\n")

            # --- Original Email Label (Optional - keep or remove) ---
            # You can keep this on the right side or remove it if the chatbot replaces its function
            # email_label = Label(f_lbl, text="Email: wanifaizan53@gmail.com", font=("times new roman", 16, "bold"), fg="blue", bg="white")
            # email_label.place(x=900, y=100) # Example placement on the right

        except FileNotFoundError:
             # Handle error if background image is not found
             error_lbl = Label(self.root, text=f"Background image not found:\n{image_path}", font=("times new roman", 18), fg="red", bg="white")
             error_lbl.place(x=0, y=55, width=1530, height=720)
             # Optionally, create the chatbot frame directly on self.root if background fails
             # chatbot_frame = Frame(self.root, ...)
             # chatbot_frame.place(x=50, y=100, ...)
             # Add chatbot elements to this frame as above
        except Exception as e:
            # Handle other potential errors during initialization
             error_lbl = Label(self.root, text=f"An error occurred: {e}", font=("times new roman", 18), fg="red", bg="white")
             error_lbl.place(x=0, y=55, width=1530, height=720)


    # --- Chatbot Functions (Copied from ChatbotWindow) ---

    def add_to_conversation(self, message):
        """
        Adds a message to the conversation text area.
        """
        self.conversation_area.config(state='normal')
        self.conversation_area.insert(END, message + "\n")
        self.conversation_area.config(state='disabled')
        self.conversation_area.see(END) # Auto-scroll

    def send_message_event(self, event):
        """Handles sending message when Enter key is pressed."""
        self.send_message()

    def send_message(self):
        """
        Gets user input, finds a response, and updates the conversation.
        """
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.add_to_conversation(f"You: {user_text}")
        self.user_input.delete(0, END)

        bot_response = self.get_response(user_text.lower())
        self.add_to_conversation(f"Bot: {bot_response}")

    def get_response(self, query):
        """
        Provides a response based on predefined rules. (Same logic as before)
        """
        # Simple rule-based responses (keep this logic identical to chatbot.py)
        if "hello" in query or "hi" in query:
            return "Hello there! How can I assist you?"
        elif "add student" in query or "new student" in query:
            return "To add a new student, click the 'Student Details' button on the main screen, fill in the information, and click 'Save'. You can also take a photo sample from there."
        elif "take attendance" in query or "mark attendance" in query or "face recognition" in query or "face detector" in query:
            return "To take attendance, click the 'Face Detector' button. The system will use the camera to recognize faces and mark attendance automatically. Ensure you have trained the system first."
        elif "train" in query or "train data" in query:
            return "Click the 'Train Data' button to train the face recognition model with the student photos you've collected in the 'data' folder. This is necessary for accurate face detection."
        elif "view attendance" in query or "attendance report" in query:
            return "Click the 'Attendance' button to view and manage attendance records. You can import/export attendance data as CSV files."
        elif "student details" in query:
             return "Click the 'Student Details' button to view, add, update, or delete student information."
        elif "photos" in query or "view photos" in query or "data folder" in query:
            return "The 'Photos' button opens the 'data' folder where the captured face samples for each student are stored."
        elif "developer" in query:
            return "The 'Developer' button shows information about the creators of this application."
        elif "exit" in query:
            return "Use the 'Exit' button on the main screen to close the application."
        elif "help" in query: # Added specific response for help within help
            return "You are currently in the Help Desk. Ask me questions about using the system, like adding students or taking attendance."
        elif "thank you" in query or "thanks" in query:
            return "You're welcome! Let me know if you have more questions."
        elif "bye" in query:
            return "Goodbye! Have a great day."
        else:
            return "Sorry, I didn't quite understand that. Can you please rephrase? You can ask about adding students, taking attendance, training data, etc."

# Example of how to run this window independently (for testing)
if __name__ == "__main__":
    root = Tk()
    app = Help(root)
    root.mainloop()
