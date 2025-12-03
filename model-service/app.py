from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
import io
import uvicorn
import time

app = FastAPI(
    title="Digitization QC Model API",
    description="AI-powered quality control for collections scans (demo placeholder).",
    version="0.1.0",
)

# --- Pydantic Models for Data Contract ---

class Defects(BaseModel):
    finger_in_frame: bool
    skew_degrees: float
    blur: str  # "none", "mild", "strong"
    glare: bool
    cutoff_edges: bool

class QualityResponse(BaseModel):
    quality: str  # "high", "low"
    score: int    # 0-100
    defects: Defects
    reasons: List[str]
    processed_at: str

# --- Core Logic ---

def dummy_quality_score(img: Image.Image) -> QualityResponse:
    """
    Placeholder logic.
    In a real deployment, replace this with a trained model.
    """
    width, height = img.size
    pixels = width * height

    # Default to "high quality" values
    is_high_quality = (pixels >= 2000 * 3000)
    
    if is_high_quality:
        return QualityResponse(
            quality="high",
            score=92,
            defects=Defects(
                finger_in_frame=False,
                skew_degrees=1.5,
                blur="none",
                glare=False,
                cutoff_edges=False,
            ),
            reasons=["Large image with sufficient resolution (placeholder heuristic)."],
            processed_at=time.strftime("%Y-%m-%dT%H:%M:%S")
        )
    else:
        return QualityResponse(
            quality="low",
            score=55,
            defects=Defects(
                finger_in_frame=False,
                skew_degrees=6.0,
                blur="mild",
                glare=False,
                cutoff_edges=True,
            ),
            reasons=["Image appears small or cropped (placeholder heuristic)."],
            processed_at=time.strftime("%Y-%m-%dT%H:%M:%S")
        )

# --- API Endpoints ---

@app.post("/predict", response_model=QualityResponse)
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as exc:
        return JSONResponse(
            status_code=400,
            content={"error": f"Could not read image: {exc}"},
        )

    result = dummy_quality_score(img)
    return result

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
