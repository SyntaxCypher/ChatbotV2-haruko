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
chatbot_image = chatbot_image.resize((200, 200), Image.ANTIALIAS)
chatbot_photo = ImageTk.PhotoImage(chatbot_image)

chatbot_photo_label = tk.Label(window, image=chatbot_photo)
chatbot_photo_label.pack()

# Create a frame for the chat history
chat_history_frame = tk.Frame(window)
chat_history_frame.pack()

# Create a canvas for the chat history text area
chat_history_canvas = tk.Canvas(chat_history_frame, width=300, height=300)
chat_history_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar to the chat history canvas
chat_history_scrollbar = tk.Scrollbar(chat_history_frame, orient=tk.VERTICAL, command=chat_history_canvas.yview)
chat_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas scrolling
chat_history_canvas.configure(yscrollcommand=chat_history_scrollbar.set)
chat_history_canvas.bind('<Configure>', lambda e: chat_history_canvas.configure(scrollregion=chat_history_canvas.bbox("all")))

# Create a frame inside the canvas to hold the chat history text area
chat_history_inner_frame = tk.Frame(chat_history_canvas)
chat_history_canvas.create_window((0, 0), window=chat_history_inner_frame, anchor=tk.NW)

# Create the user input entry field
user_input_entry = tk.Entry(window, width=40)
user_input_entry.pack(side=tk.BOTTOM, padx=10, pady=10)

# Define a function to process user input and generate a response
def get_chatbot_response():
    user_input = user_input_entry.get()
    # Perform language processing on the user input
    doc = nlp(user_input)

    # Process the user input and generate a response
    # You can implement your own logic or use pre-defined rules
    response = "Hello! I'm a chatbot."

    # Display the user input as a chat bubble in the chat history
    user_input_bubble = tk.Label(chat_history_inner_frame, text=user_input, bg='lightblue', wraplength=200, padx=10, pady=5, anchor=tk.W, justify=tk.LEFT)
    user_input_bubble.pack(anchor=tk.W, padx=10, pady=5)

    # Display the response as a chat bubble in the chat history
    response_bubble = tk.Label(chat_history_inner_frame, text=response, bg='lightgreen', wraplength=200, padx=10, pady=5, anchor=tk.W, justify=tk.LEFT)
    response_bubble.pack(anchor=tk.W, padx=10, pady=5)

    # Clear the user input entry
    user_input_entry.delete(0, tk.END)

    # Update the scrollbar position
    chat_history_canvas.yview_moveto(1.0)

# Create the send button
send_button = tk.Button(window, text="Send", command=get_chatbot_response, width=10)
send_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Run the Tkinter event loop
window.mainloop()
