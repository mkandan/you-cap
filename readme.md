# pytube x openai whisper (it's really faster_whisper) for Google App Engine (GAE)

why? avoid Open API token usage by using GCP free tier

some aws lambda instructions included at bottom, but i couldnt reduce the package/dependecy library size to 50mb zipped for the life of me.

## Run locally (after installing pip dependencies)

`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
or
`uvicorn main:app --reload`
then invoke the API with...

## API endpoints (Routes)

#### /pytube-download

`curl http://127.0.0.1:8000/pytube-download` to download a youtube video's audio

#### /pytube-download-and-upload

`curl http://127.0.0.1:8000/download-from-YT-and-upload-and-generate-caption` to download a youtube video and pump through [faster_whisper](https://github.com/guillaumekln/faster-whisper) to generate timestamped captions

## GCP App Engine Instructions

youtube tutorial i started with: https://tutlinks.com/deploy-fastapi-app-on-google-cloud-platform/

#### GCP App Engine pricing resources

pricing calculator: https://cloud.google.com/products/calculator  
free tier: https://cloud.google.com/free/docs/free-cloud-features#app-engine  
instance classes: https://cloud.google.com/appengine/docs/standard/#second-gen-runtimes  
updating `app.yaml` with preferences: https://cloud.google.com/appengine/docs/standard/reference/app-yaml?tab=python#example

### the weird ../../../tmp thing? in `main.py`

yea it's explained here https://cloud.google.com/appengine/docs/standard/using-temp-files?tab=python

#### set yo self up for success

`rm -rf dubdubs-lambda-py/`  
`git clone -b https://github.com/mkandan/dubdubs-lambda-py.git`  
`cd dubdubs-lambda-py/`  
`virtualenv env`  
`source env/bin/activate`  
`pip install -r requirements.txt`  
`gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app`

Change the numerical value in `gunicorn` to the number of workers you want to run.

#### success (ideally)

`gcloud app create`
`gcloud app deploy app.yaml`
`gcloud app browse`

## Packing for AWS Lambda

1. Install requirements into /lib

`pip install -t lib -r requirements.txt`

2. Recursively zip up /lib

`(cd lib; zip ../lambda_function.zip -r .)`

3. Lob main.py into the zip

`zip lambda_function.zip -u main.py`

#### All together now

`pip install -t lib -r requirements.txt
(cd lib; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u main.py`
