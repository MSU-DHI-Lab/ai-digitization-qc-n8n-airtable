# Airtable Base Schema – Digitization QC Log

This document describes the Airtable base that supports the AI + n8n + Airtable workflow.

## Base name

Digitization QC Log

## Table: Digitized Objects

Use a single table named “Digitized Objects” with the following fields:

| Field name            | Type              | Notes                                                      |
|-----------------------|-------------------|------------------------------------------------------------|
| Object ID             | Single line text  | Identifier, or fallback to file name without extension     |
| File name             | Single line text  | Original file name                                         |
| File path or URL      | URL or Single text| Location of the file in storage                            |
| Scan date             | Date (with time)  | When the scan was processed                                |
| Operator              | Single select     | Name of staff member / digitization operator               |
| Status                | Single select     | New Scan, QC Pending, QC Passed, QC Failed – Needs Review, Metadata Complete, Digitization Complete |
| Quality               | Single select     | High, Low                                                  |
| Quality score         | Number            | 0–100 score from the model                                 |
| Defects (text summary)| Long text         | Human-readable reasons from the model                      |
| Finger in frame       | Checkbox          | True if detected                                           |
| Skew (degrees)        | Number            | Approximate skew                                           |
| Blur level            | Single select     | None, Mild, Strong                                         |
| Glare present         | Checkbox          | True if detected                                           |
| Cutoff edges          | Checkbox          | True if any margin is cut off                              |
| Notes                 | Long text         | Human notes / comments                                     |

### Recommended views

1. All records  
   - Default grid view, no filters.

2. Needs Review  
   - Filter: Status = “QC Failed – Needs Review”.

3. QC Passed  
   - Filter: Status = “QC Passed” OR Status = “Digitization Complete”.

You can add additional tables later (for example, Collections, Operators, Devices) and link them to “Digitized Objects” as needed.
