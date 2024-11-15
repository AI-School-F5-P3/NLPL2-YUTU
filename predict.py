from joblib import load
import numpy as np

def load_model_and_vectorizer():
    model = load('best_log_reg.joblib')  
    vectorizer = load('vectorizer.joblib')
    return model, vectorizer

def predict_toxicity(text, model, vectorizer):
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)
    probability = model.predict_proba(text_vectorized)[0][1]
    return prediction[0], probability

if __name__ == "__main__":
    model, vectorizer = load_model_and_vectorizer()
    
 
    text = "Este es un comentario de ejemplo"
    prediction, probability = predict_toxicity(text, model, vectorizer)
    print(f"Predicción: {'Tóxico' if prediction else 'No tóxico'}")
    print(f"Probabilidad de ser tóxico: {probability:.2f}")