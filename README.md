# AI-Powered Collections Digitization QC with n8n and Airtable

_Automating image quality control, metadata capture, and review for museums, libraries, and archives using AI and Airtable._

## 1. What this project is

This repository demonstrates a **realistic, AI-powered digitization workflow** for museums, libraries, and archives.

It combines:

- **AI computer vision** to automatically judge whether a scan is **high quality** or **low quality** (e.g., finger in frame, skew, blur, cutoff).
- **Airtable** as the **human-facing, flexible workspace** for metadata, review queues, and progress tracking.
- **n8n** as the **orchestrator** that connects file storage, the AI model, and Airtable into a coherent workflow.

The goal is to show how AI and Airtable can work together in a **practical collections context**, not just as isolated tools.

---

## 2. Who this is for

This project is written for:

- Museum, library, and archives professionals.
- Collections managers, registrars, and digitization coordinators.
- People who want to **experiment with AI** in digitization, but need a workflow that still feels grounded in collections practice.
- Teams that already use or are considering **Airtable** as a lightweight collections or project management tool.

You do **not** need to be a software engineer to understand the workflow. Technical details (Python, Docker, n8n nodes) can be handled by a collaborator, IT staff, or your future self.

---

## 3. Architecture overview

At a high level, the workflow looks like this:

1. **Scans arrive** in a shared folder (for example, OneDrive or a local network path).
2. **n8n** detects new files and sends each image to an **AI model API**.
3. The **AI model** returns a structured JSON verdict (quality, score, defects).
4. **n8n** writes the result and core metadata into an **Airtable base**, updating status fields and defect flags.
5. **Airtable** becomes the central place where staff:
   - See which scans passed or failed AI quality control.
   - Work from a “Needs Review” view for problem scans.
   - Track where each object is in the digitization pipeline.

### Components

- **File storage**
  - Where scanned images live (e.g., OneDrive, Google Drive, local NAS).
  - n8n is configured to watch or poll this location.

- **AI model service (`model-service/`)**
  - A small **FastAPI** app that exposes a `/predict` endpoint.
  - In this demo, the logic is placeholder; in real use you plug in a trained model
    (e.g., Teachable Machine export, ONNX model, or Vertex AI / Hugging Face endpoint).

- **n8n workflow (`n8n/workflow-digitization-qc.json`)**
  - Nodes for:
    - Detecting new scans.
    - Calling the AI model.
    - Branching on high vs low quality.
    - Updating Airtable records.
    - Optionally moving files and sending notifications.

- **Airtable base (`airtable/base-schema.md`)**
  - Table design for:
    - Logging every digitized object.
    - Storing AI quality scores and defect flags.
    - Representing workflow status (QC Pending, QC Passed, Needs Review, etc.).
    - Providing review queues via filtered views.

---

## 4. How AI is used in this project

This project is intentionally structured as an **AI experiment you can grow over time**:

- The **model-service** layer is where you plug in different computer vision approaches:
  - A simple image classifier trained in **Teachable Machine**, exported to TensorFlow or ONNX.
  - A more advanced model trained with PyTorch and exported to ONNX for cheap CPU inference.
  - A managed model hosted on **Vertex AI**, **Hugging Face**, or **DigitalOcean Gradient**, with the FastAPI service acting as a thin proxy.

- The AI model returns **structured JSON** describing:
  - `quality` (high / low)
  - `score` (0–100)
  - `defects` (finger in frame, skew, blur, glare, cutoff)
  - `reasons` (short textual explanation)

- n8n uses this JSON to:
  - Automatically decide whether a scan passes or fails AI QC.
  - Populate Airtable fields that collections staff can use directly (“Finger in frame”, “Blur level”, etc.).
  - Drive a **human-in-the-loop review** process for borderline or failed scans.

See `docs/ai-experiments-notes.md` for ideas on how to swap models, convert to ONNX, or move from a local container to a cloud-hosted endpoint.

---

## 5. How Airtable is used in this project

Airtable is the **central, human-readable system of record** in this workflow.

The base has a main table, for example **Digitized Objects**, with fields such as:

- `Object ID`
- `File name`
- `File path or URL`
- `Scan date`
- `Operator`
- `Status` (New Scan, QC Pending, QC Passed, QC Failed – Needs Review, Metadata Complete, Digitization Complete)
- `Quality` (High / Low — from AI)
- `Quality score`
- `Defects (text summary)`
- `Finger in frame` (checkbox)
- `Skew (degrees)`
- `Blur level` (None / Mild / Strong)
- `Glare present` (checkbox)
- `Cutoff edges` (checkbox)
- `Notes`

Airtable plays three roles:

1. **Master digitization log**  
   Every AI-checked scan becomes a row with quality and metadata.

2. **Review and correction queue**  
   Views like **Needs Review** filter to records where AI flagged problems (for example, `Status = "QC Failed – Needs Review"`).

3. **Workflow state machine**  
   The `Status` field shows where each object is in the pipeline; n8n updates this automatically as steps complete.

The Airtable schema is described in detail in `airtable/base-schema.md`.

---

## 6. Files in this repository

- `README.md`  
  You are here.

- `n8n/workflow-digitization-qc.json`  
  Example n8n workflow export. This is a template you can import and customize in your own n8n instance.

- `model-service/app.py`  
  A small FastAPI application that exposes a `/predict` endpoint for quality checking. In this demo, it uses placeholder logic; in practice you would attach a real computer vision model.

- `model-service/requirements.txt`  
  Python dependencies for the model service.

- `model-service/Dockerfile`  
  Container definition for running the model service (locally, on a NAS, or on a small cloud instance).

- `airtable/base-schema.md`  
  Step-by-step description of the Airtable base: fields, types, and recommended views.

- `data/sample_qc_output.json`  
  Example of the AI model’s JSON output.

- `data/sample_airtable_export.csv`  
  Example export from the Airtable table after a few records have been processed.

- `data/sample_input/README.md`  
  Notes about what sample input scans would look like (filenames, formats, etc.).

- `docs/ai-experiments-notes.md`  
  Notes on potential AI model variants, deployment options (ONNX, Vertex, Hugging Face, DigitalOcean), and how they would slot into this workflow.

---

## 7. Step-by-step setup (museum / library friendly)

### Step 1 — Set up the Airtable base

1. Sign into Airtable and create a **new base** named, for example, **Digitization QC Log**.
2. Follow `airtable/base-schema.md` to:
   - Create the **Digitized Objects** table.
   - Add the fields listed there.
   - Create at least:
     - An **All records** view.
     - A **Needs Review** view (filter on `Status = "QC Failed – Needs Review"`).
     - A **QC Passed** view.

You can do this entirely through Airtable’s web UI, no code required.

### Step 2 — Decide where scans will be stored

Pick one location for **new scans** to appear, such as:

- A folder on OneDrive / Google Drive that n8n can access, or
- A local or network folder if you are running n8n on-premises.

Staff should save new scans there. You do not have to change your existing naming convention to start using the workflow.

### Step 3 — Deploy the model service (AI layer)

If you are just demoing the workflow, you can use the placeholder service as-is.

Basic, non-technical summary:

1. Ask someone comfortable with Python or Docker to:
   - Install Python 3.11 (or similar).
   - Install requirements from `model-service/requirements.txt`.
   - Run `model-service/app.py` so it listens on a port (for example, `http://localhost:8000`).
2. Confirm you can open `http://<server>:8000/docs` in a web browser and see the FastAPI documentation.
3. The important part is the `/predict` endpoint URL; you’ll paste that into n8n.

Later, this same service can be replaced or extended to call a real model exported from Teachable Machine, ONNX, Vertex AI, or Hugging Face.

### Step 4 — Import and configure the n8n workflow

1. Open your n8n instance.
2. Create a new workflow and choose **Import from File**.
3. Select `n8n/workflow-digitization-qc.json` from this repository.
4. Update the nodes:
   - **Trigger node**: point it at the folder where new scans appear (e.g., your `IncomingScans` folder).
   - **Model API node**: set the URL to your AI model service’s `/predict` endpoint.
   - **Airtable node**:  
     - Add Airtable credentials.  
     - Select the base and table you created.  
     - Map fields from the AI model output and file metadata to the Airtable columns (Object ID, Quality, Defects, Status, etc.).

5. Save and activate the workflow.

### Step 5 — Test with a few scans

1. Drop a small number of test scans into your input folder.
2. Watch the n8n workflow run:
   - Confirm requests are hitting the model service.
   - Confirm records are appearing in Airtable with the expected values.
3. Open the **Needs Review** view in Airtable to see which scans AI flagged as low quality.

Once this works, you can iterate on:

- The AI model (better quality detection).
- The Airtable schema (more metadata fields).
- The n8n workflow (notifications, integration with project management tools).

---

## 8. How to position this project in an AI + Airtable application

This project gives you a concrete, inspectable artifact that shows:

- **AI experimentation** in a real workflow:
  - AI-powered image quality assessment for scans.
  - Structured JSON outputs used directly in a workflow engine (n8n).
  - Clear separation between model experiments and orchestration.

- **Airtable integration**:
  - Airtable as the central record for digitization status, AI results, and human review.
  - Practical examples of using Airtable as a workflow state machine and review hub.
  - A schema designed specifically for collections and digitization contexts.

- **Glue code and orchestration**:
  - n8n workflow JSON demonstrating how to connect file storage, AI services, and Airtable.
  - A small, inspectable FastAPI service that can be swapped to different AI backends.

You can point reviewers directly to:

- `model-service/app.py` and `docs/ai-experiments-notes.md` for the AI side.
- `airtable/base-schema.md` and `n8n/workflow-digitization-qc.json` for the Airtable-integrated workflow.
