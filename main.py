from fastapi import FastAPI, HTTPException
import os
import time
import sys
from pytube import YouTube

from faster_whisper import WhisperModel
# import whisper

app = FastAPI()

# automatically detects if running on GAE or local. this affects /tmp folder path
if(os.environ.get("GAE_ENV")=='standard'):
    path_to_tmp_folder = '../../../tmp' # production api on GAE
else:
    path_to_tmp_folder = 'tmp' # local api on personal device

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/download-from-storage-and-generate-new-caption")
async def download_from_storage_and_generate_new_caption(video_id: str, desired_language: str, generate_caption_job_id: int):
    # get default_language by doing a db query on video_id
    return {"message": "WIP"}

@app.get("/_ah/warmup")
async def warmup():
    # Handle your warmup logic here, e.g. set up a database connection pool
    await download_from_YT_and_upload_and_generate_caption('https://www.youtube.com/watch?v=gGZmi3UVSOI','en')
    return '', 200, {}

@app.get("/pytube-download")
async def pytube_download():
    start_time = time.time()
    
    yt = YouTube('https://www.youtube.com/watch?v=gGZmi3UVSOI').streams.filter(only_audio=True).first()
    yt.download(output_path=path_to_tmp_folder)
    file_path=path_to_tmp_folder+'/'+yt.default_filename

    # delete file from local storage
    os.remove(file_path)

    # return {"message": "WIP","response_time":(time.time()-start_time)}
    return {"message": "WIP","response_time":(time.time()-start_time)}

@app.get("/download-from-YT-and-upload-and-generate-caption")
async def download_from_YT_and_upload_and_generate_caption(yt_url: str, desired_language: str):
    start_time = time.time()
    
    # download from YT
    yt = YouTube(yt_url).streams.filter(only_audio=True).first()
    # yt = YouTube('https://www.youtube.com/watch?v=gGZmi3UVSOI').streams.filter(only_audio=True).first() #apple
    # yt = YouTube('https://www.youtube.com/watch?v=j_QH5wF9XBg').streams.filter(only_audio=True).first() #theo
    # yt = YouTube('https://www.youtube.com/watch?v=hBgEx4m-ejo').streams.filter(only_audio=True).first() #mbapp interview

    # yt = YouTube('https://www.youtube.com/watch?v=u7j--YMXZtA').streams.filter(only_audio=True).first() #mbappe song causes semaphore leak or registers at TR (turkish??)

    yt.download(output_path=path_to_tmp_folder)
    file_path=path_to_tmp_folder+'/'+yt.default_filename

    # run audio through faster_whisper
    model_size='tiny' # INT8: 2.4s-2.7s 
    # model_size='base' #2.5s-2.7s

    ###############################
    # Model: faster-whisper
    ###############################
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    # segments, info = model.transcribe(file_path)
    segments, info = model.transcribe(file_path,language=desired_language)
    language, language_probability, duration = info

    # making segments prettier --> captions
    only_words_from_captions = []

    captions = []
    for segment in segments:
        captions.append({
            "start": segment[0],
            "end": segment[1],
            "text": segment[2],
            # "words": segment[3],
            "segment_confidence": segment[4],
            "word_confidence": segment[5]
        })
        only_words_from_captions.append(segment[2])

    ###############################
    # Model: whisper
    # paramters @ https://github.com/openai/whisper/blob/main/whisper/transcribe.py
    # expanded DecodingOptions @ https://github.com/openai/whisper/blob/main/whisper/decoding.py
    ###############################
    # model = whisper.load_model(model_size) # or whatever model you prefer
    # result = model.transcribe(file_path,fp16=False,language="fr")
    # options = whisper.DecodingOptions(fp16=False,language="fr")
    # result = model.transcribe(file_path, options)

    # return {"message": "WIP","response_time":(time.time()-start_time),"text":result['text'],"segments":result['segments'],"language":result['language']}
    ###############################
    ###############################

        
    # delete file from local storage
    os.remove(file_path)

    return{"response_time":(time.time()-start_time),"info":info,"captions":captions,"language":language,"language_probability":language_probability,"duration":duration,"only_words_from_captions":only_words_from_captions}