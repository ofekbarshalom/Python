import pandas as pd
import joblib
import os
from sklearn.metrics import accuracy_score, classification_report
from src.utils import preprocess_data_app, preprocess_data_att

def test_model(task_type, test_csv_path) -> None:
    print(f"\n--- Testing {task_type.upper()} Model ---")
    
    # Check if model exists
    model_path = f"models/model_{task_type}.pkl"
    feature_path = f"models/{task_type}_features.pkl"
    
    try:
        # Load model and features
        model = joblib.load(model_path)
        required_features = joblib.load(feature_path)
        le = None
        if task_type == 'app':
            le_path = f"models/le_{task_type}.pkl"
            if not os.path.exists(le_path):
                 raise FileNotFoundError(f"LabelEncoder file {le_path} not found.")
            le = joblib.load(le_path)
    except FileNotFoundError as e:
        print(f"Error: Missing model files for {task_type}. Details: {e}. Train first!")
        return
    
    df = pd.read_csv(test_csv_path)
    
    # Identify target column based on task
    target_col = 'label' if task_type == 'app' else 'attribution'
    
    if target_col not in df.columns:
        print(f"Error: Target column '{target_col}' not found in {test_csv_path}")
        return

    y_true = df[target_col]
    
    if task_type == 'app':
        X = preprocess_data_app(df) # Preprocess features for app
    else:
        X = preprocess_data_att(df) # Preprocess features for att
    
    # Ensure alignment with training features
    X = X.reindex(columns=required_features, fill_value=0)
    
    print(f"Running inference on {len(df)} samples...")
    y_pred_encoded = model.predict(X)

    if task_type == 'app' and le is not None:
        y_pred = le.inverse_transform(y_pred_encoded)
    else:
        y_pred = y_pred_encoded
    
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    
    # Show report for Attribution
    if task_type == 'att':
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred))
    else:
        # For App show top 10 rows of results
        results = pd.DataFrame({'Actual': y_true, 'Predicted': y_pred})
        print("\nFirst 10 Predictions:")
        print(results.head(10))

if __name__ == "__main__":
    test_model('app', 'data/APP-1/radcom_app_test.csv')
    test_model('att', 'data/attribution/radcom_att_test.csv')