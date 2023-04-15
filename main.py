from fastapi import FastAPI, HTTPException
import os
from faster_whisper import WhisperModel
import time
import sys
from pytube import YouTube

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/download-from-storage-and-generate-new-caption")
async def download_from_storage_and_generate_new_caption(video_id: str, desired_language: str, generate_caption_job_id: int):
    # get default_language by doing a db query on video_id
    return {"message": "WIP"}

@app.get("/pytube-download")
async def pytube_download():
    start_time = time.time()
    
    yt = YouTube('https://www.youtube.com/watch?v=gGZmi3UVSOI').streams.filter(only_audio=True).first()
    yt.download()
    file_name=yt.default_filename

    # delete file from local storage
    os.remove(file_name)

    return {"message": "WIP","response_time":(time.time()-start_time),"file_name":file_name}

@app.get("/download-from-YT-and-upload-and-generate-caption")
async def download_from_YT_and_upload_and_generate_caption():
    start_time = time.time()
    
    yt = YouTube('https://www.youtube.com/watch?v=gGZmi3UVSOI').streams.filter(only_audio=True).first()
    yt.download()
    file_path=yt.default_filename

    # run audio through faster_whisper
    model_size='tiny' # INT8: 2.4s-2.7s 
    # model_size='base' #2.5s-2.7s
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