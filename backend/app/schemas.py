from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class SupplierSchema(BaseModel):
    id: str
    name: str
    vat_id: Optional[str] = None
    country: str
    default_currency: str
    payment_terms_days: int
    preferred: bool
    status: str
    
    class Config:
        from_attributes = True


class CostCenterSchema(BaseModel):
    code: str
    name: str
    owner_employee_id: str
    department_code: str
    
    class Config:
        from_attributes = True


class EmployeeSchema(BaseModel):
    id: str
    name: str
    email: str
    role: Optional[str] = None
    deputy_for: Optional[str] = None
    default_cost_center: Optional[str] = None
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    database: str
    erp: Optional[str] = None
