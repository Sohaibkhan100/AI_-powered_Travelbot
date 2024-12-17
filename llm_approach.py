
# import google.generativeai as genai
# import requests
# import json

# def send_to_api(intent_json):
#     api_url = "http://localhost:8000/v1/search/globalsearch"
#     headers = {"Content-Type": "application/json"}
    
#     response = requests.post(api_url, json=intent_json, headers=headers)
    
#     if response.status_code == 200:
#         # print("API Response:", response.json())
#         get_naturalresponse_and_details(response.json())

#     else:
#         print(f"Error: {response.status_code} - {response.text}")

# genai.configure(api_key="AIzaSyD3D2FdD7AK3gT8wjqekH-AKWSDeeC76Yw")

# instructions = """
# You are an expert intent recognition model. Your task is to identify intents from user queries related to travel services and extract key details.

# However, if the query is unrelated to travel services (e.g., fashion, clothing, beauty), you must respond by stating:
# "I am a fashion assistant, I don’t have knowledge other than this domain. Sorry, but I can help you in matters related to travel."

# Instructions:
# 1. Identify intents from user queries.
# 2. The supported intents are: Hotel_search, Flight_search, Tour_search, and Transfer_search.
# 3. Analyze the query and extract details for each intent as follows:

# Intent Details:
# - Hotel_search:
#    - location: City or place mentioned in the query.
#    - budget: The price mentioned, in numeric format (default to null if not provided).
   
# - Flight_search:
#    - schedules: Date of the flight (default to null if not mentioned).
#    - stepover: Stopover location (default to null if not mentioned).
#    - budget: The price mentioned, in numeric format (default to null if not provided).
   
# - Tour_search:
#    - budget: The price mentioned, in numeric format (default to null if not provided).

# - Transfer_search:
#    - schedules: Date of the transfer (default to null if not provided).
#    - from: Starting location (default to null if not provided).
#    - to: Destination location (default to null if not provided).
#    - budget: The price mentioned, in numeric format (default to null if not provided).

# Response Format:
# {
#   "intentType": ["<Intent1>", "<Intent2>", ...],
#   "Hotel_search": {
#     "location": "<location>",
#     "budget": <budget>
#   },
#   "Flight_search": {
#     "schedules": "<schedules>",
#     "stepover": "<stepover>",
#     "budget": <budget>
#   },
#   "Tour_search": {
#     "budget": <budget>
#   },
#   "Transfer_search": {
#     "schedules": "<schedules>",
#     "from": "<from>",
#     "to": "<to>",
#     "budget": <budget>
#   }
# }

# Guidelines:
# - If a detail is not provided in the query, set its value to null.
# - Extract and populate all intents mentioned in the query.
# - Ensure the response format strictly follows the example format.
# """
# instruction2 = """
# ou are an AI assistant that helps users plan their travel. Based on the available options (hotel, flight, tour, or transfer), you will provide a friendly and conversational response that includes details about the services. You should present the information like a helpful suggestion, without directly asking if the user wants more details.

# Here’s how you should handle each category:

# Flight Option:

# Mention the airline, the price, class, stopover (if any), availability, and the flight schedule (date and time).
# Present the flight details in a natural, friendly tone.
# Hotel Option:

# Mention the hotel name, location, price, availability, amenities, and user reviews (if any).
# Provide the hotel details in a conversational way, highlighting the best aspects, like amenities and the guest review.
# Tour Option:

# Mention the tour name, price, availability, and duration.
# Present the tour in a way that entices the user, making it sound like a fun and enriching experience.
# Transfer Option:

# Mention the transfer type (e.g., bus), the route (from where to where), price, availability, and schedule.
# Present the transfer option as an affordable and convenient choice for getting around.


# """



# def get_intent_and_details(user_query):
#     full_prompt = f"{instructions}\nQuery: {user_query}\nResponse:"
    
#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(full_prompt)
        
#         if not response or "fashion assistant" in response.text.lower():
#             return {"error": "Non-travel related query detected or empty response"}
        
#         return json.loads(response.text.strip())  
#     except Exception as e:
#         return {"error": f"Error in generating response: {str(e)}"}

# def get_naturalresponse_and_details(intent_json):
#     if "error" in intent_json:
#         print(intent_json["error"])
#         return
    
#     full_prompt2 = f"{instruction2}\nInput: {json.dumps(intent_json)}\nResponse:"
#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(full_prompt2)
#         print(response.text.strip())
#     except Exception as e:
#         print(f"Error generating natural language response: {e}")

# test_queries = [
#     "Find me a hotel in New York with a budget of $1000, a flight to Lahore on December 25th with a stopover in Lahore and a budget of $1000, a tour within a $10 budget, and a transfer from Paris to London on December 25th within a $150 budget.",
    
#     "I need a hotel in New York under $1000, a flight to Lahore on December 25th with a stopover in Lahore and a budget of $1000, and a transfer from Paris to London on December 25th with a budget of $150.",
    
#     "Can you find me a hotel in New York with a budget of $1000, a flight to Lahore on December 25th with a stopover in Lahore, and a transfer from Paris to London within $150?",
    
#     "Find me a tour within a $10 budget, a hotel in New York under $1000, and a flight to Lahore on December 25th with a stopover in Lahore and a budget of $1000.",
    
#     "Book me a hotel in New York within $1000, a flight to Lahore on December 25th with a stopover in Lahore and a budget of $1000, and a transfer from Paris to London within a $150 budget.",
    
#     "Find a hotel in New York under $1000 and a flight on December 25th to Lahore with a stopover in Lahore and a budget of $1000.",
    
#     "Show me a hotel in New York with a budget of $1000 and a transfer from Paris to London on December 25th within a $150 budget.",
    
#     "I need a hotel in New York under $1000, a flight on December 25th to Lahore with a stopover in Lahore, and a transfer from Paris to London for $150.",
    
#     "Book a hotel in New York with a budget of $1000, a flight to Lahore on December 25th with a stopover in Lahore, and a transfer from Paris to London within a $150 budget.",
    
#     "What are you wearing today?"

# ]

# for query in test_queries:
#     print(f"Query: {query}")
#     try:
#         response_json = get_intent_and_details(query)
#         # print("Response:", response_json)

#         if "error" not in response_json:
#             send_to_api(response_json)  
#         else:
#             print("Error in response:", response_json["error"])

#     except Exception as e:
#         print(f"Error processing the intent: {e}")
#     print("\n" + "-"*50 + "\n")
import google.generativeai as genai
import requests
import json

# Function to send data to API
def send_to_api(intent_json):
    api_url = "http://localhost:8000/v1/search/globalsearch"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(api_url, json=intent_json, headers=headers)
    
    if response.status_code == 200:
        get_naturalresponse_and_details(response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Configure Gemini API
genai.configure(api_key="AIzaSyD3D2FdD7AK3gT8wjqekH-AKWSDeeC76Yw")

# Instructions for Intent Detection
instructions = """
You are an expert intent recognition model. Your task is to identify intents from user queries related to travel services and extract key details.

However, if the query is unrelated to travel services (e.g., fashion, clothing, beauty), you must respond by stating:
"I am a fashion assistant, I don’t have knowledge other than this domain. Sorry, but I can help you in matters related to travel."

Instructions:
1. Identify intents from user queries.
2. The supported intents are: Hotel_search, Flight_search, Tour_search, and Transfer_search.
3. Analyze the query and extract details for each intent as follows:

Intent Details:
- Hotel_search:
   - location: City or place mentioned in the query.
   - budget: The price mentioned, in numeric format (default to null if not provided).
   
- Flight_search:
   - schedules: Date of the flight (default to null if not mentioned).
   - stepover: Stopover location (default to null if not mentioned).
   - budget: The price mentioned, in numeric format (default to null if not provided).
   
- Tour_search:
   - budget: The price mentioned, in numeric format (default to null if not provided).

- Transfer_search:
   - schedules: Date of the transfer (default to null if not provided).
   - from: Starting location (default to null if not provided).
   - to: Destination location (default to null if not provided).
   - budget: The price mentioned, in numeric format (default to null if not provided).

Response Format:
{
  "intentType": ["<Intent1>", "<Intent2>", ...],
  "Hotel_search": {
    "location": "<location>",
    "budget": <budget>
  },
  "Flight_search": {
    "schedules": "<schedules>",
    "stepover": "<stepover>",
    "budget": <budget>
  },
  "Tour_search": {
    "budget": <budget>
  },
  "Transfer_search": {
    "schedules": "<schedules>",
    "from": "<from>",
    "to": "<to>",
    "budget": <budget>
  }
}

Guidelines:
- If a detail is not provided in the query, set its value to null.
- Extract and populate all intents mentioned in the query.
- Ensure the response format strictly follows the example format.
"""

# Instructions for Natural Language Generation
instruction2 = """
You are an AI assistant that helps users plan their travel. Based on the available options (hotel, flight, tour, or transfer), you will provide a friendly and conversational response that includes details about the services. You should present the information like a helpful suggestion, without directly asking if the user wants more details.

Here’s how you should handle each category:

Flight Option:
Mention the airline, the price, class, stopover (if any), availability, and the flight schedule (date and time).
Hotel Option:
Mention the hotel name, location, price, availability, amenities, and user reviews (if any).
Tour Option:
Mention the tour name, price, availability, and duration.
Transfer Option:
Mention the transfer type (e.g., bus), the route (from where to where), price, availability, and schedule.
"""

# Function to Detect Intent and Details
def get_intent_and_details(user_query):
    full_prompt = f"{instructions}\nQuery: {user_query}\nResponse:"
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(full_prompt)
        
        # Explicitly handle non-travel queries
        if "fashion assistant" in response.text.lower():
            print("I am a fashion assistant, I don’t have knowledge other than this domain. Sorry, but I can help you in matters related to travel.")
            return {"error": "Non-travel related query detected"}
        
        return json.loads(response.text.strip())  
    except Exception as e:
        return {"error": f"Error in generating response: {str(e)}"}

# Function to Generate Natural Response
def get_naturalresponse_and_details(intent_json):
    if "error" in intent_json:
        print(intent_json["error"])
        return
    
    full_prompt2 = f"{instruction2}\nInput: {json.dumps(intent_json)}\nResponse:"
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(full_prompt2)
        print(response.text.strip())
    except Exception as e:
        print(f"Error generating natural language response: {e}")

# Test Queries
test_queries = [
    "Find me a hotel in New York with a budget of $1000, a flight to Lahore on December 25th with a stopover in Lahore and a budget of $1000, a tour within a $10 budget, and a transfer from Paris to London on December 25th within a $150 budget.",
    "What are you wearing today?",
    "Show me the latest fashion trends.",
    "Find me a hotel in Paris under $500.",
]

# Loop Through Test Queries
for query in test_queries:
    print(f"Query: {query}")
    try:
        response_json = get_intent_and_details(query)

        # Handle Non-Travel Queries
        if "error" not in response_json:
            send_to_api(response_json)
        else:
            print("")

    except Exception as e:
        print(f"Error processing the intent: {e}")
    print("\n" + "-"*50 + "\n")
