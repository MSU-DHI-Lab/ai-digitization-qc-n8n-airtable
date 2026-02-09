# Airtable Interface Design Guide: Digitization Command Center

This guide covers practical Airtable interface layouts for the `Digitized Objects` table.

## 1. Triage Interface (Review Queue)

Goal: let a curator review flagged items quickly.

- Layout: Record Review (Split View)
- Filter: `Status` is "QC Failed – Needs Review"
- Core elements:
  - Left sidebar: `File name`, `Quality Score`, and status indicators.
  - Main pane:
    - Large image preview from `File path or URL`.
    - `AI Analysis Report` rich-text summary.
    - Action buttons:
      - Approve -> set status to `QC Passed`
      - Reject -> set status to `Rescan Required`

## 2. Collection Health Dashboard

Goal: show current throughput and quality trends.

- Layout: Dashboard
- Suggested widgets:
  - Total scans processed
  - Quality split (`High` vs `Low`)
  - Defect frequency counts
  - Recent high-quality scans (`Quality Score > 90`)

## 3. Metadata Enrichment View

Goal: review and refine AI-generated tags while items are already open.

- Layout: Grid or Gallery
- Key fields:
  - `File name`
  - `Tags`
- Workflow:
  - Review suggested tags.
  - Add or remove tags directly.
  - Save changes as part of the same review pass.

## Why this matters
Interfaces keep staff focused on review decisions instead of table mechanics. The same data model supports triage, reporting, and metadata cleanup.
