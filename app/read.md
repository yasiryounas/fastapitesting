

create the Python virtual environment by following command while remaining in your project folder and in terminal:
py -3 -m venv venv

Now activate the virtual environment by 

venv\Scripts\activate.bat

install the fastAPI by following command

pip install fastapi[all]
psycopg2 is for postgres integration
pip install psycopg2

sqlalchemy is for programmetically model creation for DB
pip install sqlalchemy

Jose was for jwt token creation 
pip install python-jose[cryptography]
pip install "python-jose[cryptography]"

Alembic is used for database migration tool, any change in database model will be updated accordingly.
pip install alembic
To initialize the alembic, run the following commands in terminal
alembic init alembic

it will add the revision and create the model accordingly
alembic revision -m "create post tables"

It will upgrade the vision in the dB
alembic upgrade 218590f44fd5

To downgrade revision, where you want to go..
alembic downgrade 218590f44fd5

To make alembic automatically detect the models created in Models file,
alembic revision --autogenerate -m "auto-vote"

to install the library for this project

pip install -r requirements.txt

to run the server
uvicorn app.main:app --reload