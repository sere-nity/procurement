import json
from pathlib import Path
from sqlalchemy.orm import Session
from .db import engine, SessionLocal, Base
from . import models


def normalize_name(name: str) -> str:
    """Normalize supplier name for matching.
    
    Strips legal forms only as whole words at the end, preserves umlauts
    (so Müller and Mueller remain distinct).
    """
    name = name.lower()
    # Remove punctuation
    for char in ".,&-":
        name = name.replace(char, " ")
    # Strip legal forms only as whole words at the end
    legal_forms = ["gmbh", "ag", "kg", "ltd", "inc", "s.r.l.", "srl", "bv", "oü", "as", "co"]
    words = name.split()
    while words and words[-1] in legal_forms:
        words.pop()
    return " ".join(words)


def normalize_vat(vat: str) -> str:
    """Normalize VAT ID for matching."""
    if not vat:
        return None
    vat = vat.upper()
    # Strip spaces, dots, dashes
    for char in " .-":
        vat = vat.replace(char, "")
    # Remove suffixes
    for suffix in ["MWST", "TVA", "IVA"]:
        vat = vat.replace(suffix, "")
    return vat


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
        
        # Seed FX rates
        fx_rates = master_data["_meta"]["fx_rates_to_chf"]
        for currency, rate in fx_rates.items():
            fx_rate = models.FXRate(currency=currency, rate_to_chf=rate)
            db.add(fx_rate)
        
        # Seed employees first (needed for foreign keys)
        for emp_data in master_data["employees"]:
            employee = models.Employee(
                id=emp_data["id"],
                name=emp_data["name"],
                email=emp_data["email"].lower(),
                role=emp_data.get("role"),
                deputy_for=emp_data.get("deputy_for"),
                default_cost_center=emp_data.get("default_cost_center")
            )
            db.add(employee)
        
        # Seed departments
        for dept_data in master_data["departments"]:
            department = models.Department(
                code=dept_data["code"],
                name=dept_data["name"],
                head_employee_id=dept_data["head_employee_id"]
            )
            db.add(department)
        
        # Seed cost centers
        for cc_data in master_data["cost_centers"]:
            cost_center = models.CostCenter(
                code=cc_data["code"],
                name=cc_data["name"],
                owner_employee_id=cc_data["owner_employee_id"],
                department_code=cc_data["department"]
            )
            db.add(cost_center)
        
        # Seed suppliers
        normalized_names = set()
        for sup_data in master_data["suppliers"]:
            vat_id = sup_data.get("vat_id")
            name_norm = normalize_name(sup_data["name"])
            
            # Check uniqueness of normalized names
            if name_norm in normalized_names:
                print(f"⚠ WARNING: Duplicate normalized name '{name_norm}' for supplier {sup_data['id']} ({sup_data['name']})")
            normalized_names.add(name_norm)
            
            supplier = models.Supplier(
                id=sup_data["id"],
                name=sup_data["name"],
                name_norm=name_norm,
                vat_id=vat_id,
                vat_norm=normalize_vat(vat_id) if vat_id else None,
                country=sup_data["country"],
                default_currency=sup_data["default_currency"],
                payment_terms_days=sup_data["payment_terms_days"],
                preferred=sup_data.get("preferred", False),
                status=sup_data.get("status", "active"),
                created_by_clerk=False
            )
            db.add(supplier)
        
        # Verify all normalized names are unique
        if len(normalized_names) != len(master_data["suppliers"]):
            raise ValueError(f"Normalized name collision detected: {len(master_data['suppliers'])} suppliers but only {len(normalized_names)} unique normalized names")
        
        # Seed GL accounts
        for gl_data in master_data["gl_accounts"]:
            gl_account = models.GLAccount(
                code=gl_data["code"],
                name=gl_data["name"]
            )
            db.add(gl_account)
        
        # Seed approval bands
        for idx, band_data in enumerate(master_data["approval_limits_chf"], start=1):
            band = models.ApprovalBand(
                id=idx,
                from_chf=band_data["from"],
                to_chf=band_data.get("to"),
                required_roles=band_data["required_roles"]
            )
            db.add(band)
        
        db.commit()
        print(f"✓ Seeded {db.query(models.Supplier).count()} suppliers")
        print(f"✓ Seeded {db.query(models.Employee).count()} employees")
        print(f"✓ Seeded {db.query(models.CostCenter).count()} cost centers")
        print(f"✓ Seeded {db.query(models.Department).count()} departments")
        print(f"✓ Seeded {db.query(models.GLAccount).count()} GL accounts")
        print(f"✓ Seeded {db.query(models.ApprovalBand).count()} approval bands")
        print(f"✓ Seeded {db.query(models.FXRate).count()} FX rates")
        
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
