# AI-Powered Collections Digitization QC with n8n and Airtable

_Automating image quality control, metadata capture, and review for museums, libraries, and archives using AI and Airtable._

## 1. What this project is

This repository demonstrates a realistic, AI-powered digitization workflow for museums, libraries, and archives.

It combines:

- AI computer vision to automatically judge whether a scan is high quality or low quality (for example, finger in frame, skew, blur, cutoff).
- Airtable as the human-facing, flexible workspace for metadata, review queues, and progress tracking.
- n8n as the orchestrator that connects file storage, the AI model, and Airtable into a coherent workflow.

The goal is to show how AI and Airtable can work together in a practical collections context, not just as isolated tools.

### Architecture (high level)

At a high level, the workflow looks like this:

1. A new scan is saved into a watched folder.
2. n8n detects the new file and sends the image to the AI model service.
3. The AI model returns a structured JSON verdict (quality, score, defects, reasons).
4. n8n writes the result into Airtable, updates status fields, and (optionally) moves the file.
5. Collections staff work entirely from Airtable views and Interfaces for review, correction, and reporting.

Files are routed through three folders: `data/incoming/` (drop folder), `data/processed/` (AI passed), and `data/failed/` (AI failed or error).

Airtable is the main place where humans work. AI and n8n run in the background to reduce manual screening and keep quality consistent at scale.

## 2. Project context (the “why”)

The Challenge: our lab faced a backlog of thousands of physical objects requiring digitization. Our existing process was manual, prone to human error, and difficult to scale. We needed a workflow that ensured consistent quality standards and reproducibility without slowing down our human operators.

The Solution: we built this “force multiplier” workflow. By offloading the rote visual inspection to AI, we increased throughput and ensured that every single scan met our baseline quality metrics before a human ever had to review it.

### Why Airtable?

We chose Airtable as the core platform because it sits at the intersection of a relational database and a project management tool.

- Relational structure: unlike a spreadsheet, we can properly model relationships (Objects ↔ Scans ↔ Defects).
- Low-code Interfaces: we can build custom, drag-and-drop Interfaces for student workers and staff so they do not have to interact with raw data tables or learn SQL.
- API-first: Airtable’s API allows seamless integration with our AI model service and n8n orchestrator.

In practice, Airtable gave us much of the structure of a dedicated DAM system while preserving the flexibility to iterate on our metadata schema as the project evolved.

### Project origin

This workflow was developed in the Digital Heritage Innovation Lab at Michigan State University as part of a collections scalability initiative. Our team used Airtable as the operational hub for digitization quality control, integrating it with a lab-hosted AI service and an n8n instance already in use for other research and teaching workflows. The repository reflects that lab implementation in a cleaned-up, shareable form.

## 3. Architecture overviews

### AI quality control

The system automatically checks every scan for common issues such as:

- Fingers in frame
- Skew or rotation
- Blur
- Cutoff edges

The AI service does not make final curatorial decisions. Instead, it flags potential problems and assigns a score that helps staff prioritize which scans need attention.

> Note: the default model logic in this repo is a simple resolution-based placeholder to keep the workflow runnable. Replace it with your trained model before relying on results.

### AI-generated reports (Airtable Rich Text)

Instead of a simple pass or fail checkbox, the AI generates a short, structured explanation for every image. This maps directly to an Airtable Rich Text field, giving curators and digitization staff a clear, readable summary of why an image passed or failed the automated checks.

### Semantic auto-tagging

The AI can suggest content tags such as “High Res”, “Sepia”, or “Handwritten” to jumpstart metadata work. These map to Airtable multi-select fields, making it easy to refine or override the suggestions over time.

### “Interface-first” design

The data schema is designed to power Airtable Interfaces. The lab uses Interfaces as a “digitization command center” where staff can:

- See new scans entering the system.
- Filter to items that AI has flagged for review.
- Track progress across boxes, collections, or operators.

The repository includes written guidance for building an interface of this type, so teams can adapt it to their own collections and digitization goals.

## 4. Files in this repository

- README.md: you are here.
- n8n/workflow-digitization-qc.json: the orchestration logic to import into n8n.
- model-service/:
  - app.py: FastAPI application that exposes the AI quality control API.
  - Dockerfile: container definition for running the model service.
  - requirements.txt: Python dependencies for the model service.
- airtable/:
  - base-schema.md: how to set up your Airtable base and fields.
  - interface-design.md: guide to building a review and monitoring interface in Airtable.
- data/:
  - sample_qc_output.json: example of the structured JSON response from the AI service.
  - sample_airtable_export.csv: example Airtable export after several scans have been processed.
  - sample_input/: notes on what example input scans look like.
- docs/:
  - ai-experiments-notes.md: notes on model variants, ONNX, and possible cloud-hosted deployments.

## 5. Quick Start (Docker Compose)

The easiest way to run the entire system is with Docker Compose. This will start both the AI model service and n8n in a connected network.

1.  **Configure Environment:**
    Copy the example environment file and fill in your Airtable details.
    ```bash
    cp .env.example .env
    # Edit .env with your Base ID
    # Optional: set MODEL_API_TOKEN to lock down the model API
    ```

2.  **Start the services:**
    ```bash
    docker-compose up -d
    ```

3.  **Access n8n:**
    Open your browser to `http://localhost:5678`.

4.  **Configure the Workflow:**
    - Import `n8n/workflow-digitization-qc.json`.
    - The workflow is pre-configured to use the Docker service name and your `.env` variables.
    - You will still need to authenticate the Airtable node with your API Key (n8n Credential).

5.  **Test:**
    - Drop an image into `data/incoming/`.
    - Watch the workflow execute. Successful files are moved to `data/processed/`; failures go to `data/failed/`.
    - The included AI logic is a placeholder resolution check, not a production model. Swap in your own model (see docs/ai-experiments-notes.md) for real QC.
    - The stack pins n8n to a specific tag to avoid breaking changes (`n8nio/n8n:1.61.4`). Update deliberately when you are ready to upgrade.

## 6. Step-by-step setup (Manual)

This section is written for collections staff, registrars, and project managers who may not consider themselves technical specialists. You do not need to write code to understand the workflow, but you may want a colleague or IT partner to help with the server and container pieces.

### Step 1 — Set up the Airtable base

1. Sign into Airtable and create a new base.
2. Follow airtable/base-schema.md to create the table and fields.
3. Optionally, read airtable/interface-design.md to see how to build a review interface for your team.

### Step 2 — Start the AI service

This step is often handled by IT staff or a technically comfortable collaborator.

1. From the model-service directory, install dependencies from requirements.txt or build the Docker image.
2. Run the service so it listens on a known port (for example, port 8000 on an internal server or development machine).
3. Check the service health endpoint or documentation page in a browser to confirm it is running.

The exact commands depend on your environment. They are intentionally simple so that a small team can host the AI service alongside other lab tools.

### Step 3 — Configure n8n

1. Import n8n/workflow-digitization-qc.json into your n8n instance.
2. Update the trigger node so it watches the folder where new scans are saved.
3. Point the AI node to your model service endpoint.
4. Configure the Airtable node with your Airtable API key, base, and table, and map fields to match your base-schema.md configuration.
   - If running via Docker Compose, keep the default `http://model-service:8000/predict` URL.
   - If running the model locally without Compose, change the HTTP node to `http://localhost:8000/predict` (or your host/port).
5. In n8n, create an Airtable credential (Personal Access Token or legacy API key) and select it in the Airtable node; the `.env` file only supplies Base ID/Table Name.

### Step 4 — Digitize and review

Once everything is connected:

1. Drop a test scan into the watched folder.
2. Wait for the workflow to run. The image is sent to the AI service, evaluated, and recorded in Airtable.
3. Open Airtable and confirm that a new record appears with:
   - The object or file identifier
   - Quality score and simple quality label
   - Defect flags
   - A short text explanation
4. Use Airtable views and Interfaces to monitor new scans and identify items that need manual review or rescanning.

## 7. For developers

For teams that want to extend or harden this workflow, the repository can be used as a starting point.

- The model service is built with FastAPI and organized so that a real computer vision model (for example, a Teachable Machine export, ONNX model, or cloud-hosted model) can be swapped in.
- The container definition is suitable for running the model service on a small VM, NAS, or on-premises server.
- The data examples demonstrate how the AI output is shaped so it can be written directly into Airtable via n8n.
- The model API supports an optional `MODEL_API_TOKEN` shared secret and upload limits (`MAX_UPLOAD_MB`, `MAX_PIXELS`) to keep the service safe in multi-tenant or shared environments.

### Local development and tests

```bash
cd model-service
pip install -r requirements.txt
pytest
```

Recommended environment defaults: `MODEL_API_TOKEN` set to a non-empty secret, `MAX_UPLOAD_MB=10`, `MAX_PIXELS=35000000`. If you expose n8n publicly, enable basic auth in `.env` (`N8N_BASIC_AUTH_ACTIVE=true`, user/pass set).

This makes it straightforward to experiment with different models or hosting environments while keeping Airtable and n8n configuration stable.

## 8. What is implemented today

The current version of this project includes:

- An n8n workflow template that:
  - Watches a scan folder.
  - Sends images to the AI service.
  - Receives quality results.
  - Writes records into Airtable.
- A model service implementation that:
  - Exposes a simple HTTP API for image quality checks.
  - Returns structured JSON suitable for direct Airtable mapping.
- An Airtable base schema that:
  - Stores object identifiers, quality scores, defect flags, and workflow status.
  - Supports filtered views such as “Needs Review” and “QC Passed”.
- Example data artifacts:
  - Sample AI output.
  - Sample Airtable export from test runs.
  - A description of sample input scans.

These components were used together in the Digital Heritage Innovation Lab to support a real digitization backlog and are now published in this repository in a form that other teams can adapt.

## 9. Future directions

While this project represents a working version of the workflow, there are clear opportunities to extend it using additional AI and Airtable features. The ideas below are future enhancements and may not all be implemented in the current repository.

1. Generative metadata description  
   Idea: connect a large language model to the n8n workflow.  
   Value: have the AI write a short, human-friendly description of each object (for example, “A sepia-toned photograph of a family standing in front of a 1920s farmhouse”) and store it in a long text field in Airtable.

2. Automated OCR pipeline  
   Idea: add a Tesseract or cloud vision node to the n8n workflow.  
   Value: automatically extract text from documents and store it in Airtable for full-text search and downstream analysis.

3. Public search and discovery  
   Idea: use Airtable Interfaces to create a read-only, public-facing view of the records that have passed quality control.  
   Value: publish a browsable slice of the digitized collection to researchers and community partners without building a separate website.

These directions are intentionally aligned with Airtable’s strengths: relational modeling, Interfaces, and API-friendly integration with AI services.
