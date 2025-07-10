import os
from openai import OpenAI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from utils.context import get_context
from utils.context import index_wines

# Obtain the api adresses
load_dotenv() 
app = FastAPI()
# Create the embeddings and create collection once
index_wines()
# Load data
api_base = os.getenv("OPENAI_API_BASE_URL")  # Your Azure OpenAI resource's endpoint value.
api_key = os.getenv("OPENAI_API_KEY")
api_model = os.getenv("OPENAI_API_MODEL")
# Create the client using api keys
client = OpenAI(
    base_url= api_base, # "http://<Your api-server IP>:port"
    api_key = api_key
)

class Body(BaseModel):
    query: str
    limit: int


@app.get('/')
def root():
    return RedirectResponse(url='/docs', status_code=301)


@app.post('/ask')
def ask(body: Body):
    """
    Use the query parameter to interact with the desired model.
    """
    search_result = get_context(body.query, body.limit)
    chat_bot_response = assistant(body.query, search_result)
    return {'response': chat_bot_response}

def assistant(query, context):
    messages=[
        # Set the system characteristics for this chat bot
        {"role": "system", "content": "Asisstant is a chatbot that helps you find the best wine for your taste."},

        # Set the query so that the chatbot can respond to it
        {"role": "user", "content": query},

        # Add the context from the vector search results so that the chatbot can use
        # it as part of the response for an augmented context
        {"role": "Assistant", "content": str(context)}
    ]

    response = client.chat.completions.create(
        model = api_model,
        messages=messages,
    )
    return response.choices[0].message