from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL
import os
from dotenv import load_dotenv
from storage3 import create_client as create_client_storage
from supabase import StorageException, create_client, Client
import datetime
import whisper_timestamped as whisper
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/download-from-storage-and-generate-new-caption")
async def download_from_storage_and_generate_new_caption(video_id: str, desired_language: str, generate_caption_job_id: int):
    # get default_language by doing a db query on video_id
    return {"message": "WIP"}

@app.get("/download-from-YT-and-upload-and-generate-caption")
async def download_from_YT_and_upload_and_generate_caption(desired_language: str, download_audio_job_id: int, generate_captions_job_id: int):
    # desired_language = 'en'
    # download_audio_job_id=36
    # generate_captions_job_id=37

    dotenv_path = 'dot.env'
    load_dotenv(dotenv_path)

    url = os.getenv('SUPABASE_STORAGE_URL')
    key = os.getenv('SUPABASE_API_KEY')
    headers = {"apiKey": key, "Authorization": f"Bearer {key}"}

    # pass in is_async=True to create an async client
    storage_client = create_client_storage(url, headers, is_async=False)

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

    # upload file to supabase storage
    with open(file_path, 'rb+') as f:
        res = storage_client.from_('audio').upload(f'{file_path}', file_path,)
        print('res', res)

    supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_API_KEY'))
    # prep updated history with current utc time
    utc_now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    audio_existing_history = supabase.table('audio').select('id,history').eq('video_id', file_name).execute()
    audio_updated_history = audio_existing_history.data[0]['history'] + [{'event':'downloaded_audio','time': utc_now}]
    # update row's history in audio table
    res = supabase.table('audio').update({"history": audio_updated_history}).eq('video_id', file_name).execute()

    # update download_audio job's history and status
    download_audio_job_existing_history = supabase.table('queue').select('history').eq('id', download_audio_job_id).execute()
    download_audio_job_updated_history = download_audio_job_existing_history.data[0]['history'] + [{'event':'downloaded_audio','time': utc_now}]
    download_audio_job__res = supabase.table('queue').update({"history": download_audio_job_updated_history, "status": "complete"}).eq('id', download_audio_job_id).execute()

    # run audio through openai whisper
    whisper_audio = whisper.load_audio(file_path)
    whisper_model = whisper.load_model('tiny',device='cpu')
    whisper_res = whisper.transcribe(whisper_model, whisper_audio)
    captions = []
    # pull text, start time, end time, confidence (accuracy) for each segment
    for segment in whisper_res["segments"]:
        for word in segment["words"]:
            captions.append({
                "text": word["text"],
                "start": word["start"],
                "end": word["end"],
                "confidence": word["confidence"]
            })
    # write captions to db
    utc_now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    captions_res = supabase.table('captions').insert({"history":[{'event':"created_at",'time':utc_now},{'event':"generated_captions",'time':utc_now}],"audio_id":audio_existing_history.data[0]['id'],"language":whisper_res["language"],"timestamped_captions":captions}).execute()
    # update generate_captions job's history and status
    generate_captions_job_existing_history = supabase.table('queue').select('history').eq('id', generate_captions_job_id).execute()
    generate_captions_job_updated_history = generate_captions_job_existing_history.data[0]['history'] + [{'event':'generated_captions','time': utc_now}]
    generate_captions_job__res = supabase.table('queue').update({"history": generate_captions_job_updated_history, "status": "complete"}).eq('id', generate_captions_job_id).execute()


    return {"language":whisper_res["language"],"captions_res": captions_res,"whisper_res": whisper_res}
    
    # delete file from local storage
    os.remove(file_path)