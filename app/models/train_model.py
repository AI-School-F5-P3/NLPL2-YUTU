import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score
from joblib import dump, load

def train_model(X_train, y_train):
    # Logistic Regression
    log_reg = LogisticRegression(random_state=42)
    param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100],
                  'penalty': ['l1', 'l2']}
    grid_search = GridSearchCV(log_reg, param_grid, cv=5, scoring='f1')
    grid_search.fit(X_train, y_train)
    
    best_log_reg = grid_search.best_estimator_
    
    # Random Forest
    rf = RandomForestClassifier(random_state=42)
    param_grid = {'n_estimators': [100, 200, 300],
                  'max_depth': [10, 20, 30, None]}
    grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='f1')
    grid_search.fit(X_train, y_train)
    
    best_rf = grid_search.best_estimator_
    
    # Evaluate models on training data
    for name, model in [('Logistic Regression', best_log_reg), ('Random Forest', best_rf)]:
        y_pred = model.predict(X_train)
        print(f"\n{name} - Training Metrics:")
        print(f"Accuracy: {accuracy_score(y_train, y_pred):.4f}")
        print(f"F1 Score: {f1_score(y_train, y_pred):.4f}")
        print(f"Recall: {recall_score(y_train, y_pred):.4f}")
        print(f"ROC AUC: {roc_auc_score(y_train, model.predict_proba(X_train)[:, 1]):.4f}")
        
        # Cross-validation scores
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
        print(f"Cross-validation F1 Scores: {cv_scores}")
        print(f"Mean CV F1 Score: {np.mean(cv_scores):.4f}")
    
    return best_log_reg, best_rf

if __name__ == "__main__":
    X_train = np.load('X_train.npy')
    y_train = np.load('y_train.npy')
    
    best_log_reg, best_rf, results = train_model(X_train, y_train)
    
    # Crear DataFrame con los resultados
    results_df = pd.DataFrame(results)
    
    # Guardar resultados en CSV
    results_df.to_csv('model_results.csv', index=False)
    print("Results saved to model_results.csv")
    
    dump(best_log_reg, 'best_log_reg.joblib')
    dump(best_rf, 'best_rf.joblib')