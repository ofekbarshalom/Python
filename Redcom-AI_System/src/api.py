from fastapi import FastAPI, File, UploadFile
from src.tasks import run_inference_task, celery_app
from typing import Dict

app = FastAPI(title="Radcom Traffic Classifier API")

@app.get("/")
def health_check() -> Dict[str,str]:
    return {"status": "Active", "docs": "/docs"}

@app.post("/predict/{task_type}")
async def predict(task_type: str, file: UploadFile = File(...)):
    # Endpoint to trigger inference.
    # task_type: 'app' (128 categories) or 'att' (5 categories)
    contents = await file.read()
    
    # Send to Celery for asynchronous background processing
    job = run_inference_task.delay(contents.decode('utf-8'), task_type)
    
    return {
        "task_id": job.id,
        "status": "Processing",
        "info": f"Inference started for {task_type}"
    }

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    # Check the status or fetch the result of a specific task.
    res = celery_app.AsyncResult(task_id)
    if res.ready():
        return {"status": "Done", "result": res.result}
    return {"status": "Pending"}