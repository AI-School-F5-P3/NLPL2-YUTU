import joblib
import pandas as pd
import datetime
from flask import Flask, request, jsonify, render_template
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno
DB_URI = os.getenv('DB_URI')
API_KEY = os.getenv('MI_API_KEY')

# Configurar la aplicación Flask
app = Flask(__name__)

# Cargar el modelo y vectorizador
model = joblib.load('models/svm_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

# Configuración de la base de datos y la API de YouTube usando variables de entorno
client = MongoClient(DB_URI)
db = client.youtube_comments
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Función para extraer comentarios de un video de YouTube
def get_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,
        textFormat='plainText'
    )
    response = request.execute()

    for item in response.get('items', []):
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    return comments

# Función para clasificar comentarios
def classify_comments(comments):
    comments_df = pd.DataFrame(comments, columns=['comment'])
    X = vectorizer.transform(comments_df['comment'])
    predictions = model.predict(X)
    comments_df['prediction'] = predictions
    return comments_df

# Función para guardar los resultados en la base de datos
def save_to_db(df, video_id):
    data = df.to_dict('records')
    for item in data:
        item['video_id'] = video_id
        item['timestamp'] = datetime.datetime.now()
    db.comments.insert_many(data)

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form['video_url']
    video_id = video_url.split('v=')[1]  # Extraer el video ID de la URL
    comments = get_comments(video_id)

    if not comments:
        return jsonify({'message': 'No se encontraron comentarios'}), 404

    # Clasificar y guardar los resultados en la base de datos
    results_df = classify_comments(comments)
    save_to_db(results_df, video_id)

    return results_df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
