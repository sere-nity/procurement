import json
from pathlib import Path
from sqlalchemy.orm import Session
from .db import engine, SessionLocal, Base
from . import models


def seed_database():
    """Load master_data.json into the database if it's empty."""
    db = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(models.Supplier).count() > 0:
            print("Database already seeded, skipping.")
            return
        
        # Load master data
        data_path = Path(__file__).parent.parent.parent / "data" / "master_data.json"
        with open(data_path) as f:
            master_data = json.load(f)
        
        print("Seeding database from master_data.json...")
        
        # Seed employees first (needed for foreign keys)
        for emp_data in master_data["employees"]:
            employee = models.Employee(
                id=emp_data["id"],
                name=emp_data["name"],
                email=emp_data["email"],
                role=emp_data.get("role"),
                department=emp_data.get("department")
            )
            db.add(employee)
        
        # Seed cost centers
        for cc_data in master_data["cost_centers"]:
            cost_center = models.CostCenter(
                code=cc_data["code"],
                name=cc_data["name"],
                owner_id=cc_data.get("owner_employee_id"),
                department=cc_data.get("department")
            )
            db.add(cost_center)
        
        # Seed suppliers
        for sup_data in master_data["suppliers"]:
            supplier = models.Supplier(
                id=sup_data["id"],
                name=sup_data["name"],
                vat_id=sup_data.get("vat_id"),
                country=sup_data["country"],
                currency=sup_data["default_currency"],
                blocked=(sup_data.get("status") == "blocked")
            )
            db.add(supplier)
        
        # Seed approval limits
        # Extract roles from approval_limits_chf and create ApprovalLimit entries
        # Each role gets the highest max_chf from all bands it appears in
        role_max_chf = {}
        for band_data in master_data["approval_limits_chf"]:
            max_chf = band_data.get("to") or 999999999
            for role in band_data["required_roles"]:
                if role not in role_max_chf or max_chf > role_max_chf[role]:
                    role_max_chf[role] = max_chf
        
        for role, max_chf in role_max_chf.items():
            approval_limit = models.ApprovalLimit(
                role=role,
                max_chf=max_chf
            )
            db.add(approval_limit)
        
        db.commit()
        print(f"✓ Seeded {db.query(models.Supplier).count()} suppliers")
        print(f"✓ Seeded {db.query(models.Employee).count()} employees")
        print(f"✓ Seeded {db.query(models.CostCenter).count()} cost centers")
        print(f"✓ Seeded {db.query(models.ApprovalLimit).count()} approval limits")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


if __name__ == "__main__":
    init_db()
    seed_database()
