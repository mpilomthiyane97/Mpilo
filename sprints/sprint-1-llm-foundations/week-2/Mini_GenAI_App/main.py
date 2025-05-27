import openai
import os
from fastapi import FastAPI, UploadFile, Form
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import uvicorn

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/")  # Root endpoint to avoid 404
def read_root():
    return {"message": "Welcome to the Mini GenAI App!"}


@app.post("/summarize")
async def summarize_text(file: UploadFile, summary_length: str = Form("short")):
    text = await file.read()
    text = text.decode("utf-8")

    # Define token limit based on summary length
    max_tokens = 50 if summary_length == "short" else (150 if summary_length == "medium" else 300)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize the following text in {summary_length} detail:\n{text}"}],
            max_tokens=max_tokens,
            temperature=0.7
        )

        summary = response.choices[0].message['content'].strip()
        return JSONResponse(content={"summary": summary})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)