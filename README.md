# AI-Powered Digitization Quality Control Workflow  
A practical, lab-developed system that integrates AI, Airtable, and n8n to support large-scale collections digitization.

## Overview

This project documents a real digitization quality control workflow developed and deployed in our research lab at Michigan State University. The system supports staff working through a large backlog of scans across multiple collections, many requiring consistent quality review before entering long-term metadata and preservation pipelines.

We moved this workflow to GitHub to make it transparent, reusable, and adaptable for museums, archives, libraries, and cultural heritage organizations facing similar challenges. Everything in this repository reflects a working implementation that evolved through direct use, staff feedback, and several iterations of schema, interface, and automation design.

Airtable serves as the operational home for review, triage, and metadata handling. AI provides first-pass quality assessment, and n8n coordinates movement between systems. The goal is a practical, human-centered pipeline where automation reduces repetitive tasks while staff retain full oversight and curatorial decision-making.

## How the System Works

1. A new digitized image is placed in an incoming folder monitored by n8n.
2. n8n sends the file to a lightweight AI model service that evaluates image quality and detects issues such as blur, skew, cutoff edges, or hands in the frame.
3. The AI returns structured JSON containing defect flags, an overall quality rating, and a brief explanation.
4. n8n writes these results into Airtable, updates workflow statuses, and moves the file to processed or failed folders.
5. Staff complete all human review and metadata refinement inside Airtable using curated views and Interfaces designed specifically for non-technical users.

This setup allows AI to handle repetitive first-pass analysis while Airtable provides the structured, reliable workspace staff use every day.

## Why Airtable

Airtable became the natural home for this project because it matched the way collections staff already work:

- A relational structure well suited to object and scan metadata.
- Views and Interfaces that let us design role-specific workflows.
- A clean, intuitive UI that minimizes training needs for non-technical staff.
- A robust API that integrates easily with n8n and the AI service.
- A flexible schema that can evolve as digitization practices change.

In practice, Airtable functioned as the command center for the entire workflow. Every human decision, correction, approval, and status update happened there.

## Architectural Overview

### AI Quality Control Service  
A lightweight model hosted via Docker or ONNX Runtime that reads each image and returns:
- Quality rating  
- Detected defects  
- Explanation text  
- Recommended next steps

The model was tuned using real digitization output from our lab.

### n8n Orchestration  
n8n connects the file system, AI service, and Airtable. It manages:
- File detection  
- Error handling  
- API calls  
- Structured record updates  
- Folder transitions for incoming, processed, and failed scans

Staff never interact with n8n directly; all automation runs silently in the background.

### Airtable Base and Interfaces  
Airtable stores all scan records, AI results, review statuses, and metadata fields.  
Interfaces provide:
- A triage screen for quick review  
- A detailed review screen for high-flag items  
- Dashboards for throughput and rescan monitoring  

These Interfaces became the daily workspace for student workers and staff during the pilot.

## Repository Contents

ai-service/  
Minimal computer vision service (Python)

n8n-workflow.json  
Complete n8n workflow exported as JSON

base-schema.md  
Airtable table structure and field definitions

interface-design.md  
Airtable Interface specifications and recommended layouts

ai-experiments-notes.md  
Notes from training experiments and ONNX testing

docker-compose.yml  
Optional container configuration for local deployment

README.md  
This documentation

All files represent working components used in our lab.

## Airtable Base Structure

The full schema is documented in base-schema.md. It includes:

- Core scan records  
- AI-generated fields  
- Reviewer workflows  
- Metadata enrichment fields  
- Status and lifecycle fields  

The schema evolved through several iterations based on real staff use.

## Airtable Interface Design

Details are in interface-design.md. Interfaces were created to keep the workflow approachable and efficient for non-technical users. They include:

- Triage view for incoming scans  
- Review screens for high-flag items  
- Dashboards for monitoring project progress  

Interfaces significantly reduced cognitive load and made the workflow easier for staff and student workers.

## Quick Start for Developers

### 1. Clone the repository  
git clone https://github.com/MSU-DHI-Lab/ai-digitization-qc-n8n-airtable.git

### 2. Configure environment variables  
Set your Airtable Personal Access Token, Base ID, Table ID, and AI service URL.

### 3. Run the AI service (optional)  
docker compose up --build

### 4. Import the n8n workflow  
Load n8n-workflow.json into your n8n instance and update credentials.

A detailed, step-by-step guide is included in the documentation.

## Quick Start for Non-Technical Teams

Once initial setup is complete, staff work entirely in Airtable.

1. Prepare your Airtable base using the provided schema.  
2. Create the recommended views and Interfaces.  
3. Confirm your folder structure: incoming, processed, failed.  
4. Use the provided n8n workflow with minimal modification.  
5. Begin digitizing and watch records populate automatically in Airtable.

## What Is Implemented Today

- AI-based defect detection and quality scoring  
- Automated record creation and updates in Airtable  
- Automated file transitions between states  
- Airtable Interfaces for triage, review, and monitoring  
- Basic metadata suggestions from the AI model  

The workflow has processed thousands of test and production images in our lab.

## Future Enhancements

Planned or active areas of development include:

- Improved defect models tuned to specific collection types  
- More advanced metadata extraction  
- Batch review Interfaces  
- Integrations with OneDrive, S3, or institutional DAMS platforms  
- Deployment presets for partner institutions  

All enhancements will continue to center Airtable as the human-facing workspace.

## Collaboration and Reuse

This repository is open for reuse and adaptation. Cultural heritage organizations often face similar digitization challenges, and we hope this workflow provides a practical starting point.

If you adapt or extend it, we welcome hearing about your implementation.
