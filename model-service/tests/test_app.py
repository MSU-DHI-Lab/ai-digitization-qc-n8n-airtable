from fastapi.testclient import TestClient
from PIL import Image
import io
import sys
import os

# Allow test runs without a token
os.environ.setdefault("ALLOW_NO_TOKEN", "true")

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)

def create_dummy_image(width, height):
    img = Image.new('RGB', (width, height), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "model-service"}

def test_predict_high_quality():
    # Create large image (high quality)
    img_bytes = create_dummy_image(2000, 3000)
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    
    response = client.post("/predict", files=files)
    assert response.status_code == 200
    data = response.json()
    
    assert data["quality"] == "high"
    assert data["score"] == 92
    assert "rich_text_report" in data
    assert "semantic_tags" in data
    assert "High Res" in data["semantic_tags"]

def test_predict_low_quality():
    # Create small image (low quality)
    img_bytes = create_dummy_image(100, 100)
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    
    response = client.post("/predict", files=files)
    assert response.status_code == 200
    data = response.json()
    
    assert data["quality"] == "low"
    assert data["score"] == 55
    assert "Low Res" in data["semantic_tags"]

def test_invalid_file_type():
    files = {'file': ('test.txt', b'not an image', 'text/plain')}
    response = client.post("/predict", files=files)
    assert response.status_code == 400
    assert "File must be one of" in response.json()["detail"]
