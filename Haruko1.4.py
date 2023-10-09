import spacy
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from transformers import BlenderbotForConditionalGeneration, BlenderbotTokenizer
import random
import pyttsx3

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Create a Tkinter window
window = tk.Tk()
window.title("Haruko Chatbot")

# Set the window size and make it non-resizable
window.geometry("500x700")
window.resizable(False, False)

# Create a banner at the top of the window
banner_label = tk.Label(
    window,
    text="***Copyright QuantumBytePanda 2023***",
    bg="lightblue",
    fg="white",
    font=("Arial", 14, "bold"),
    padx=10,
    pady=5,
)
banner_label.pack(fill=tk.X)

# Create a frame to hold the chat bubbles
chat_frame = tk.Frame(window, bg="white")
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a canvas to hold the chat frame
canvas = tk.Canvas(chat_frame, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scroll bar for the chat frame
scrollbar = tk.Scrollbar(chat_frame, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to use the scroll bar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame to hold the chat bubbles within the canvas
chat_bubbles_frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=chat_bubbles_frame, anchor="nw")

# Load the profile pictures
chatbot_image = Image.open("profile_picture.png")
chatbot_image = chatbot_image.resize((50, 50), Image.LANCZOS)
chatbot_photo = ImageTk.PhotoImage(chatbot_image)

user_image = Image.open("user_profile_picture.png")
user_image = user_image.resize((50, 50), Image.LANCZOS)
user_photo = ImageTk.PhotoImage(user_image)

# Connect to the SQLite database
conn = sqlite3.connect("chat_history.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        chatbot_response TEXT
    )
    """
)
conn.commit()

# Define a function to insert a chat entry into the database
def insert_chat_entry(user_input, chatbot_response):
    # Remove </s> artifact from chatbot response
    chatbot_response = chatbot_response.replace("</s>", "").strip()

    cursor.execute(
        """
        INSERT INTO chat (user_input, chatbot_response)
        VALUES (?, ?)
        """,
        (user_input, chatbot_response),
    )
    conn.commit()

# Load the Blenderbot model and tokenizer
model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set the voice to a female voice

# Define a function to process user input and generate a response
def get_chatbot_response():
    user_input = user_input_entry.get()

    # Encode the user input
    user_input_ids = tokenizer.encode(user_input, return_tensors="pt")

    # Check if the user asked for the chatbot's name
    if "name" in user_input.lower():
        chatbot_response = "You can call me Haruko."
    else:
        # Check if user asked for System Admin Name
        if "define" in user_input.lower() and ("admin" in user_input.lower()):
            chatbot_response = "The System Admin's name is Seth"
            response = None  # Assigning a default value to response
        else:
            # Generate a response from the model
            chatbot_response_ids = model.generate(
                user_input_ids,
                max_length=1000,
                num_return_sequences=1,
                no_repeat_ngram_size=3,
                do_sample=True,
                temperature=0.7,
            )
            chatbot_response = tokenizer.decode(chatbot_response_ids[0], skip_special_tokens=True)

        # Remove any artifacts from the chatbot response
        chatbot_response = chatbot_response.replace("</s>", "").strip()

        # Save the chat entry in the database
        insert_chat_entry(user_input, chatbot_response)
        
    # Display the user input and the chatbot response in the chat history
    user_chat_frame = tk.Frame(chat_bubbles_frame, bg="white")
    user_chat_frame.pack(anchor="e", padx=(10, 80), pady=5)
    user_profile_label = tk.Label(user_chat_frame, image=user_photo)
    user_profile_label.pack(side="left", padx=(0, 5))
    user_message_label = tk.Label(
        user_chat_frame,
        text="Admin: " + user_input,
        bg="lightblue",
        wraplength=380,
        anchor="e",
        justify="right",
    )
    user_message_label.pack(side="right", expand=True, fill="both")

    chatbot_chat_frame = tk.Frame(chat_bubbles_frame, bg="white")
    chatbot_chat_frame.pack(anchor="w", padx=10, pady=5)
    chatbot_profile_label = tk.Label(chatbot_chat_frame, image=chatbot_photo)
    chatbot_profile_label.pack(side="left", padx=(0, 5))
    chatbot_message_label = tk.Label(
        chatbot_chat_frame,
        text="Haruko: " + chatbot_response,
        bg="lightgreen",
        wraplength=380,
        anchor="w",
        justify="left",
    )
    chatbot_message_label.pack(side="left")

    # Update the scroll region to include the new chat bubbles
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Scroll to the bottom of the chat frame
    canvas.yview_moveto(1.0)

    # Read the chatbot response aloud after a delay
    window.after(1000, lambda: speak(chatbot_response))

    # Clear the user input entry
    user_input_entry.delete(0, tk.END)
    
# Function to speak the given text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Create the user input entry box
input_frame = tk.Frame(window, bg="white")
input_frame.pack(fill=tk.X, padx=10, pady=10)
user_input_entry = tk.Entry(input_frame, width=68)
user_input_entry.pack(side=tk.LEFT)

# Create the send button
send_button = tk.Button(input_frame, text="  Send  ", command=get_chatbot_response)
send_button.pack(side=tk.LEFT, padx=15)

# Create a button to speak the user input
#speak_button = tk.Button(window, text="Speak", font=("Arial", 14), command=lambda: speak(user_input_entry.get()))
#speak_button.pack(pady=5)

# Retrieve the chat history from the database
cursor.execute("SELECT user_input, chatbot_response FROM chat")
chat_history = cursor.fetchall()

# Update the chat window with the chat history
for user_input, chatbot_response in chat_history:
    # Remove </s> artifact from chatbot response
    chatbot_response = chatbot_response.replace("</s>", "").strip()

    # Display the user input and the chatbot response in the chat history
    user_chat_frame = tk.Frame(chat_bubbles_frame, bg="white")
    user_chat_frame.pack(anchor="e", padx=(10, 80), pady=5)
    user_profile_label = tk.Label(user_chat_frame, image=user_photo)
    user_profile_label.pack(side="right", padx=(0, 5))
    user_message_label = tk.Label(
        user_chat_frame,
        text="Admin: " + user_input,
        bg="lightblue",
        wraplength=380,
        anchor="e",
        justify="left",
    )
    user_message_label.pack(side="right", expand=True, fill="both")

    chatbot_chat_frame = tk.Frame(chat_bubbles_frame, bg="white")
    chatbot_chat_frame.pack(anchor="w", padx=10, pady=5)
    chatbot_profile_label = tk.Label(chatbot_chat_frame, image=chatbot_photo)
    chatbot_profile_label.pack(side="left", padx=(0, 5))
    chatbot_message_label = tk.Label(
        chatbot_chat_frame,
        text="Haruko: " + chatbot_response,
        bg="lightgreen",
        wraplength=380,
        anchor="w",
        justify="left",
    )
    chatbot_message_label.pack(side="left")

# Update the scroll region to include the new chat bubbles
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Scroll to the bottom of the chat frame
canvas.yview_moveto(1.0)

# Start the Tkinter event loop
window.mainloop()

# Close the SQLite connection
conn.close()
