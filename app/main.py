from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import json
from fastapi.middleware.cors import CORSMiddleware
import re
import asyncio
import logging
from difflib import get_close_matches

# Initialize FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

# Load static airport data with versioning support
with open("app/static_data.json", "r") as f:
    static_data = json.load(f)

@app.post("/generate")
async def generate_response(request: QueryRequest):
    query = request.query
    logger.info(f"Query received: '{query}'")
    
    # Search static data first
    response_text = search_static_data(query)
    
    if response_text == "Sorry, I couldn't find the information you're looking for.":
        # If the static data search returns 'not found' message, use LLaMA 3.1 model via Ollama
        response_text = await use_llama_model_async(query)
    
    return {"response": response_text}

def normalize(text):
    """Helper function to normalize text."""
    return text.lower().strip()

def find_best_match(query, items):
    """Finds the closest match for a given query in a list of items."""
    matches = get_close_matches(query, items, n=1, cutoff=0.6)
    return matches[0] if matches else None

def search_static_data(query):
    query_normalized = normalize(query)
    logger.info(f"Searching static data for: '{query_normalized}'")

    # Check gates
    for item in static_data.get("gates", []):
        gate_name = normalize(item['gate'])
        logger.debug(f"Checking gate: '{gate_name}'")
        
        if re.search(r'\b' + re.escape(gate_name) + r'\b', query_normalized):
            logger.info(f"Exact match found in gates: '{gate_name}'")
            return item["info"]

    # Check restaurants
    for item in static_data.get("restaurants", []):
        restaurant_name = normalize(item['name'])
        logger.debug(f"Checking restaurant: '{restaurant_name}'")
        if re.search(r'\b' + re.escape(restaurant_name) + r'\b', query_normalized):
            return (f"Restaurant: {item['name']}\n"
                    f"Location: {item['location']}\n"
                    f"Cuisine: {item['cuisine']}\n"
                    f"Details: {item['details']}")

    # Check lounges
    for item in static_data.get("lounges", []):
        lounge_name = normalize(item['name'])
        logger.debug(f"Checking lounge: '{lounge_name}'")
        if re.search(r'\b' + re.escape(lounge_name) + r'\b', query_normalized):
            return (f"Lounge: {item['name']}\n"
                    f"Location: {item['location']}\n"
                    f"Details: {item['details']}")

    # Check services
    for item in static_data.get("services", []):
        service_name = normalize(item['name'])
        logger.debug(f"Checking service: '{service_name}'")
        if re.search(r'\b' + re.escape(service_name) + r'\b', query_normalized):
            return (f"Service: {item['name']}\n"
                    f"Location: {item['location']}\n"
                    f"Details: {item['details']}")

    # Check directions
    for item in static_data.get("directions", []):
        start = normalize(item['start'])
        end = normalize(item['end'])
        logger.debug(f"Checking direction start: '{start}'")
        logger.debug(f"Checking direction end: '{end}'")
        if re.search(r'\b' + re.escape(start) + r'\b', query_normalized) or re.search(r'\b' + re.escape(end) + r'\b', query_normalized):
            return (f"Directions from {item['start']} to {item['end']}:\n"
                    f"{item['details']}")

    return "Sorry, I couldn't find the information you're looking for."

async def use_llama_model_async(query):
    logger.info(f"Running LLaMA model with query: '{query}'")

    try:
        process = await asyncio.create_subprocess_exec(
            'ollama', 'run', 'llama3.1',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        output, error = await process.communicate(input=query.encode())

        if process.returncode != 0:
            error_message = error.decode('utf-8').strip()
            logger.error(f"Error executing LLaMA command: {error_message}")
            return f"Error executing LLaMA command: {error_message}"
        
        response = output.decode('utf-8').strip()
        logger.info(f"LLaMA model response: '{response}'")
        return response
    
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return f"Exception occurred: {str(e)}"

# Mount the static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")
