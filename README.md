# Jessup Cellars Chatbot

This project is a chatbot designed to assist users with information about Jessup Cellars winery. The chatbot uses a combination of LangChain, Cohere, and Chroma for context retrieval and response generation. The frontend is a simple HTML/JavaScript interface for interacting with the chatbot, and the backend is built using Flask.

# Table of Contents
1. Features
2. Prerequisites
3. Setup
4. Running the Backend
5. Running the Frontend
6. Using the Chatbot
7. Project Structure
8. Contributing
9. License

# FEATURES:

1) Answer questions based on a provided corpus of PDF documents.
2) Handle out-of-scope queries by directing users to contact the business directly.
3) Maintain conversation history and context.
4) Stream responses for a better user experience.

# Prerequisites:

Python 3.8+

a) pip (Python package installer)

b) Flask

c) Flask-CORS

d) Spacy

e) Cohere API key

# Setup:

1. Clone the repository:

git clone https://github.com/carefreecherry/Wine-ChatBot

Edit the 3 Paths in the Chatbot.py file:

1st=function add_to_chroma #Right Click on the ChromaDB folder and click on Copy path

2nd=function get_chrome #Right Click on the ChromaDB folder and click on Copy path

3rd=fuction load_document #Right Click on the PDF folder and click on Copy path

2. Get the Cohere API Key:
   
Sign Up on https://cohere.com/

You will find a Button Called API Keys

Copy it and paste it in function get_response_stream of ChatBot.py

3. Set up a virtual environment:
   
python -m venv .venv

source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

'''if error occurs while `.venv\Scripts\activate` then follow the below steps:
1) Open PowerShell as an Administrator: Right-click on the Start button and select "Windows PowerShell (Admin)" or "Windows Terminal (Admin)".
2) Check the current execution policy by running the following command:
Get-ExecutionPolicy
3) Change the execution policy to allow scripts to run. You can choose between different levels:

a) RemoteSigned: Allows scripts created on your machine to run, and scripts downloaded from the internet must be signed by a trusted publisher.
Set-ExecutionPolicy RemoteSigned

OR

b) Unrestricted: Allows all scripts to run.
To set the execution policy to RemoteSigned, run:
Set-ExecutionPolicy Unrestricted

4) You may be prompted to confirm the change. Type Y and press Enter to confirm.

5)After changing the execution policy, run the below command on your terminal:
.venv\Scripts\Activate'''

# Install the required packages:
Check your Python version >=3.8.0

pip install Flask
pip install Flask-CORS
pip install langchain
pip install langchain_huggingface
pip install langchain_community
pip install cohere
pip install spacy
pip install pypdf
pip install chromadb
python -m spacy download en_core_web_sm

# Running the Backend
Ensure your Chroma database is populated:

Uncomment the last lines in chatbot.py to create and populate the Chroma database from your PDF documents, then run the script once:

*'''Uncomment the following lines to create and populate the Chroma database from PDFs*

*documents = load_documents()*

*chunks = split_documents(documents)*

*print(chunks[0])*

*add_to_chroma(chunks)'''*

run python chatbot.py

'''if error while running the chatbot.py:

persist_directory = "Path\to\ChromaDB"
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape

then

persist_directory = r"Path\to\ChromaDB" '''

After running Chatbot.py successfully, comment those 4 line again

Run the Flask application:

python app.py

The backend will start on http://127.0.0.1:5000.

# Running the Frontend

Open the index.html file:

Open the index.html file in a web browser. This file is located in the root of the project directory.

# Using the Chatbot
Type a message: Enter your message in the input field at the bottom of the page.

Send the message: Click the "Send" button or press "Enter".

View the response: The chatbot's response will appear in the chat window.

# Project Structure

wine-chatbot/

├── ChromaDB/                        # Chroma database directory

├── PDF/                             # PDF documents directory

│   ├── Corpus.pdf                   # Example PDF file

├── wine_chatbot_backend/venv/       # Virtual environment directory

│   ├── ...

│   ├──chatbot.py                     # Main chatbot logic

│   ├──app.py                         # Flask backend application

├── wine_chatbot_frontend

│   ├──index.html                     # Frontend HTML file

├── README.md                         # This README file

├── Wine_chatbot.pdf                   # This PDF file

├── Working.mp4                       # This is Video

# Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

# License
This project is licensed under the MIT License.
