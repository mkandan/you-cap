from fastapi import FastAPI 
from yt_dlp import YoutubeDL
import os
from dotenv import load_dotenv
from supabase import create_client, Client

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    dotenv_path = 'dot.env'
    load_dotenv(dotenv_path)

    supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_API_KEY'))

    response = supabase.table('queue').select('*').execute()
    print(response)
    return {'response': response}

    # URLS = ['https://www.youtube.com/watch?v=gGZmi3UVSOI']

    # ydl_opts = {
    #     'format': 'm4a/bestaudio/best',
    #     'postprocessors': [{  # Extract audio using ffmpeg
    #         'key': 'FFmpegExtractAudio',
    #         'preferredcodec': 'm4a',
    #     }]
    # }

    # with YoutubeDL(ydl_opts) as ydl:
    #     ydl.download(URLS)

    return {"done": "done"}

# /list-books
# /book-by-index/{index} (Ex: /book-by-index/1)