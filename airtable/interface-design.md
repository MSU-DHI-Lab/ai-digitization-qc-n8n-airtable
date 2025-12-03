# Airtable Interface Design Guide: Digitization Command Center

This guide describes how to build a modern, "Interface-First" dashboard for this digitization workflow. This transforms the raw data in the **Digitized Objects** table into a powerful tool for collections staff.

## 1. The "Triage" Interface (Review Queue)

**Goal:** Allow a curator to rapidly review items flagged by AI.

- **Layout:** Record Review (Split View)
- **Filter:** `Status` is "QC Failed – Needs Review"
- **Key Elements:**
  - **Left Sidebar:** List of items, showing `File name` and `Quality Score` (color-coded).
  - **Main Area:**
    - **Hero Image:** Large preview of the scan (`File path or URL` attachment).
    - **AI Analysis Panel:**
      - Display the **AI Analysis Report** (Rich Text field).
      - This gives the curator a clear, formatted summary (e.g., "✅ High Confidence" or "❌ Issues: Blur detected").
    - **Action Buttons:**
      - "Approve" (Updates status to `QC Passed`)
      - "Reject" (Updates status to `Rescan Required`)

## 2. The "Collection Health" Dashboard

**Goal:** High-level metrics for the department head.

- **Layout:** Dashboard
- **Charts:**
  - **Number:** Total Scans Processed (Count of all records).
  - **Pie Chart:** Quality Distribution (`Quality` field: High vs. Low).
  - **Bar Chart:** Common Defects (Count of `Finger in frame`, `Blur`, etc.).
  - **List:** Recent "High Quality" scans (filtered by `Quality Score > 90`).

## 3. Metadata Enrichment View

**Goal:** Review and refine auto-generated tags.

- **Layout:** Grid or Gallery
- **Key Fields:**
  - `File name`
  - `Tags` (Multi-select, auto-populated by AI).
- **Workflow:**
  - Staff member reviews the AI-suggested tags (e.g., "Sepia", "Handwritten").
  - Adds or removes tags directly in the interface.
  - This turns the QC step into a **value-add metadata step**.

---

## Why this matters
By using Interfaces, you hide the complexity of the underlying database. Staff interact with a clean, purpose-built app that feels professional and focused, powered by the structured data from the AI workflow.
