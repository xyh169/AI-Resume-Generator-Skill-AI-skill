# Candidate Knowledge Base And Local RAG Framework

Use this reference when Stage 2 needs a reusable candidate fact database, local knowledge base, RAG retrieval, evidence mapping, or gap detection.

## Goal

Turn long, repeated, or messy candidate materials into small, traceable facts that can be retrieved for a specific JD without fabricating experience.

## Required Materials

Ask for or extract these materials when available:

| Material | Purpose |
|---|---|
| Existing resume versions | Baseline education, work history, projects, awards, skills |
| Raw chat notes or interview transcript | Hidden details, responsibilities, metrics, decision context |
| Project docs or portfolio links | Evidence for scope, tools, outputs, users, architecture |
| Achievement records | Awards, certificates, publications, patents, competition results |
| Metrics evidence | Revenue, DAU/MAU, conversion, latency, accuracy, cost, defect rate, NPS |
| Target JD or target role/domain | Retrieval query and relevance scoring |
| Constraints | Language, seniority, location, page mode, facts that must not be used |

If sensitive personal data is involved, keep the local database in the user's working/output directory and do not store it inside the skill folder.

## Local Directory Contract

Default path when the user has not specified a database path:

```text
{OUTPUT_DIR}/candidate_knowledge/
  candidate_facts.jsonl
  job_targets/
    product-manager-healthcare.example.json
    ai-agent-engineer-finance.example.json
  source_materials/
  retrieval_cache/
  indexes/
```

Only `candidate_facts.jsonl` is required. Other folders are optional.

## Candidate Fact Schema

Store one fact per JSONL line. Prefer small facts over long merged narratives.

```json
{
  "id": "fact_0001",
  "fact_type": "project",
  "title": "Clinical workflow analytics platform",
  "organization": "Example Hospital",
  "role": "Product Manager",
  "start_date": "2024-03",
  "end_date": "2024-12",
  "summary": "Led requirements and dashboard iteration for outpatient workflow analytics.",
  "actions": [
    "Interviewed clinicians and operations stakeholders",
    "Defined KPI dashboard and backlog priority",
    "Coordinated design, engineering, and data teams"
  ],
  "outcomes": [
    "Reduced manual report preparation effort",
    "Improved visibility into appointment bottlenecks"
  ],
  "metrics": [
    {"name": "manual_report_time", "value": "not_provided", "evidence": "user note"}
  ],
  "skills": ["roadmap", "user research", "PRD", "data dashboard"],
  "technologies": ["SQL", "BI dashboard", "FHIR"],
  "role_targets": ["product-manager"],
  "domain_tags": ["healthcare", "workflow", "analytics"],
  "seniority": "entry_to_mid",
  "source_ref": {
    "source_file": "raw_content.md",
    "source_quote": "User described leading clinic dashboard requirements.",
    "source_line": null
  },
  "evidence_strength": "medium",
  "sensitivity": "internal",
  "verification_status": "needs_metric_confirmation",
  "resume_sections": ["项目经历", "专业技能"],
  "avoid_claims": ["Do not claim HIPAA ownership unless user provided it."],
  "follow_up_questions": [
    "Can we quantify the report time reduction or user adoption?"
  ],
  "embedding_text": "Product Manager healthcare workflow analytics FHIR dashboard PRD clinician interviews backlog KPI appointment bottlenecks"
}
```

## Field Rules

| Field | Rule |
|---|---|
| `id` | Stable unique ID; do not recycle when facts are deleted |
| `fact_type` | Use `work`, `project`, `achievement`, `skill`, `education`, `certification`, `publication`, `metric`, `domain_knowledge`, or `case_story` |
| `summary` | One concise factual sentence |
| `actions` | Candidate actions only, not team actions unless candidate's role is clear |
| `outcomes` | Use provided results; qualitative outcomes are allowed if clearly supported |
| `metrics` | Use exact metrics only when sourced; otherwise mark `not_provided` |
| `role_targets` | Example: `product-manager`, `ai-agent-engineer`, `data-analyst` |
| `domain_tags` | Example: `healthcare`, `finance`, `risk`, `payments`, `clinical`, `agentic-rag` |
| `source_ref` | Required; every resume claim must trace back to a source |
| `evidence_strength` | Use `high`, `medium`, or `low` |
| `verification_status` | Use `verified`, `needs_confirmation`, `needs_metric_confirmation`, or `do_not_use` |
| `embedding_text` | Dense retrieval text combining role, domain, skills, action, and outcome |

## Build Workflow

1. Read `raw_content.md` and any user-approved source files.
2. Split content into atomic facts: one project, achievement, skill, metric, or case story per record.
3. Normalize dates, organization names, role titles, skills, technologies, metrics, and source references.
4. Tag each fact with role targets and domain tags.
5. Assign evidence strength.
6. Generate `embedding_text` from factual content only.
7. Write or update `candidate_facts.jsonl`.
8. Run a duplicate pass: merge exact duplicates, keep conflicting facts separate and mark them `needs_confirmation`.

## Retrieval Workflow

Parse the JD or target direction into:

```json
{
  "target_role": "product-manager",
  "domain": "healthcare",
  "must_have": ["roadmap", "user research", "data product"],
  "nice_to_have": ["FHIR", "clinical workflow", "AI feature launch"],
  "responsibilities": ["define PRD", "prioritize backlog", "measure adoption"],
  "risk_or_compliance": ["privacy", "regulated workflow"],
  "keywords": ["provider workflow", "EHR", "KPI", "cross-functional"]
}
```

Score candidate facts with a simple hybrid policy:

```text
score =
  0.35 * semantic_match
  + 0.25 * keyword_overlap
  + 0.20 * role_domain_match
  + 0.10 * evidence_strength
  + 0.10 * recency
  - unsupported_claim_penalty
```

If no vector database exists, use keyword/tag filtering first:

1. Filter by `role_targets` and `domain_tags`.
2. Keep facts with `evidence_strength` in `high` or `medium`.
3. Rank by overlap with JD skills, responsibilities, technologies, and metrics.
4. Deduplicate facts that would produce the same resume bullet.
5. Return the top 6-12 facts for a one-page resume, or 12-20 facts for a multi-page resume.

## Stage 2 Use Rules

- Strong-match facts can become primary bullets.
- Medium-match facts can support skills or secondary bullets.
- Low-evidence facts should trigger follow-up questions or be omitted.
- Missing JD requirements should never be filled by industry assumptions.
- Keep retrieval and scoring artifacts out of `refined_resume.md`.

## Minimal Output Before Writing Resume

Internally produce this handoff:

```json
{
  "strong_matches": ["fact_0001", "fact_0004"],
  "supporting_matches": ["fact_0007"],
  "gaps": [
    {"requirement": "HIPAA compliance", "status": "not_evidenced", "question": "Have you worked with HIPAA or PHI controls?"}
  ],
  "do_not_use": ["fact_0012"]
}
```

Use it internally only. Do not write it into `refined_resume.md`.

## Source Notes

The framework is compatible with local JSONL keyword retrieval, SQLite full-text search, or a vector store. If using a hosted vector database, keep source metadata and filtering attributes with every record so retrieval can be audited.
