# Radcom Traffic Classification System 🚀

This project is a high-performance, scalable machine learning system designed to classify encrypted network traffic.
---

## 🧠 Machine Learning Approach

### Algorithm

- **App Classification**:  
  Implemented using a combination of **Random Forest**, **Extra Trees**, and **XGBoost** classifiers.  
  Each model is trained with **300 estimators**, with maximum depths of **25** (Random Forest), **25** (Extra Trees), and **10** (XGBoost), to handle the complexity of **128 target classes**.

- **Attribution Classification**:  
  Trained with **100 estimators**, using all available CPU cores (`n_jobs=-1`) for efficient processing.

### Preprocessing & Feature Engineering
To ensure the model generalizes across different networks and avoids overfitting on identity data, the following steps are performed:

- **Identity Removal**:  
  Columns such as `Source_IP`, `Destination_IP`, and `Timestamp` are dropped to focus purely on behavioral patterns.

- **Protocol Encoding**:  
  Network protocols are encoded numerically:
  - TCP → `6`
  - UDP → `17`

- **Feature Alignment**:  
  During inference, incoming data is reindexed to match the exact feature order used during training, with missing values filled with zeros.

---

## 🏗️ System Architecture

The project follows a **decoupled microservices architecture** designed to handle high-traffic *hexabyte-scale* workloads through horizontal scaling.

- **FastAPI**  
  REST API gateway serving as the entry point for inference requests using the OpenAPI standard.

- **Celery & Redis**  
  Asynchronous task queue that prevents API blocking during heavy ML computations, enabling massive scale.

- **Streamlit**  
  User-friendly web interface for file uploads, real-time status polling, and result visualization.

- **Docker**  
  All components are containerized to ensure environment consistency across development and production.

---

## 🚀 Getting Started

### 1. Model Training & Testing

> ⚠️ Models are **not included** in the source submission.  
> You must generate them before starting the Docker services.

The trained models will be saved under the `models/` directory.

#### Train the models
```bash
# Generate the Application Model
python3 src/train_app.py

# Generate the Attribution Model
python3 src/train_att.py
```

#### Test the models
Evaluate accuracy and view classification reports:
```bash
python3 src/test_models.py
```

---

### 2. Activating the Docker Environment

Ensure your `models/` directory contains the generated `.pkl` files before launching the containers.

```bash
# Build and start all services
sudo docker compose up --build
```

---

### 3. Accessing the System

Once the containers are running:

- **Streamlit Web UI**  
  http://localhost:8501  
  Upload your validation CSV and receive results with the prediction column.

- **FastAPI Docs (OpenAPI)**  
  http://localhost:8000/docs  
  Interact directly with the REST API endpoints.

---

## 📂 Project Structure

```
data/
├── APP-1/
│   ├── radcom_app_train.csv               # Application training dataset
│   ├── radcom_app_test.csv                # Application test dataset
│   └── radcom_app_val_without_labels.csv  # Application validation dataset (no labels)
│
└── attribution/
    ├── radcom_att_train.csv               # Attribution training dataset
    ├── radcom_att_test.csv                # Attribution test dataset
    └── radcom__att_val_without_labels.csv # Attribution validation dataset (no labels)

models/

predictions/
├── app_predictions.csv  # Application prediction results
└── att_predictions.csv  # Attribution prediction results

src/
├── api.py               # FastAPI server logic and endpoints
├── tasks.py             # Celery background task definitions
├── worker.py            # Celery worker initialization and model loading
├── streamlit_app.py     # Streamlit web UI
└── utils.py             # Data cleaning and preprocessing utilities

train/
├── train_app.py         # Application model training script
└── train_att.py         # Attribution model training script

test_models.py           # Model evaluation script
requirements.txt         # Python dependencies

Dockerfile.app           # API service Dockerfile
Dockerfile.worker        # Celery worker Dockerfile
docker-compose.yml       # Full stack orchestration (Redis, API, Worker, UI)
```
