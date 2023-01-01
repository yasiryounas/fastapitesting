

create the Python virtual environment by following command while remaining in your project folder and in terminal:
py -3 -m venv venv

Now activate the virtual environment by 

venv\Scripts\activate.bat

install the fastAPI by following command

pip install fastapi[all]
pip install psycopg2

pip install sqlalchemy

pip install python-jose[cryptography]
pip install "python-jose[cryptography]"

to run the server

uvicorn app.main:app --reload