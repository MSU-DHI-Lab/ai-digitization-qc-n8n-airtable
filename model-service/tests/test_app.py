from fastapi.testclient import TestClient
from PIL import Image
import io
import sys
import os
import importlib
from contextlib import contextmanager

# Allow test runs without a token
os.environ.setdefault("ALLOW_NO_TOKEN", "true")

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)

def create_dummy_image(width, height, format='JPEG'):
    img = Image.new('RGB', (width, height), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    return img_byte_arr


def post_predict(test_client, filename, content_type, img_bytes):
    files = {'file': (filename, img_bytes, content_type)}
    return test_client.post("/predict", files=files)


def assert_security_headers(response):
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert response.headers.get("referrer-policy") == "no-referrer"
    assert response.headers.get("cache-control") == "no-store"


def _set_env_vars(overrides):
    originals = {}
    for key, value in overrides.items():
        originals[key] = os.environ.get(key)
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    return originals


def _restore_env_vars(originals):
    for key, value in originals.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@contextmanager
def reloaded_client(overrides):
    originals = _set_env_vars(overrides)
    try:
        import app as app_module
        app_module = importlib.reload(app_module)
        yield TestClient(app_module.app), app_module
    finally:
        _restore_env_vars(originals)
        import app as app_module
        app_module = importlib.reload(app_module)
        global client
        client = TestClient(app_module.app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "model-service"}
    assert_security_headers(response)

def test_predict_high_quality():
    # Create large image (high quality)
    img_bytes = create_dummy_image(2000, 3000)
    response = post_predict(client, 'test.jpg', 'image/jpeg', img_bytes)
    assert response.status_code == 200
    assert_security_headers(response)
    data = response.json()
    
    assert data["quality"] == "high"
    assert data["score"] == 92
    assert "rich_text_report" in data
    assert "semantic_tags" in data
    assert "High Res" in data["semantic_tags"]

def test_predict_low_quality():
    # Create small image (low quality)
    img_bytes = create_dummy_image(100, 100)
    response = post_predict(client, 'test.jpg', 'image/jpeg', img_bytes)
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

def test_predict_with_png():
    """Test that PNG images are accepted."""
    img_bytes = create_dummy_image(2000, 3000, format='PNG')
    response = post_predict(client, 'test.png', 'image/png', img_bytes)
    assert response.status_code == 200
    data = response.json()
    assert data["quality"] == "high"

def test_predict_response_structure():
    """Test that the response contains all expected fields."""
    img_bytes = create_dummy_image(2000, 3000)
    response = post_predict(client, 'test.jpg', 'image/jpeg', img_bytes)
    assert response.status_code == 200
    data = response.json()
    
    # Check all required fields exist
    assert "quality" in data
    assert "score" in data
    assert "defects" in data
    assert "reasons" in data
    assert "rich_text_report" in data
    assert "semantic_tags" in data
    assert "processed_at" in data
    
    # Check defects structure
    defects = data["defects"]
    assert "finger_in_frame" in defects
    assert "skew_degrees" in defects
    assert "blur" in defects
    assert "glare" in defects
    assert "cutoff_edges" in defects

def test_invalid_image_data():
    """Test handling of corrupt/invalid image data."""
    files = {'file': ('test.jpg', b'not valid image data', 'image/jpeg')}
    response = client.post("/predict", files=files)
    assert response.status_code == 400
    assert "Invalid image file" in response.json()["detail"]

def test_rich_text_report_format():
    """Test that the rich text report is properly formatted markdown."""
    img_bytes = create_dummy_image(2000, 3000)
    response = post_predict(client, 'test.jpg', 'image/jpeg', img_bytes)
    assert response.status_code == 200
    data = response.json()
    
    report = data["rich_text_report"]
    assert "## " in report  # Has markdown headers
    assert "AI Analysis" in report
    assert "Generated by AI Model Service" in report

def test_authentication_required():
    """Test that authentication is enforced when token is set."""
    with reloaded_client({"MODEL_API_TOKEN": "test-secret-token", "ALLOW_NO_TOKEN": "false"}) as (test_client, _):
        img_bytes = create_dummy_image(100, 100)

        # Request without token should fail
        response = post_predict(test_client, 'test.jpg', 'image/jpeg', img_bytes)
        assert response.status_code == 401
        assert_security_headers(response)

        # Request with wrong token should fail
        response = test_client.post(
            "/predict",
            files={'file': ('test.jpg', img_bytes, 'image/jpeg')},
            headers={"x-api-token": "wrong-token"},
        )
        assert response.status_code == 401

        # Request with correct token should succeed
        response = test_client.post(
            "/predict",
            files={'file': ('test.jpg', img_bytes, 'image/jpeg')},
            headers={"x-api-token": "test-secret-token"},
        )
        assert response.status_code == 200


def test_content_type_mismatch_rejected():
    """Reject files where declared content-type and actual format differ."""
    img_bytes = create_dummy_image(2000, 2000, format='PNG')
    response = post_predict(client, 'test.png', 'image/jpeg', img_bytes)
    assert response.status_code == 400
    assert "content type" in response.json()["detail"].lower()


def test_rejects_file_over_max_upload_mb():
    """Reject uploads that exceed MAX_UPLOAD_MB."""
    with reloaded_client({"MAX_UPLOAD_MB": "0.001"}) as (test_client, _):  # ~1KB
        img_bytes = create_dummy_image(2000, 2000, format='PNG')
        response = post_predict(test_client, 'big.png', 'image/png', img_bytes)
        assert response.status_code == 413


def test_internal_error_sanitized(monkeypatch):
    """Internal errors should not leak implementation details."""
    with reloaded_client({}) as (test_client, app_module):
        def boom(_):
            raise RuntimeError("simulated failure detail")

        monkeypatch.setattr(app_module, "dummy_quality_score", boom)

        img_bytes = create_dummy_image(2000, 3000)
        response = post_predict(test_client, 'test.jpg', 'image/jpeg', img_bytes)
        assert response.status_code == 500
        assert "internal processing error" in response.json()["detail"].lower()


def test_rejects_when_pixel_count_exceeds_limit():
    """Reject images that exceed configured pixel budget."""
    with reloaded_client({"MAX_PIXELS": "10000"}) as (local_client, _):  # very small limit
        img_bytes = create_dummy_image(200, 200)  # 40k pixels
        response = post_predict(local_client, 'test.jpg', 'image/jpeg', img_bytes)
        assert response.status_code == 413
        assert "dimensions exceed" in response.json()["detail"].lower()


def test_invalid_max_upload_mb_falls_back_to_default():
    with reloaded_client({"MAX_UPLOAD_MB": "-1"}) as (local_client, app_module):
        img_bytes = create_dummy_image(100, 100)
        response = post_predict(local_client, 'small.jpg', 'image/jpeg', img_bytes)
        assert response.status_code == 200
        assert app_module.MAX_UPLOAD_MB == app_module.DEFAULT_MAX_UPLOAD_MB


def test_invalid_max_pixels_falls_back_to_default():
    with reloaded_client({"MAX_PIXELS": "0"}) as (local_client, app_module):
        img_bytes = create_dummy_image(100, 100)
        response = post_predict(local_client, 'small.jpg', 'image/jpeg', img_bytes)
        assert response.status_code == 200
        assert app_module.MAX_PIXELS == app_module.DEFAULT_MAX_PIXELS


def test_auth_uses_constant_time_compare(monkeypatch):
    with reloaded_client({"MODEL_API_TOKEN": "test-secret-token", "ALLOW_NO_TOKEN": "false"}) as (local_client, app_module):
        compare_calls = {"count": 0}

        def fake_compare(lhs, rhs):
            compare_calls["count"] += 1
            return lhs == rhs

        monkeypatch.setattr(app_module.hmac, "compare_digest", fake_compare)

        img_bytes = create_dummy_image(100, 100)
        response = local_client.post(
            "/predict",
            files={'file': ('test.jpg', img_bytes, 'image/jpeg')},
            headers={"x-api-token": "test-secret-token"},
        )
        assert response.status_code == 200
        assert compare_calls["count"] == 1
        assert_security_headers(response)
