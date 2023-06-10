# Orbidi Project

To run this project please use install **python 3.7.9**

Dependencies required to run it are store and defined in requirements.txt, to install it please run the code

>pip install -r requirements.txt

After install dependencies you can run the project with this command

>uvicorn main:app --reload

## Credentials

values for database and api conection should be store in a file named .env, fastapi will take the required keys

## Endpoints

There are four endpoint to be executed

>http://127.0.0.1:8000/contact/create/hubspot

For this one a example of request body is this

    {
    "email": "juan@orbidi.com",
    "firstname": "Test",
    "lastname": "Orbidi",
    "phone": "(322) 123-4567",
    "website": "orbidi.com",
    "test": "outside"
    }

>http://127.0.0.1:8000/contact/sync/hubspot_clickup

And these two can be used to debug this implementation

>http://127.0.0.1:8000/contact

>http://127.0.0.1:8000/task

Contact will work for fetch contacts from hubspot and task for fetch "contacts" from clickup platform, they don't have any parameters

## Logs

To check what contacts are been synced you can check **info.log** file in the root project folder, there will be a message indicating contact email synced

There is another one named **error.log** where you can find controlled **exceptions**

## Database

In case to use a local database you can migrate with alembic using the command

>alembic upgrade head

For the specified database you can run it without this step.