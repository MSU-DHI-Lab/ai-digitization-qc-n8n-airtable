from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import uvicorn
import time

app = FastAPI(
    title="Digitization QC Model API",
    description="AI-powered quality control for collections scans (demo placeholder).",
    version="0.1.0",
)

def dummy_quality_score(img: Image.Image) -> dict:
    """
    Placeholder logic.

    In a real deployment, replace this with a trained model:
    - Teachable Machine export
    - ONNX model served with onnxruntime
    - A call out to Vertex AI / Hugging Face / Gradient, etc.
    """
    width, height = img.size
    pixels = width * height

    if pixels >= 2000 * 3000:
        score = 92
        quality = "high"
        defects = {
            "finger_in_frame": False,
            "skew_degrees": 1.5,
            "blur": "none",
            "glare": False,
            "cutoff_edges": False,
        }
        reasons = ["Large image with sufficient resolution (placeholder heuristic)."]
    else:
        score = 55
        quality = "low"
        defects = {
            "finger_in_frame": False,
            "skew_degrees": 6.0,
            "blur": "mild",
            "glare": False,
            "cutoff_edges": True,
        }
        reasons = ["Image appears small or cropped (placeholder heuristic)."]

    return {
        "quality": quality,
        "score": score,
        "defects": defects,
        "reasons": reasons,
        "processed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

@app.post("/predict")
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
