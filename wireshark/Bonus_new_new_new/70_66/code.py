# Train models
rf_model_full = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=2, min_samples_split=2, random_state=42)
rf_model_full.fit(X_train_full, y_train)

rf_model_limited = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=2, min_samples_split=2, random_state=42)
rf_model_limited.fit(X_train_limited, y_train)
