from dotenv import load_dotenv
from os import getenv
from datetime import datetime as dt

load_dotenv()

database_url = getenv('DATABASE_URL')
postgres_pass = getenv('POSTGRES_PASSWORD')
aws_region = getenv('us-east-1')
secret_key = getenv('SECRET_KEY')