# Digitization Quality Control Automation Workflow (AI + n8n + Airtable)

[![Docker Pulls](https://img.shields.io/docker/pulls/watrall/ai-digitization-qc-model?logo=docker&logoColor=white)](https://hub.docker.com/r/watrall/ai-digitization-qc-model)

Digitization projects generate a lot of image files, and each one needs a quick quality check before it can move into description, metadata work, and long-term preservation. When you are working through a backlog, that review step can become the bottleneck, especially when issues like blur, skew, cropped edges, uneven lighting, or an accidental hand in the frame only show up after the scan is already in the queue.

This repository documents a digitization quality control workflow developed in the Digital Heritage Innovation Lab at Michigan State University. The basic routine is simple.

- Staff place new scans into an “incoming” folder.
- The system runs an automated first-pass check for common capture problems.
- The results land in Airtable as an easy-to-read record that includes the image, any detected issues, and suggested next steps.

From there, the Airtable Interfaces guide staff through triage and review so they can approve clean scans, flag items that should be rescanned, and track progress without having to touch the automation tools behind the scenes.

In the background, n8n handles the file watching and the handoffs, and a lightweight computer vision service provides the automated checks. Staff still make the final call. The automation reduces repetitive visual screening and helps keep review work more consistent and easier to manage. We moved the workflow to GitHub so museums, archives, libraries, and other cultural heritage organizations can reuse it as it is or adapt it to their own digitization setups.

## Fast Start (Copy/Paste)

This quick start is designed for users who can run Docker Desktop but do not want to manage Python or Node setup.

```bash
git clone https://github.com/MSU-DHI-Lab/ai-digitization-qc-n8n-airtable.git && cd ai-digitization-qc-n8n-airtable
cp .env.example .env
docker compose up -d
```

After startup:

- n8n is available at http://localhost:5678  
- Model service health check is available at http://localhost:8000/health  
- Before production use, edit `.env` and set `AIRTABLE_PAT`, `AIRTABLE_BASE_ID`, and `MODEL_API_TOKEN`

## What You Need Before You Begin

This workflow is designed to be usable by non-technical collections staff once a small amount of initial setup is completed by someone comfortable with basic IT tasks. Before starting, you will need:

1. A designated folder on a workstation, server, shared drive, or mounted cloud drive where staff will place new scans.  
2. An Airtable account (free or paid) and permission to create a base.  
3. A machine capable of running n8n and the lightweight AI model.  
4. An Airtable Personal Access Token.  
5. Basic IT support to install and run n8n and the AI service if staff are not comfortable doing so.  

After setup is complete, day-to-day staff work exclusively in Airtable.

## How the System Works

1. Staff place new scans into the incoming folder.  
2. n8n detects each new file and sends it to the AI service.  
3. The AI service evaluates the image and returns structured results.  
4. n8n writes these results into Airtable and moves the file to a processed or failed folder.  
5. Staff complete review and decision-making directly in Airtable using Interfaces.

This workflow allows staff to remain inside Airtable, while automation handles the technical steps.

## Where the Incoming Folder Lives

The incoming folder can be located on:

- A local workstation  
- A shared network drive  
- A NAS device such as Synology  
- A mounted OneDrive, SharePoint, or Dropbox directory  

The only requirement is that n8n must be able to access the folder. This is the entry point of the workflow.

## Why Airtable

Airtable was chosen because it aligns well with how collections teams work:

- Relational tables fit object and scan metadata.  
- Interfaces enable simple, guided review workflows.  
- Staff need minimal training to use it effectively.  
- The schema is flexible and can evolve over time.  
- The Airtable API integrates smoothly with n8n and the AI model.

In practice, Airtable is the command center for this workflow.

## What Is n8n and Why We Use It

n8n is an open-source automation tool that connects systems and runs background workflows. In this project, n8n:

- Watches the incoming folder  
- Sends images to the AI service  
- Updates Airtable records with results  
- Routes files into processed or failed folders  

n8n can run on a local computer, a small server, a NAS, or a cloud instance. Staff do not access n8n directly.

## The AI Quality Control Service

The AI service uses a lightweight computer vision model that runs through Docker or ONNX Runtime. It does not require a GPU and can run on basic hardware. It generates:

- A quality score  
- Detected defects  
- A short explanation of issues  
- Suggested next steps  

Institutions may use the provided model or replace it with a custom-trained model later.

## Architectural Overview

### AI Quality Control Service  
Analyzes images and returns structured quality assessments.

### n8n Orchestration  
Automates file monitoring, AI requests, and Airtable updates.

### Airtable Base and Interfaces  
Stores all scan records, AI results, workflow statuses, and metadata; supports review through simple, structured Interfaces.

## Repository Contents

model-service  
Minimal Python-based computer vision service

n8n/workflow-digitization-qc.json  
Complete n8n workflow definition

base-schema.md  
Airtable base schema and field descriptions

interface-design.md  
Airtable Interface layouts and user guidance

ai-experiments-notes.md  
Notes from model testing and ONNX experiments

docker-compose.yml  
Known-good container deployment with version-pinned images

README.md  
This documentation

## Airtable Base Structure

Fields fall into three categories:

### Automatically generated by AI  
Quality score, defect flags, explanation text, suggested next steps.

### Automatically populated by n8n  
File name, file path, workflow status, timestamps.

### Entered or confirmed by staff  
Object ID or catalog number, operator metadata, final review decision, notes.

This structure makes the division of responsibility clear for staff and automation.

## Airtable Interface Design

Interfaces provide streamlined, non-technical views tailored for:

- Triage of new scans  
- Detailed review of flagged items  
- Progress monitoring and throughput tracking  

These Interfaces were refined with real staff and student workers and reduce cognitive load during high-volume review.

## Known-Good Container Tags

- `MODEL_SERVICE_IMAGE=watrall/ai-digitization-qc-model:v0.1.0`  
- `N8N_IMAGE=n8nio/n8n:1.61.4`  

These tags are pinned on purpose. Avoid using `latest` in production.

## Quick Start for Developers

1. Clone the repository and copy `.env.example` to `.env`.  
2. Fill in Airtable credentials and set a strong `MODEL_API_TOKEN` in `.env`.  
3. Start services with `docker compose up -d`.  
4. Import `n8n/workflow-digitization-qc.json` into n8n and configure credentials.

## Quick Start for Non-Technical Teams

Once initial setup is complete:

1. Place new scans in the incoming folder.  
2. Review AI-generated results in the Airtable Interface.  
3. Approve scans or request rescans.  
4. Add or confirm metadata fields as required.  

Staff do not need to interact with n8n or the AI service.

## What Is Implemented Today

- AI-based image defect detection  
- Automated Airtable record creation and updating  
- Automated file routing  
- Interfaces for structured triage and review  
- Basic metadata suggestions from the AI  

The system has been tested on thousands of images in real lab conditions.

## Future Enhancements

Potential enhancements include:

- Collection-specific AI models  
- More advanced metadata extraction  
- Batch review capabilities  
- Integrations with OneDrive, S3, or DAMS platforms  
- Deployment templates for partner institutions  

## Collaboration and Reuse

This repository is open for reuse and adaptation. Cultural heritage organizations often face similar digitization challenges, and this workflow aims to provide a practical foundation. We welcome feedback and collaboration as others build on this framework.
