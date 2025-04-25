@echo off
REM *******************************************************
REM This is a setup script for your Django project
REM Make sure Python and git are installed on your machine.
REM *******************************************************

REM Step 1: Create the database
REM Make sure to replace this with the correct database name or command if needed
echo Creating the database...
echo Enter MySQL root password when prompted.
mysql -u root -p < create_database.sql
echo Database created successfully.

REM Step 2: Clone the GitHub repository
echo Cloning the repository...
git clone https://github.com/hafizcode/nsm.git
cd nsm

REM Step 3: Create a Python virtual environment
echo Creating virtual environment...
py -m venv .venv

REM Step 4: Activate the virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Step 5: Install required packages from requirements.txt
echo Installing dependencies...
@REM pip install -r ./requirements.txt
pip install cryptography Django django-widget-tweaks mysqlclient pillow PyMySQL

REM Step 6: Switch to a specific Git branch (optional)
REM Replace "branch_name" with the branch you want to checkout
echo Switching to the desired branch...
git checkout release/v1.0.1

REM Step 7: Run makemigrations and migrate
echo Running makemigrations...
python manage.py makemigrations
echo Applying migrations...
python manage.py migrate

@REM Step 8: Creating Superuser
echo Creating superuser...
echo You will be prompted to enter a username, email, and password.
echo Make sure to remember these credentials for logging in.
python manage.py createsuperuser

REM Step 9: Run the Django development server
echo Starting the development server...
python manage.py runserver

REM *******************************************************
REM The script will run the Django server on localhost:8000.
REM You can modify this script to fit your specific needs.
REM *******************************************************

pause