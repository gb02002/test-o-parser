### DOCUMENTATION

Test parser task.

Uses Django, celery, telegram and selemiun, MariaDB.

To start project:

1. Clone repository

2. Create .env file, this is example:

DATABASE_PASSWORD = 
STATIC_ROOT = '/usr/src/app/static/'
SECRET_KEY = ''
BOT_TOKEN = ''
CHAT_ID = 
PARSING_PATH = 'https://www.ozon.ru/seller/1/products/'

3. Setup.

I wasn't able to start docker-compose, celery has conflict with database. Although you can set up all containers by "docker-compose up 'name_of_container'", ex: "docker-compose up db".


4. Everything is available by /v1/products/. It has 3 methods: 2 GET and a POST. 
    
5. Documentation is available by /swagger/

6. If you would like not to use Docker you can simply use python -m venv /path/to/directory and run install pip -r requirements.txt
