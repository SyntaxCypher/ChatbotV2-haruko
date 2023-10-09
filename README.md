# ChatbotV2-haruko

![CodeLogo4](https://github.com/QuantumBytePanda/ChatbotV2-haruko/assets/52766040/c7ebe686-8d19-4440-8ff8-7f65c5550e5f)

Welcome to Haruko Chatbot! Haruko is a simple chatbot built using Python and Tkinter that can chat with you and even respond using text-to-speech. This README will provide an overview of the code and explain how to run and use the chatbot.

## Table of Contents

- [Introduction](#introduction)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)

## Introduction

Haruko Chatbot is a Python-based chatbot that uses the Transformers library to generate responses. It utilizes the `BlenderbotForConditionalGeneration` model to generate chatbot responses based on user input. The chat history is stored in an SQLite database, and the chat interface is built using the Tkinter library. Additionally, Haruko supports text-to-speech functionality using the `pyttsx3` library.

## Dependencies

Before running Haruko Chatbot, make sure you have the following dependencies installed:

```
  pip install spacy
  pip install pillow
  pip install transformers
  pip install pyttsx3
  python -m spacy download en_core_web_sm
```
## Installation

To use Haruko Chatbot, follow these steps:

1. Clone this GitHub repository or download the code as a ZIP file.
2. Ensure that you have all the dependencies installed, as mentioned in the previous section.
3. Place your profile pictures (profile_picture.png for the chatbot and user_profile_picture.png for the user) in the same directory as the code.
4. Run the code by executing the haruko_chatbot.py script using Python:
5. Download a blenderbot model from https://huggingface.co/
```
python haruko_chatbot.py

```
## Usage
Once you've started Haruko Chatbot, you can interact with it in the following way:

1. Type your message in the input box at the bottom.
2. Click the "Send" button or press Enter to send your message to Haruko.
3. Haruko will respond with a message, and the conversation will be displayed in the chat window.
4. Messages are saved in an SQLite database, so you can view your chat history.
5. Haruko can also read her responses aloud if you uncomment the "Speak" button.

## Features
* Simple chatbot interface built with Tkinter.
* Text-to-speech functionality.
* Conversation history stored in an SQLite database.
* Uses the Blenderbot model for generating responses.
* Profile pictures for the chatbot and user.

## License
This project is licensed under the MIT License - see the LICENSE file for details

Copyright QuantumBytePanda 2023
