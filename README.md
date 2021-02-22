This is the repo for backend of powerset and provides all the REST APIs
#### Instructions to run
```bash
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
python3 src/manage.py migrate
python3 src/manage.py runserver
```