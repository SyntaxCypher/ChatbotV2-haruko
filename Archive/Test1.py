import spacy
import tkinter as tk
from PIL import Image, ImageTk

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Create a Tkinter window
window = tk.Tk()
window.title("Chatbot GUI")

# Set the window size for a mobile-like application
window.geometry("375x667")

# Load and display the profile picture for the chatbot
chatbot_image = Image.open("profile_picture.png")
chatbot_image = chatbot_image.resize((100, 100), Image.ANTIALIAS)
chatbot_photo = ImageTk.PhotoImage(chatbot_image)

chatbot_photo_label = tk.Label(window, image=chatbot_photo)
chatbot_photo_label.pack()

# Create the chat history text area
chat_history_text = tk.Text(window, width=50, height=10)
chat_history_text.pack()

# Create a frame for user input and send button
user_input_frame = tk.Frame(window)
user_input_frame.pack(side=tk.BOTTOM)

# Create the user input entry field
user_input_entry = tk.Entry(user_input_frame, width=40)
user_input_entry.grid(row=0, column=0, padx=10, pady=10)

# Define a function to process user input and generate a response
def get_chatbot_response():
    user_input = user_input_entry.get()
    # Perform language processing on the user input
    doc = nlp(user_input)

    # Process the user input and generate a response
    # You can implement your own logic or use pre-defined rules
    response = "Hello! I'm a chatbot."

    # Display the response in the chat window
    chat_history_text.insert(tk.END, "User: " + user_input + "\n")
    chat_history_text.insert(tk.END, "Chatbot: " + response + "\n")
    chat_history_text.insert(tk.END, "-------------------------\n")
    chat_history_text.see(tk.END)

    # Clear the user input entry
    user_input_entry.delete(0, tk.END)

# Create the send button
send_button = tk.Button(user_input_frame, text="Send", command=get_chatbot_response, width=10)
send_button.grid(row=0, column=1, padx=10, pady=10)

# Run the Tkinter event loop
window.mainloop()
