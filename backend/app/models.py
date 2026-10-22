from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime, Text, JSON, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    vat_id = Column(String, nullable=True)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    blocked = Column(Boolean, default=False)


class CostCenter(Base):
    __tablename__ = "cost_centers"
    
    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey("employees.id"), nullable=True)
    department = Column(String, nullable=True)


class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=True)
    department = Column(String, nullable=True)


class ApprovalLimit(Base):
    __tablename__ = "approval_limits"
    
    role = Column(String, primary_key=True)
    max_chf = Column(Numeric(14, 2), nullable=False)


class Requisition(Base):
    __tablename__ = "requisitions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_file = Column(String, nullable=True)
    status = Column(String, default="needs_review")
    requester_id = Column(String, ForeignKey("employees.id"), nullable=True)
    supplier_id = Column(String, ForeignKey("suppliers.id"), nullable=True)
    cost_center_code = Column(String, ForeignKey("cost_centers.code"), nullable=True)
    currency = Column(String, nullable=True)
    total_net = Column(Numeric(14, 2), nullable=True)
    total_chf = Column(Numeric(14, 2), nullable=True)
    delivery_date = Column(Date, nullable=True)
    extracted = Column(JSON, nullable=True)
    issues = Column(JSON, nullable=True)
    duplicate_of = Column(Integer, ForeignKey("requisitions.id"), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    po_number = Column(String, nullable=True)
    
    lines = relationship("LineItem", back_populates="requisition")
    approval_steps = relationship("ApprovalStep", back_populates="requisition")


class LineItem(Base):
    __tablename__ = "line_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"), nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Numeric(14, 4), nullable=True)
    unit_price = Column(Numeric(14, 4), nullable=True)
    unit = Column(String, nullable=True)
    
    requisition = relationship("Requisition", back_populates="lines")


class ApprovalStep(Base):
    __tablename__ = "approval_steps"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"), nullable=False)
    step_no = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    approver_id = Column(String, ForeignKey("employees.id"), nullable=True)
    status = Column(String, default="pending")
    decided_at = Column(DateTime, nullable=True)
    
    requisition = relationship("Requisition", back_populates="approval_steps")
