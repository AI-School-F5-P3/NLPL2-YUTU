# test_mongodb.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
DB_URI = os.getenv('DB_URI')

try:
    client = MongoClient(DB_URI)
    client.admin.command('ping')
    print("¡Conexión exitosa!")
except Exception as e:
    print(f"Error de conexión: {str(e)}")