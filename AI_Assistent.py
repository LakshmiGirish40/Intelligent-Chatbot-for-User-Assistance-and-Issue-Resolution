import openai
import os
import json
import uuid
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to interact with GPT-3/4 using the new API interface
def General_Chat(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" or "gpt-4"
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"
    
  #========================================================================  
  #Create Folder Save the each session chat history in .txt format
def get_next_filename(folder_path, base_name, extension):
    """
    Generate the next available filename in the sequence.
    Example: text1.txt, text2.txt, ...
    """
    i = 1
    while True:
        file_name = f"{base_name}{i}.{extension}"
        file_path = os.path.join(folder_path, file_name)
        if not os.path.exists(file_path):
            return file_path
        i += 1

# Function to save chat history to a file
def save_chat_history(chat_history, file_name="chat_history"):
    folder_path = "Chatbot_Python/Chat_Histories"
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
      # Generate the next available filename
    file_path = get_next_filename(folder_path, base_name="text", extension="txt")

    # Save chat history to the file in plain text format
    with open(file_path, "w") as file:
        for entry in chat_history:
            if isinstance(entry, dict) and "User" in entry and "Bot" in entry:
                if entry["role"] == "user":
                    file.write(f"User: {entry['content']}\n")
                elif entry["role"] == "bot":
                    file.write(f"Bot: {entry['content']}\n")
            else:
                file.write(f"Chat History: {entry}\n\n")

    print(f"Chat history saved to: {file_path}")
    
     

#========================================================================================
# Function to raise an issue and save the Raising Issues


def raise_issue():
    print("Sure, I'd be happy to help. Please provide more information about the issue.")
    name = input("Please enter your name: ")
    email = input("Please enter your email: ")
    description = input("Please describe the issue: ")

    token_id = str(uuid.uuid4())  # Generate a unique token ID
    issue_details = {
        "Name": name,
        "Email": email,
        "Issue Description": description,
        "Token ID": token_id,
    }

#=========================================================================================
    #Create a Folder and save the Raised Issues
    folder_path = 'Chatbot_Python/Issues_Record'
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    # file_path = os.path.join(folder_path, 'issues.json')
    # Generate a unique filename using the timestamp
    # Generate a timestamp for the file
   # Generate a unique filename using the timestamp for better organization
    file_name = f"issue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join(folder_path, file_name)
    file_path = os.path.join(folder_path, file_name)

    # Save the issue details
    with open(file_path, 'w') as file:
        json.dump(issue_details, file, indent=4)
        file.write("\n")  # Add a newline between entries

    print("\nYour issue has been raised successfully! Here are the details:")
    print(f"Token ID: {token_id}")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Description: {description}")

#===============================================================================================
# Main chatbot function
def chatbot():
    print("Welcome to the chatbot! Type 'raise issue' to report a problem or 'exit' to end the chat.")
    chat_history = []

    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            print("Ending the conversation. Goodbye!")
            save_chat_history(chat_history)
            break
        elif user_message.lower() == "raise issue":
            raise_issue()
        else:
            # Get bot response
            bot_response = General_Chat(user_message)
            print(f"Bot: {bot_response}")

            # Add messages to chat history
            chat_history.append({"role": "user", "content": user_message})
            chat_history.append({"role": "bot", "content": bot_response})
            
#=================================================================================
#Accessing Books and Novels (via API)
#You can use the Open Library API or Google Books API to fetch book data.
#Example with Google Books API:

import requests

def get_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
    response = requests.get(url)
    
    if response.status_code == 200:
        books = response.json().get('items', [])
        for book in books:
            title = book['volumeInfo'].get('title', 'No Title')
            authors = book['volumeInfo'].get('authors', ['No Authors'])
            print(f"Title: {title}, Authors: {', '.join(authors)}")
    else:
        print(f"Error fetching books: {response.status_code}")

# Get a list of books about Python programming
get_books("python programming")

#=========================================================

# #Accessing Weather Forecasts (via API)

# import requests

# def get_weather_forecast(city):
#     api_key = 'your_openweathermap_api_key'  # Get it from https://openweathermap.org/api
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#         city_name = data['name']
#         temperature = data['main']['temp']
#         weather_description = data['weather'][0]['description']
#         print(f"The current weather in {city_name}: {temperature}°C, {weather_description}")
#     else:
#         print(f"Error fetching weather: {response.status_code}")

# # Get weather forecast for a city
# get_weather_forecast("New York")


# #=======================================================================================
# #Accessing Movie List (via API)
# import requests

# def get_movies(query):
#     api_key = 'your_tmdb_api_key'  # Get it from https://www.themoviedb.org/settings/api
#     url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&page=1"
    
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         movies = response.json().get('results', [])
#         for movie in movies:
#             title = movie['title']
#             release_date = movie.get('release_date', 'No Release Date')
#             print(f"Title: {title}, Release Date: {release_date}")
#     else:
#         print(f"Error fetching movies: {response.status_code}")

# # Get a list of action movies
# get_movies("action")



#===================================================================================





if __name__ == "__main__":
    chatbot()


#=============================================================