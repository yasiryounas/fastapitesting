

create the Python virtual environment by following command while remaining in your project folder and in terminal:
py -3 -m venv venv

Now activate the virtual environment by 

venv\Scripts\activate.bat
venv\Scripts\Activate.ps1

For MAC/WSL
apt install python3.10-venv
python3 -m venv venvWSL
source venvWSL/bin/activate

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

To resolve the importModuleError 

 python setup.py install

to run this in ubuntu vm where it can be accessed via any IP,
  uvicorn --host 0.0.0.0 app.main:app


to make the app run automatically, just install the gunicorn...
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000


to automate it via systemctl command, 

create file api.service file in /etc/systemd/system and paste all the content available in gunicorn.service file.

to run the server
uvicorn app.main:app --reload


Create Docker file and run following command to build the image
docker build -t fastapi .
to check the docker image
docker image ls
Create the docker compose and run the following command to run the image 
docker-compose -f docker-compose-dev.yml up -d
To verify the docker compose
docker ps
To down/remove the docker-compose
docker-compose -f docker-compose-dev.yml down

For Test automation:

pip install pytest
Create Test_*.py files and run it with below
pytest -v -s
parametrize is used if we want to execute same test with different parameters
@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (7, 1, 8), (12, 4, 16)])

@pytest.fixture is use to initial a function/value to reduce the repeative code, it would use when you have to initialize the database or email before starting the testing... in short, the fixture will run first then any testing happen

To disable the warning in pytest and to stop on first test fail status, whereas in default it run for all the test no matter how much tests were failed.
pytest --disable-warnings -x

by defining the scope of the fixture on module level, fixture will not be called again unless the module completed, but then the function in the module will not run independent from other functions present in same module, like changing the order of the function, like checking login first and then creating user, will fail the first function
@pytest.fixture(scope="module")

