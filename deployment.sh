sudo apt-get install python-virtualenv;
virtualenv --python=python3.6 priyank-infilect-vnev;
sudo apt install python3.6-venv;
source priyank-infilect-vnev/bin/activate && pip install -r requirements.txt &&
python manage.py migrate &&
python manage.py runserver
