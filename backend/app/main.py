from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import httpx

from .db import get_db, engine, Base
from .seed import seed_database, init_db
from . import models, schemas
from .config import settings

# Create tables and seed on startup
init_db()
seed_database()

app = FastAPI(title="Purchase Requisition API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=schemas.HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    # Check database
    try:
        db.query(models.Supplier).first()
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check ERP
    erp_status = "not_checked"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.po_api_url}/health", timeout=2.0)
            erp_status = "ok" if response.status_code == 200 else f"error: {response.status_code}"
    except Exception as e:
        erp_status = f"error: {str(e)}"
    
    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "database": db_status,
        "erp": erp_status
    }


@app.get("/api/master/suppliers", response_model=List[schemas.SupplierSchema])
def get_suppliers(db: Session = Depends(get_db)):
    """Get all suppliers."""
    suppliers = db.query(models.Supplier).all()
    return suppliers


@app.get("/api/master/cost-centers", response_model=List[schemas.CostCenterSchema])
def get_cost_centers(db: Session = Depends(get_db)):
    """Get all cost centers."""
    cost_centers = db.query(models.CostCenter).all()
    return cost_centers


@app.get("/api/master/employees", response_model=List[schemas.EmployeeSchema])
def get_employees(db: Session = Depends(get_db)):
    """Get all employees."""
    employees = db.query(models.Employee).all()
    return employees


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
