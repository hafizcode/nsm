# Django Project Setup Guide

Follow the steps below to set up and run this Django project:

## Prerequisites
- Install `uv` by running:
    ```bash
    pip install uv
    ```
- Create a MySQL database named `notesdb`:  
    Open MySQL Command Line, log in with your root password, and run:
    ```sql
    CREATE DATABASE notesdb;
    ```

## Steps to Run the Project

1. **Clone the Repository**  
     Clone the project repository to your local machine:
     ```bash
     git clone <repository-url>
     ```

2. **Navigate to the Project Directory**  
     Change your working directory to the cloned repository:
     ```bash
     cd <repository-folder>
     ```

3. **Install Dependencies**  
     Install the required dependencies using `uv`:
     ```bash
     uv add -r requirements.txt
     ```

4. **Apply Migrations**  
     Run the following commands to apply database migrations:
     ```bash
     uv run manage.py makemigrations
     uv run manage.py migrate
     ```

5. **Create a Superuser**  
     Create an admin user for the project:
     ```bash
     uv run manage.py createsuperuser
     ```
     - Enter `admin` as the username.
     - Leave the email field blank.
     - Set the password to `root@12345`.

6. **Run the Development Server**  
     Start the Django development server:
     ```bash
     uv run manage.py runserver
     ```

## Access the Application
- Open your browser and navigate to `http://127.0.0.1:8000/`.

You're all set!  
