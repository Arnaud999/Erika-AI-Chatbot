
#----------------Make Sure Fill all the details and your API key HERE!!!-----------------


# Your API Key
API_KEY = "" # enter your API_KEY

# Other Details
ai_api_dict = { # some API urls
    "OpenAI Chat API": "https://api.openai.com/v1/chat/completions",
    "Groq Llama API": "https://api.groq.com/openai/v1/chat/completions"
}

API_URL = ai_api_dict["Groq Llama API"] # Change accordingly

MODEL = "llama-3.1-8b-instant"  # find an active model

Model_name = "Groq's Llama 3.1" # name of model
