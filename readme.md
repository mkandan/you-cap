# Build instructions

`pip install -t libraries -r requirements.txt
(cd libraries; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u main.py`

### Explained

1. Install requirements into /libraries

`pip install -t libraries -r requirements.txt`

2. Recursively zip up /libraries

`(cd libraries; zip ../lambda_function.zip -r .)`

3. Lob main.py into the zip

`zip lambda_function.zip -u main.py`
