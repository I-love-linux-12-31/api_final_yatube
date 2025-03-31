# api_final
Решения проектной задачи на реализацию REST API на django(django rest framework)
 
## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 yatube_api/manage.py migrate

python3 yatube_api/manage.py runserver
```

## Tests
```bash
source venv/bin/activate
flake8 && pytest
```