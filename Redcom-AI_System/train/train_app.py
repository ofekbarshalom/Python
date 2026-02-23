import pandas as pd
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import preprocess_data_app

def train_app_model(csv_path) -> None:
    print(f"Loading App training data...")
    df = pd.read_csv(csv_path)
    
    le = LabelEncoder()
    y = le.fit_transform(df['label'])
    X = preprocess_data_app(df)
    
    # Defining the three models
    rf = RandomForestClassifier(n_estimators=300, max_depth=25, random_state=42)
    et = ExtraTreesClassifier(n_estimators=300, max_depth=25, random_state=42)
    xgb_model = xgb.XGBClassifier(n_estimators=300, max_depth=10, learning_rate=0.05, 
                                  random_state=42, eval_metric='mlogloss')
    
    # Creating a combined Ensemble (Voting)
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('et', et), ('xgb', xgb_model)],
        voting='soft', # Using probabilities for a more accurate decision
        n_jobs=-1
    )
    
    print(f"Training Triple Ensemble (RF + ET + XGB)... Features: {X.shape[1]}")
    ensemble.fit(X, y)
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(ensemble, 'models/model_app.pkl')
    joblib.dump(le, 'models/le_app.pkl')
    joblib.dump(X.columns.tolist(), 'models/app_features.pkl')
    print("Triple Ensemble App Model saved successfully.")

if __name__ == "__main__":
    train_app_model('data/APP-1/radcom_app_train.csv')