import spacy
import tkinter as tk
from PIL import Image, ImageTk

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Create a Tkinter window
window = tk.Tk()
window.title("QuantumBytePanda")

# Set the window size and make it non-resizable
window.geometry("500x700")
window.resizable(False, False)

# Create a banner at the top of the window
banner_label = tk.Label(window, text="***Authorized Personel Only***", bg="lightblue", fg="white", font=("Arial", 14, "bold"), padx=10, pady=5)
banner_label.pack(fill=tk.X)

# Create a frame to hold the chat bubbles
chat_frame = tk.Frame(window, bg="white")
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a profile picture for the chatbot
chatbot_image = Image.open("profile_picture.png")
chatbot_image = chatbot_image.resize((50, 50), Image.ANTIALIAS)
chatbot_photo = ImageTk.PhotoImage(chatbot_image)

# Create a profile picture for the user input
user_image = Image.open("user_profile_picture.png")
user_image = user_image.resize((50, 50), Image.ANTIALIAS)
user_photo = ImageTk.PhotoImage(user_image)

# Define a function to process user input and generate a response
def get_chatbot_response():
    user_input = user_input_entry.get()
    # Perform language processing on the user input
    doc = nlp(user_input)

    # Process the user input and generate a response
    # You can implement your own logic or use pre-defined rules
    response = "Hello! I'm a chatbot."

    # Display the user input and the chatbot response in the chat history
    user_chat_frame = tk.Frame(chat_frame, bg="white")
    user_chat_frame.pack(anchor="e", padx=10, pady=5)
    user_profile_label = tk.Label(user_chat_frame, image=user_photo)
    user_profile_label.pack(side="left", padx=(0, 5))
    user_message_label = tk.Label(user_chat_frame, text="Admin: " + user_input, bg="lightblue", wraplength=250, anchor="w", justify="left")
    #user_message_label = tk.Label(user_chat_frame, text=user_input, bg="lightblue", wraplength=250, anchor="w", justify="left")
    user_message_label.pack(side="left")

    chatbot_chat_frame = tk.Frame(chat_frame, bg="white")
    chatbot_chat_frame.pack(anchor="w", padx=10, pady=5)
    chatbot_profile_label = tk.Label(chatbot_chat_frame, image=chatbot_photo)
    chatbot_profile_label.pack(side="left", padx=(0, 5))
    chatbot_message_label = tk.Label(chatbot_chat_frame, text="ProjectOmega: " + response, bg="lightgreen", wraplength=250, anchor="w", justify="left")
    chatbot_message_label.pack(side="left")

    # Clear the user input entry
    user_input_entry.delete(0, tk.END)

# Create the user input entry box
input_frame = tk.Frame(window, bg="white")
input_frame.pack(fill=tk.X, padx=10, pady=10)
user_input_entry = tk.Entry(input_frame, width=68)
user_input_entry.pack(side=tk.LEFT)

# Create the send button
send_button = tk.Button(input_frame, text="  Send  ", command=get_chatbot_response)
send_button.pack(side=tk.LEFT, padx=15)

# Run the Tkinter event loop
window.mainloop()
