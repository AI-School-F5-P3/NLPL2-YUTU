import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import joblib

# Asegúrate de que los recursos de NLTK estén descargados
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def load_data(file_path):
    """Carga los datos desde un archivo CSV."""
    return pd.read_csv(file_path)

def clean_text(text):
    """Limpia el texto eliminando URLs, menciones, caracteres especiales y números."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', str(text))
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text.lower().strip()

def tokenize_and_lemmatize(text):
    """Tokeniza y lematiza el texto."""
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

def prepare_data_for_modeling(data):
    """Prepara los datos para el modelado."""
    X = data['cleaned_text']
    y = data['IsToxic']
    
    # Dividir en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Vectorización TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    
    return X_train_vectorized, X_test_vectorized, y_train, y_test, vectorizer

def main():
    # Cargar datos
    data = load_data('comentarios_limpios.csv')
    
    # Aplicar limpieza de texto si no se ha hecho en EDA.py
    if 'cleaned_text' not in data.columns:
        data['cleaned_text'] = data['Text'].apply(clean_text)
    
    # Tokenización y lematización si no se ha hecho en EDA.py
    if 'tokenized_text' not in data.columns:
        data['tokenized_text'] = data['cleaned_text'].apply(tokenize_and_lemmatize)
    
    # Preparar datos para modelado
    X_train, X_test, y_train, y_test, vectorizer = prepare_data_for_modeling(data)
    
    # Guardar datos procesados
    np.save('X_train.npy', X_train.toarray())
    np.save('X_test.npy', X_test.toarray())
    np.save('y_train.npy', y_train)
    np.save('y_test.npy', y_test)
    joblib.dump(vectorizer, 'vectorizer.joblib')
    
    print("Datos preprocesados y guardados con éxito.")

if __name__ == "__main__":
    main()