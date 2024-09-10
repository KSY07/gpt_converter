from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
app = FastAPI()
client = OpenAI(api_key=OPENAI_API_KEY)


class GPTRequest(BaseModel):
    prompt: str
@app.post("/gpt/request")
async def get_gpt_response(request:GPTRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is missing")

    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "너는 지금부터 캐드 도면을 그려줘야해."},
            {"role": "user", "content": request.prompt},
        ]
    )

    return {"gpt_response": completion.choices[0].message}

@app.post("/gpt/request/image")
async def get_gpt_image_response(request:GPTRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is missing")

    completion = client.image.generate(
        model="dall-e-3",
        prompt=request.prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return {"image_response": completion.data[0].url}