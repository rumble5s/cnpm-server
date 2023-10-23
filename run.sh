echo "[Installing]"
pip install -r requirements.txt
echo "[Make migrations]"
python manage.py makemigrations
echo "[Migrate]"
python manage.py migrate
echo "[Run]"
python manage.py runserver