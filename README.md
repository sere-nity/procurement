# Purchase Requisition Automation System

A web application that automates the purchase requisition workflow by extracting data from emails and PDFs, validating against master data, and routing for approval.

## Status: Scaffold Only

This is the initial scaffold. Implemented: backend API (FastAPI + SQLAlchemy + SQLite), frontend UI (Vite + React + TypeScript + Tailwind), database models, seed script. Not yet implemented: email/PDF parsing, LLM extraction, validation rules, approval engine, state machine, full workflow UI. See `PLAN.md` for the complete build roadmap.

## Quick Start

**Prerequisites:** Python 3.11+, Node.js 18+

**Install dependencies:**
```bash
make setup
```

**Run backend (port 8000):**
```bash
make backend
```

**Run frontend (port 5173):**
```bash
make frontend
```

**Run mock ERP (port 8080, optional):**
```bash
make erp
```

**Access:**
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Project Structure

```
blp-requisitions/
├── backend/
│   ├── app/
│   │   ├── config.py          # Settings (DB, LLM, ERP URLs)
│   │   ├── db.py              # SQLAlchemy setup
│   │   ├── models.py          # Database models (40+ tables)
│   │   ├── schemas.py         # Pydantic API schemas
│   │   ├── seed.py            # Load master_data.json into SQLite
│   │   └── main.py            # FastAPI app + routes
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api.ts             # API client
│   │   ├── types.ts           # TypeScript types
│   │   ├── App.tsx            # Main component (supplier list)
│   │   └── main.tsx
│   ├── vite.config.ts         # Dev server + proxy to :8000
│   └── package.json
├── data/
│   ├── emails/*.eml           # Test emails (48)
│   ├── quotes/*.pdf           # Supplier quotes (21)
│   ├── master_data.json       # Master data source
│   └── mock_po_api.py         # Mock ERP
├── .env.example
├── Makefile
└── PLAN.md                    # Detailed build plan
```
