from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import ollama
import uvicorn


app = FastAPI(
    title="AI User Story Generator",
    description="FastAPI application using Ollama LLM",
    version="1.0"
)


# Request model
class RequirementRequest(BaseModel):
    requirement: str


# Home page
@app.get("/")
def home():
    return FileResponse("static/index.html")


# LLM endpoint
@app.post("/generate")
def generate_user_stories(request: RequirementRequest):

    prompt = f"""
You are an expert Business Analyst and QA Engineer.

Convert the following software requirement into detailed Agile user stories.

Requirement:
{request.requirement}

For each user story, use exactly this structure:

User Story:
AS A <type of user>,
I WANT <functionality>,
SO THAT <business value>.

Acceptance Criteria:
1. ...
2. ...
3. ...

Also include:
- Assumptions
- Important edge cases
- QA testing considerations

Make the response clear and easy to understand.
"""

    try:

        response = ollama.chat(
            model="qwen2.5-coder:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response["message"]["content"]
        print("LLM Response:", result)

        return {
            "success": True,
            "response": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )