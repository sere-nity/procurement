from pydantic import BaseModel
from typing import Optional


class SupplierSchema(BaseModel):
    id: str
    name: str
    vat_id: Optional[str] = None
    country: str
    currency: str
    blocked: bool
    
    class Config:
        from_attributes = True


class CostCenterSchema(BaseModel):
    code: str
    name: str
    owner_id: Optional[str] = None
    department: Optional[str] = None
    
    class Config:
        from_attributes = True


class EmployeeSchema(BaseModel):
    id: str
    name: str
    email: str
    role: Optional[str] = None
    department: Optional[str] = None
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    database: str
    erp: Optional[str] = None
