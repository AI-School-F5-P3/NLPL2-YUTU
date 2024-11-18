# test_youtube_api.py
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

try:
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.videos().list(
        part='snippet',
        id='YpoUzo-CflQ?si=UxGdTaI9HYayKI7B'  # ID de un video de YouTube conocido
    )
    response = request.execute()
    print("API de YouTube funciona correctamente!")
    print("Título del video:", response['items'][0]['snippet']['title'])
except Exception as e:
    print(f"Error: {str(e)}")