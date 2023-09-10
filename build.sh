pip install -r requirments.txt

python3 manage.py collect static --no input
python3 manage.py makemigrations
python3 manage.py migrate