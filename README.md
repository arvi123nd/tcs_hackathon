# tcs_hackathon
# Airport Wayfinding and Navigation

This project uses the LLaMA 3.1 model via the Ollama platform to provide a wayfinding and navigation chatbot for airports.

## Features

- Provides gate information and navigation prompts.
- Uses static JSON data to answer specific queries.
- Integrates with LLaMA 3.1 for more generalized responses.

## Setup

1. Install [Ollama](https://ollama.com/download) on your local machine.
2. Clone this repository.
3. Set up a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
4. uvicorn app.main:app --reload

Usage

Send POST requests to http://127.0.0.1:8000/generate with a JSON body containing a query, e.g.:

curl -X POST "http://127.0.0.1:8000/generate" -H "Content-Type: application/json" -d '{"query": "Where is Gate 12?"}'


### **Step 3: Push the Project to GitHub**

1. **Add, Commit, and Push Your Changes**

   ```bash
   git add .
   git commit -m "Initial commit with full implementation"
   git remote add origin https://github.com/yourusername/airport-wayfinding.git
   git push -u origin main


## Step 4: Testing the Implementation

### Run the Server Locally

- Ensure Ollama is installed and running on your local machine with the LLaMA 3.1 model.
- Start the FastAPI server:
  ```bash
  uvicorn app.main:app --reload
- Test the API using curl or Postman.

#### Check GitHub Actions
 - After pushing your code, check the Actions tab on GitHub to ensure the CI/CD pipeline runs correctly.

This update correctly reflects the steps needed to run and test the implementation locally, as well as how to verify the CI/CD pipeline via GitHub Actions.
