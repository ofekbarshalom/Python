from celery import Celery
from typing import Any
import pandas as pd
import joblib
import io
import os
from src.utils import preprocess_data_app, preprocess_data_att

# Initialize Celery with Redis broker
celery_app = Celery("tasks", 
                    broker="redis://redis:6379/0", 
                    backend="redis://redis:6379/1")

@celery_app.task(bind=True)
def run_inference_task(self, csv_content: str, task_type: str) -> str | dict[str, str]:
    # Load data from string
    df = pd.read_csv(io.StringIO(csv_content))
    
    model_path = f"models/model_{task_type}.pkl"
    feature_path = f"models/{task_type}_features.pkl"
    
    try:
        # Load model and feature list
        model = joblib.load(model_path)
        required_features = joblib.load(feature_path)
        le = None
        if task_type == 'app':
            le_path = f"models/le_{task_type}.pkl"
            if not os.path.exists(le_path):
                 raise FileNotFoundError(f"LabelEncoder file {le_path} not found.")
            le = joblib.load(le_path)
    except FileNotFoundError as e:
        return {"error": f"Model or Encoder files not found for {task_type}. Details: {e}. Ensure training is complete."}
    
    # Process and engineer features
    if task_type == 'app':
        X = preprocess_data_app(df)
    else:
        X = preprocess_data_att(df)
    
    # Ensure feature alignment (same columns in same order as training)
    X = X.reindex(columns=required_features, fill_value=0)
    
    # Perform batch inference
    y_pred_encoded = model.predict(X)

    # Convert predictions back to textual names if LabelEncoder is available
    if task_type == 'app' and le is not None:
        predictions = le.inverse_transform(y_pred_encoded)
    else:
        predictions = y_pred_encoded
    
    df['prediction'] = predictions
    
    # Return result as JSON
    return df.to_json(orient="split")