# Purchase Requisition Automation System

A web application that automates the purchase requisition workflow by extracting data from emails and PDFs, validating against master data, and routing for approval.

## Project Status: Scaffold Phase

This is the initial scaffold of the system. The current implementation includes:

✅ **Backend (FastAPI + SQLAlchemy + SQLite)**
- Database models for master data (suppliers, cost centers, departments, employees, approval bands, GL accounts, FX rates)
- Stub tables for transactional data (requisitions, line items, approval steps, audit log)
- Seed script that loads `data/master_data.json` into SQLite on startup
- Health check endpoint (`GET /health`)
- Read-only API endpoints for suppliers, cost centers, and employees

✅ **Frontend (Vite + React + TypeScript + Tailwind)**
- Basic UI structure
- Suppliers list page that fetches data from the API
- Dev proxy to backend (port 8000)

✅ **Configuration**
- `.env.example` with LLM provider settings and API URLs
- Makefile with commands for running all services

🚧 **Not Yet Implemented**
- Email parsing (`.eml` files and PDF attachments)
- LLM extraction logic
- Validation rules and approval engine
- State machine and workflow
- Full UI for requisition management

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- pip and npm

### Installation

1. **Clone and set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your LLM API key if needed (not required for scaffold)
```

2. **Install dependencies:**
```bash
make setup
```

This will:
- Install Python packages (FastAPI, SQLAlchemy, etc.)
- Install Node packages (React, Vite, Tailwind)
- Create and seed the SQLite database

### Running the Application

**Option 1: Run all services separately (recommended for development)**

Terminal 1 - Backend:
```bash
make backend
# Runs on http://localhost:8000
```

Terminal 2 - Frontend:
```bash
make frontend
# Runs on http://localhost:5173
```

Terminal 3 - Mock ERP (optional, for future PO submission):
```bash
make erp
# Runs on http://localhost:8080
```

**Option 2: Run backend and frontend together**
```bash
make dev
```

### Accessing the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (FastAPI automatic documentation)
- **Health Check**: http://localhost:8000/health

## Project Structure

```
blp-requisitions/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── db.py               # SQLAlchemy database setup
│   │   ├── models.py           # Database models
│   │   ├── schemas.py          # Pydantic API schemas
│   │   ├── seed.py             # Master data seed script
│   │   └── main.py             # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api.ts              # API client functions
│   │   ├── types.ts            # TypeScript type definitions
│   │   ├── App.tsx             # Main React component
│   │   ├── main.tsx            # React entry point
│   │   └── index.css           # Tailwind styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
├── data/
│   ├── emails/                 # Email test files (.eml)
│   ├── quotes/                 # PDF quotes
│   ├── master_data.json        # Source of truth for master data
│   └── mock_po_api.py          # Mock ERP API
├── .env.example
├── Makefile
├── PLAN.md                     # Detailed build plan
└── README.md
```

## Database Schema

### Master Data Tables
- `suppliers` - Supplier information with VAT IDs and normalized names
- `departments` - Company departments with heads
- `cost_centers` - Cost centers with owners and department links
- `employees` - Employee directory with roles and deputies
- `gl_accounts` - General ledger account codes
- `approval_bands` - Approval limits in CHF with required roles
- `fx_rates` - Foreign exchange rates to CHF
- `rules` - System configuration rules

### Transactional Tables (Stubs)
- `inbound_emails` - Parsed incoming emails
- `attachments` - Email attachments with extracted text
- `requisitions` - Purchase requisitions with all fields
- `requisition_lines` - Line items for each requisition
- `issues` - Validation issues flagged on requisitions
- `approval_steps` - Approval chain steps with status
- `duplicate_links` - Suspected duplicates and corrections
- `llm_runs` - LLM extraction attempts with results
- `audit_log` - Complete audit trail
- `purchase_orders` - Submitted POs with ERP responses

## API Endpoints (Current)

- `GET /health` - Health check (database + ERP connectivity)
- `GET /api/master/suppliers` - List all suppliers
- `GET /api/master/cost-centers` - List all cost centers
- `GET /api/master/employees` - List all employees

## Technology Stack

**Backend:**
- FastAPI - Modern async web framework
- SQLAlchemy - SQL toolkit and ORM
- SQLite - Embedded database (production would use PostgreSQL)
- Pydantic - Data validation and settings
- pdfplumber - PDF text extraction (to be implemented)
- httpx - HTTP client for ERP calls

**Frontend:**
- React 18 - UI framework
- TypeScript - Type-safe JavaScript
- Vite - Fast development server and build tool
- Tailwind CSS - Utility-first CSS framework

## Development Notes

### For Beginners Learning Python + React

**What is FastAPI?**
FastAPI is a modern Python web framework that makes it easy to build APIs. When you see `@app.get("/health")`, that's a "decorator" that tells FastAPI "when someone visits /health, run this function." The `async def` means the function can handle multiple requests at once without blocking.

**What is SQLAlchemy?**
SQLAlchemy is like a translator between Python and databases. Instead of writing SQL directly, you define Python classes (like `Supplier` in `models.py`) and SQLAlchemy handles creating tables and running queries. This is called an "ORM" (Object-Relational Mapper).

**What is React?**
React is a JavaScript library for building user interfaces. You write "components" (like `App.tsx`) that describe what the UI should look like, and React handles updating the page when data changes. The `.tsx` extension means we're using TypeScript, which adds type checking to JavaScript.

**How do the backend and frontend connect?**
The frontend (React) runs in your browser and makes HTTP requests to the backend (FastAPI). In development, Vite's proxy (see `vite.config.ts`) forwards `/api` requests from port 5173 to port 8000 so they reach the backend. This avoids CORS (Cross-Origin) issues.

**What is the seed script doing?**
`seed.py` reads `master_data.json` and populates the database tables. It only runs once (when the database is empty) so you don't get duplicates. The normalization functions (`normalize_name`, `normalize_vat`) prepare the data for fuzzy matching later.

## Troubleshooting

**Backend won't start:**
- Make sure you're in the project root directory
- Check that Python 3.11+ is installed: `python3 --version`
- Verify dependencies are installed: `pip list | grep fastapi`

**Frontend won't start:**
- Check Node.js version: `node --version` (need 18+)
- Delete `node_modules` and reinstall: `cd frontend && rm -rf node_modules && npm install`

**"Connection refused" errors:**
- Make sure the backend is running on port 8000
- Check no other process is using the ports: `lsof -i :8000` or `lsof -i :5173`

**Database errors:**
- Delete the database and restart: `make clean && make backend`

## Next Steps

The next phases of implementation will add:

1. **Email parsing** - Parse `.eml` files and extract PDF text
2. **LLM extraction** - Use GPT/Claude to extract structured data
3. **Validation engine** - Match suppliers, check totals, flag issues
4. **Approval routing** - Build approval chains based on bands
5. **Full UI** - Requisition detail view, approval queue, workflow
6. **State machine** - Track requisition status through the workflow
7. **PO submission** - Send approved requisitions to the ERP

See `PLAN.md` for the complete implementation roadmap.

## License

This is a take-home challenge project for BLP Digital.
