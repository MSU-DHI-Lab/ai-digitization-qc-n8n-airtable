# AI Experiments - Digitization QC Model

Use this file to track model options for image-quality checks in collections workflows.

## Model variants to try

- Teachable Machine -> TensorFlow / ONNX  
  Train a high/low quality classifier in Teachable Machine, export TensorFlow, convert to ONNX, and load in `model-service/app.py`.

- Custom PyTorch / ONNX model  
  Train on your own labeled scans, export to ONNX, and run inference on CPU with `onnxruntime`.

- Cloud-hosted models  
  Use a hosted vision endpoint (for example Vertex AI, Hugging Face, or DigitalOcean Gradient) and adapt `model-service/app.py` to proxy `/predict` requests.

## Why ONNX is useful here

- Portable: one model artifact can run on local hardware, cloud VMs, or containers.
- Efficient: good CPU performance for institutions without GPU infrastructure.

## Connecting AI to Airtable

The model output should stay aligned with Airtable fields:

- quality decision (`quality`)
- numeric score (`score`)
- defect flags (`defects`)
- human-readable rationale (`reasons`)

Keeping the output schema stable makes automation and staff review simpler.
