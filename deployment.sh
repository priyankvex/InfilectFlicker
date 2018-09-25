sudo apt-get install python-virtualenv;
virtualenv --python=python3.6 myvenv;
sudo apt install python3.6-venv;
python3.6 -m venv /priyank-infilect-vnev;
source priyank-infilect-vnev/bin/activate && pip install -r requirements.txt &&
python manage.py migrate &&
python manage.py runserver
