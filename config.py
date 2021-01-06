from dotenv import load_dotenv
load_dotenv()
import os


API_TOKEN = os.getenv('API_TOKEN')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DOMAIN = os.getenv("DOMAIN")
DB_DOMAIN = os.getenv("DB_DOMAIN")
DB_PORT = os.getenv("DB_PORT")
ADMIN_ID = int(os.getenv("ADMIN_ID"))