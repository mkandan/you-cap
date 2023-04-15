virtualenv --python=/usr/bin/python3.9 python
source python/bin/activate
pip install -r requirements.txt -t python/lib/python3.9/site-packages

zip -r9 python.zip python