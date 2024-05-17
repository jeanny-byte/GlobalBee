from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import random
import aiofiles
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
# Initialize an empty set to store selected words
selected_words = set()

@app.on_event("startup")
async def load_words():
    with open("words.txt", "r") as f:
        words = [word.strip() for word in f.read().split(",")]
    return words

@app.get("/random_word")
async def get_random_word():
    words = await load_words()
    available_words = [word for word in words if word not in selected_words]

    if not available_words:
        return {"error": "No words available"}
    
    selected_word = random.choice(available_words)
    selected_words.add(selected_word)
    
    async with aiofiles.open("selected_words.txt", mode="w") as f:
        await f.write("\n".join(selected_words))
    
    # async with aiofiles.open("selected.html", mode="w") as f:
    #     table_body = "".join(f"<tr><td>{word}</td></tr>" for word in selected_words)
    #     html_content = f"<html><body><h1>Selected words:</h1><table class='table table-zebra w-full'><thead><tr><th>Word</th></tr></thead><tbody id='words-table-body'>{table_body}</tbody></table></body></html>"
    #     await f.write(html_content)
        
    print(selected_word)
    return {"word": selected_word}

@app.get("/")
async def read_root():
    # Read the HTML file and return it
    with open("index.html", "r") as f:
        html = f.read()
    return HTMLResponse(html)