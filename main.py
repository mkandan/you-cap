from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL
import os
from faster_whisper import WhisperModel
from mangum import Mangum
import time

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/download-from-storage-and-generate-new-caption")
async def download_from_storage_and_generate_new_caption(video_id: str, desired_language: str, generate_caption_job_id: int):
    # get default_language by doing a db query on video_id
    return {"message": "WIP"}

@app.get("/download-from-YT-and-upload-and-generate-caption")
async def download_from_YT_and_upload_and_generate_caption():
    start_time = time.time()
    
    # (desired_language: str):
    desired_language = 'en'

    URLS = ['https://www.youtube.com/watch?v=gGZmi3UVSOI'] # apple audio

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'outtmpl': '%(id)s.%(ext)s'  # Output file template
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)

    # get file path source of downloaded file from youtube
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(URLS[0], download=True)
        file_path = ydl.prepare_filename(info_dict)  # Get the file path of the downloaded file
        file_name = file_path.split('.')[0]

    # run audio through faster_whisper
    model_size='tiny' # INT8: 3.2s-3.5s 
    # model_size='base' #3.8s
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    # word-level timestamps & language info
    segments, info = model.transcribe(file_path, word_timestamps=True)

    captions = []
    for segment in segments:
        for word in segment.words:
            captions.append({
            "word": word.word,
            "start": word.start,
            "end": word.end,
            "confidence": word.probability
            })
        
    # delete file from local storage
    os.remove(file_path)

    return {"language":info.language,"language_probability":info.language_probability,"captions": captions,"response_time":(time.time()-start_time)}

handler = Mangum(app)