import openai
import os
from fastapi import FastAPI, UploadFile, Form  # FastAPI core features
from dotenv import load_dotenv  # Load environment variables from .env file
from fastapi.responses import JSONResponse  # For returning structured JSON responses
import uvicorn  # For running the FastAPI app

#Load OpenAI API key securely from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#Initialize FastAPI app
app = FastAPI()

#Root endpoint to confirm app is running
@app.get("/")
def read_root():
    return {"message": "Welcome to the Mini GenAI App!"}

#Endpoint to summarize uploaded text file content
@app.post("/summarize")
async def summarize_text(file: UploadFile, summary_length: str = Form("short")):
    # Read and decode uploaded file contents
    text = await file.read()
    text = text.decode("utf-8")

    #Set token limits based on requested summary length
    max_tokens = 50 if summary_length == "short" else (150 if summary_length == "medium" else 300)

    try:
        #Call OpenAI API to generate a summary
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Summarize the following text in {summary_length} detail:\n{text}"
            }],
            max_tokens=max_tokens,
            temperature=0.7
        )

        #Extract and return the summary
        summary = response.choices[0].message['content'].strip()
        return JSONResponse(content={"summary": summary})

    except Exception as e:
        #Catch and return any errors from the API call
        return JSONResponse(content={"error": str(e)}, status_code=500)

#Run the app locally using Uvicorn (if run directly, not imported)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
