# Build instructions

`pip install -t lib -r requirements.txt
(cd lib; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u main.py`

### Explained

1. Install requirements into /lib

`pip install -t lib -r requirements.txt`

2. Recursively zip up /lib

`(cd lib; zip ../lambda_function.zip -r .)`

3. Lob main.py into the zip

`zip lambda_function.zip -u main.py`

## Run locally

`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
or
`uvicorn main:app --reload`

## GCP App Engine Instructions

https://tutlinks.com/deploy-fastapi-app-on-google-cloud-platform/

#### step 1

`rm -rf dubdubs-lambda-py/
git clone -b https://github.com/mkandan/dubdubs-lambda-py.git
cd dubdubs-lambda-py/
virtualenv env
source env/bin/activate
pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`

#### step 2

`gcloud app create
gcloud app deploy app.yaml
gcloud app browse`
