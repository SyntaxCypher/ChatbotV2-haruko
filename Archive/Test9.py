import spacy
import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from transformers import pipeline, AutoTokenizer, SquadExample

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Create a Tkinter window
window = tk.Tk()
window.title("QuantumBytePanda")

# Set the window size and make it non-resizable
window.geometry("500x700")
window.resizable(False, False)

# Create a banner at the top of the window
banner_label = tk.Label(
    window,
    text="***Authorized Personnel Only***",
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
    cursor.execute(
        """
        INSERT INTO chat (user_input, chatbot_response)
        VALUES (?, ?)
        """,
        (user_input, chatbot_response),
    )
    conn.commit()

# Load the question-answering model
tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = "facebook/blenderbot-400M-distill"


def example_to_dict(example):
    return {
        "question": example.question_text,
        "context": example.context_text,
        "qas_id": example.qas_id,
        "title": example.title,
        "answers": [
            {
                "text": example.answer_text,
                "answer_start": example.answer_start,
            }
        ],
    }

def generate_chatbot_response(user_input):
    # Define the start_position_character and char_to_word_offset variables
    start_position_character = 0  # Update with the appropriate value
    char_to_word_offset = []  # Update with the appropriate value

    # Check if the user input contains a question
    if "?" in user_input:
        # Create a SquadExample object with the user input as the question
        example = SquadExample(
            qas_id="1",
            question_text=user_input,
            context_text="",
            answer_text="",
            start_position_character=min(start_position_character, len(char_to_word_offset) - 1),
            title=""
        )
        # Convert the SquadExample object to a dictionary
        example_dict = example_to_dict(example)
        # Generate an answer using the question-answering pipeline
        answer = pipeline("question-answering", model=model, tokenizer=tokenizer)(example_dict)
        response = answer["answer"]
    else:
        # Process the user input using the spaCy pipeline
        doc = nlp(user_input)

        # Retrieve the named entities from the user input
        entities = [ent.text for ent in doc.ents]

        # If named entities are found, generate a response based on them
        if entities:
            # Process the named entities and generate a response
            response = f"I see that you mentioned {', '.join(entities)}. Could you please provide more details?"
        else:
            response = "I'm sorry, I didn't understand. Can you please rephrase your statement?"

    return response

# Define a function to process user input and generate a response
def get_chatbot_response():
    user_input = user_input_entry.get()

    # Generate a contextually appropriate response
    response = generate_chatbot_response(user_input)

    # Insert the user input and the chatbot response into the database
    insert_chat_entry(user_input, response)

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
        text="ProjectOmega: " + response,
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

    # Clear the user input entry
    user_input_entry.delete(0, tk.END)

# ... rest of the code ...

# Create the user input entry box
input_frame = tk.Frame(window, bg="white")
input_frame.pack(fill=tk.X, padx=10, pady=10)
user_input_entry = tk.Entry(input_frame, width=68)
user_input_entry.pack(side=tk.LEFT)

# Create the send button
send_button = tk.Button(input_frame, text="  Send  ", command=get_chatbot_response)
send_button.pack(side=tk.LEFT, padx=15)

# Retrieve the chat history from the database
cursor.execute("SELECT user_input, chatbot_response FROM chat")
chat_history = cursor.fetchall()

# Update the chat window with the chat history
for user_input, chatbot_response in chat_history:
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
        text="ProjectOmega: " + chatbot_response,
        bg="lightgreen",
        wraplength=380,
        anchor="w",
        justify="left",
    )
    chatbot_message_label.pack(side="left")

# Update the scroll region to include the chat history
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Scroll to the bottom of the chat frame
canvas.yview_moveto(1.0)

# Start the Tkinter event loop
window.mainloop()
