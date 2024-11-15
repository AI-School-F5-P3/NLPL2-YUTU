from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from scraping import get_comments_selenium

# Configuración de Flask
app = Flask(__name__)

# Cargar el modelo y el vectorizador entrenado
model = joblib.load('svm_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Configurar la base de datos (MySQL)
DB_URI = 'mysql+pymysql://user:password@localhost/your_db'
engine = create_engine(DB_URI)

# Clasificar comentarios
def classify_comments(comments):
    """Clasificar los comentarios con el modelo entrenado y asignar mensajes descriptivos."""
    comments_df = pd.DataFrame(comments, columns=['Cleaned_Text'])
    
    # Vectorizar los comentarios usando el vectorizador entrenado
    X = vectorizer.transform(comments_df['Cleaned_Text'])
    
    # Predecir con el modelo SVM
    predictions = model.predict(X)
    
    # Asignar mensajes basados en las predicciones
    comments_df['Sentiment'] = predictions
    comments_df['Message'] = comments_df['Sentiment'].apply(
        lambda x: "El comentario contiene frases o palabras de odio." if x == 'Negative' else "¡Qué comentario más amable!"
    )
    
    return comments_df

# Guardar los resultados en la base de datos
def save_to_db(df, video_url):
    """Guardar los resultados en la base de datos."""
    df['video_url'] = video_url
    df['timestamp'] = datetime.now()
    df.to_sql('comments_analysis', engine, if_exists='append', index=False)

# Rutas de la aplicación Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form['video_url']
    comments = get_comments_selenium(video_url)

    if not comments:
        return jsonify({'message': 'No se encontraron comentarios'}), 404

    # Clasificar los comentarios y obtener mensajes personalizados
    results_df = classify_comments(comments)

    # Guardar los resultados en la base de datos
    save_to_db(results_df, video_url)
    
    # Convertir los resultados a JSON
    results_json = results_df[['Cleaned_Text', 'Message']].to_json(orient='records')

    return results_json

if __name__ == '__main__':
    app.run(debug=True)
