from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

from database import models, database
import ingestion
import schemas
from ai import service as ai_service
import logic_matcher
import export_service
from fastapi.responses import FileResponse
import uuid

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Michele's Arts Helper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    yield from database.get_db()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is running"}

@app.post("/ingest")
def ingest_assets(directory_path: str, db: Session = Depends(get_db)):
    if not os.path.isdir(directory_path):
        raise HTTPException(status_code=400, detail="Invalid directory path")
    
    count = ingestion.scan_and_ingest(directory_path, db)
    return {"status": "scanned", "files_found": count}

@app.get("/assets", response_model=List[schemas.AssetBase])
def list_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    assets = db.query(models.Asset).offset(skip).limit(limit).all()
    return assets

@app.post("/interpret")
def interpret_request(request: dict):
    # Expects {"prompt": "some text"}
    prompt = request.get("prompt", "")
    interpretation = ai_service.interpret_request(prompt)
    return interpretation

@app.post("/generate")
def generate_design(request: dict, db: Session = Depends(get_db)):
    prompt = request.get("prompt", "")
    
    # 1. Interpret
    criteria = ai_service.interpret_request(prompt)
    
    # 2. Select Assets
    assets = logic_matcher.select_assets(criteria, db)
    
    # 3. Serialize assets for response (manual for now as they are SQLAlchemy obj)
    response = {
        "criteria": criteria,
        "assets": {
            "background": schemas.AssetBase.from_orm(assets["background"]) if assets["background"] else None,
            "frame": schemas.AssetBase.from_orm(assets["frame"]) if assets["frame"] else None,
        },
        "text_content": assets["text_content"],
        "dimensions": assets["dimensions"]
    }
    
    return response

@app.get("/assets/view")
def view_asset(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Asset not found")
    return FileResponse(path)

class ExportRequest(BaseModel):
    assets: dict
    text_content: str

@app.post("/export")
def export_design(request: ExportRequest):
    # Generate a unique filename
    filename = f"design_{uuid.uuid4()}.svg"
    output_path = os.path.join("exports", filename)
    os.makedirs("exports", exist_ok=True)
    
    export_service.create_svg(request.assets, request.text_content, output_path)
    
    return FileResponse(output_path, filename=filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
