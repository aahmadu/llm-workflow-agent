from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI client (v1.x+)
client = openai.OpenAI(api_key=api_key)

app = FastAPI()

class InputData(BaseModel):
    input_text: str

@app.post("/run-agent")
async def run_agent(data: InputData):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": data.input_text}
            ]
        )
        output_text = response.choices[0].message.content
        return {"output_text": output_text}
    except Exception as e:
        return {"error": str(e)}
