import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import sys

# Add src directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import preprocess_data

def train_att_model(csv_path) -> None:
    print(f"Loading Attribution training data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    y = df['attribution']    # Separate the target attribution
    X = preprocess_data(df)  # Preprocess features
    
    print(f"Training Attribution Model (Random Forest)... Features: {X.shape[1]}")
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    model.fit(X, y)
    
    os.makedirs('models', exist_ok=True)
    
    # Save the model and feature list
    joblib.dump(model, 'models/model_att.pkl')
    joblib.dump(X.columns.tolist(), 'models/att_features.pkl')
    print("Attribution Model saved successfully to models/model_att.pkl")

if __name__ == "__main__":
    train_att_model('data/attribution/radcom_att_train.csv')