# Build instructions

`pip install -t lib -r requirements.txt
(cd lib; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u main.py`

## Run locally

`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
or
`uvicorn main:app --reload`
then invoke the API with
`curl http://127.0.0.1:8000/pytube-download`

## GCP App Engine Instructions

youtube tutorial i started with: https://tutlinks.com/deploy-fastapi-app-on-google-cloud-platform/

### GCP App Enginer pricing resources

pricing calculator: https://cloud.google.com/products/calculator  
free tier: https://cloud.google.com/free/docs/free-cloud-features#app-engine  
instance classes: https://cloud.google.com/appengine/docs/standard/#second-gen-runtimes  
updating `app.yaml` with preferences: https://cloud.google.com/appengine/docs/standard/reference/app-yaml?tab=python#example

#### step 1

`rm -rf dubdubs-lambda-py/  
git clone -b https://github.com/mkandan/dubdubs-lambda-py.git
cd dubdubs-lambda-py/
virtualenv env
source env/bin/activate
pip install -r requirements.txt
gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app`

Change the numerical value in `gunicorn` to the number of workers you want to run.

#### step 2

`gcloud app create
gcloud app deploy app.yaml
gcloud app browse`

## Packing for AWS Lambda

1. Install requirements into /lib

`pip install -t lib -r requirements.txt`

2. Recursively zip up /lib

`(cd lib; zip ../lambda_function.zip -r .)`

3. Lob main.py into the zip

`zip lambda_function.zip -u main.py`
