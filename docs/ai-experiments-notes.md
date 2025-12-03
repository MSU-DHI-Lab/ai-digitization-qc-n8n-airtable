# AI Experiments – Digitization QC Model

This project is designed as a small laboratory for experimenting with AI-powered image quality checking in a collections context.

## Model variants to try

- Teachable Machine → TensorFlow / ONNX  
  Train a simple high/low quality classifier in Teachable Machine. Export as TensorFlow, convert to ONNX, and load it in model-service/app.py.

- Custom PyTorch / ONNX model  
  Train on your own dataset (e.g., high/low quality scans with labels for defects). Export to ONNX and run it with onnxruntime for fast CPU inference.

- Cloud-hosted models  
  Use Vertex AI, Hugging Face, or DigitalOcean Gradient to host a vision model. Adapt model-service/app.py to proxy /predict requests to that endpoint.

## Why ONNX is useful here

- Portable: the same model can run locally on a NAS, a small cloud VM, or in a container platform.
- Efficient: good performance on CPU-only hardware, which is common in museums, libraries, and archives.

## Connecting AI to Airtable

The key design choice in this project is that the AI model always returns structured JSON that fits directly into Airtable fields:

- Binary judgment: quality
- Score: score
- Defect flags: defects object
- Human-friendly explanations: reasons

This makes the AI output immediately useful to collections staff, without requiring them to read raw logs or developer-centric dashboards.
