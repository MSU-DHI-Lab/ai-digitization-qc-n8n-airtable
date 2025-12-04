# AI-Powered Digitization Quality Control Workflow  
A practical, lab-developed system that integrates AI, Airtable, and n8n to support large-scale collections digitization.

## What You Need Before You Begin

This workflow is designed to be usable by non-technical collections staff once a small amount of initial setup is completed by someone comfortable with basic IT tasks. Before starting, you will need:

1. A designated folder on a workstation, server, shared drive, or mounted cloud drive where staff will place new scans.  
2. An Airtable account (free or paid) and permission to create a base.  
3. A machine capable of running n8n and the lightweight AI model.  
4. An Airtable Personal Access Token.  
5. Basic IT support to install and run n8n and the AI service if staff are not comfortable doing so.  

After setup is complete, day-to-day staff work exclusively in Airtable.

## Plain Language Summary

This workflow helps museum and archive staff review digitized images more efficiently. When a new scan is placed into a designated incoming folder, the system automatically checks the image for common issues such as blur, skew, cutoff edges, or a hand in the frame. Results are sent directly into Airtable as a simple record showing the image, any detected issues, and suggested next steps. Airtable Interfaces guide staff through triage and review so they can approve good scans or flag scans that need to be redone. The workflow is designed so non-technical users can manage digitization work in a clear, intuitive environment.

## Overview

This project documents a real digitization quality control workflow developed in our research lab at Michigan State University. The system supports staff working through a large backlog of scans across multiple collections, many of which require consistent quality checks before entering long-term metadata and preservation pipelines.

We moved this workflow to GitHub to support transparency, reuse, and adaptation by museums, archives, libraries, and cultural heritage organizations facing similar challenges. The implementation reflects multiple rounds of iteration, user feedback, and refinement based on actual digitization output.

Airtable serves as the human-facing environment for metadata, review tasks, and quality assessment. AI provides automated first-pass evaluation. n8n coordinates file monitoring, AI requests, and Airtable updates. The result is a practical, human-centered workflow that reduces repetitive manual work while preserving curatorial judgment.

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

ai-service  
Minimal Python-based computer vision service

n8n-workflow.json  
Complete n8n workflow definition

base-schema.md  
Airtable base schema and field descriptions

interface-design.md  
Airtable Interface layouts and user guidance

ai-experiments-notes.md  
Notes from model testing and ONNX experiments

docker-compose.yml  
Optional container configuration for local deployment

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

## Quick Start for Developers

1. Clone the repository.  
2. Configure environment variables including Airtable credentials and the AI URL.  
3. Run the AI service using docker compose.  
4. Import n8n-workflow.json into your n8n instance and configure credentials.

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
