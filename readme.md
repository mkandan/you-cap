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
