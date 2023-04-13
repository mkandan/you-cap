from fastapi import FastAPI 
from yt_dlp import YoutubeDL
import os
from dotenv import load_dotenv
from storage3 import create_client as create_client_storage
from supabase import StorageException, create_client, Client
import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/downloadAndUpload")
async def downloadAndUpload():
    dotenv_path = 'dot.env'
    load_dotenv(dotenv_path)

    url = os.getenv('SUPABASE_STORAGE_URL')
    key = os.getenv('SUPABASE_API_KEY')
    headers = {"apiKey": key, "Authorization": f"Bearer {key}"}

    # pass in is_async=True to create an async client
    storage_client = create_client_storage(url, headers, is_async=False)

    # allFiles = storage_client.from_('audio').list()
    # print('allFiles', allFiles)
    # return {"allFiles": allFiles}

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

    # prep supabase client for updating history
    supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_API_KEY'))
    # prep updated history with current utc time
    utc_now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    existing_history = supabase.table('audio').select('history').eq('video_id', file_name).execute()
    updated_history = existing_history.data[0]['history']
    updated_history.append({'type':'downloaded_audio','time': utc_now})

    # update row's history in audio table
    res = supabase.table('audio').update({"history": updated_history}).eq('video_id', file_name).execute()
    return {"res": res}