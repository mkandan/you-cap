from fastapi import FastAPI 
from yt_dlp import YoutubeDL

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World","var":123}

@app.get("/test")
async def test():
    URLS = ['https://www.youtube.com/watch?v=gGZmi3UVSOI']

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    # with YoutubeDL(ydl_opts) as ydl:
    #     error_code = ydl.do
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)

    return {"done": "done"}

# /list-books
# /book-by-index/{index} (Ex: /book-by-index/1)