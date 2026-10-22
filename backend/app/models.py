from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime, Text, JSON, Date, ForeignKey, Enum
from sqlalchemy.sql import func
from .db import Base
import enum


class SupplierStatus(str, enum.Enum):
    active = "active"
    blocked = "blocked"


class RequisitionStatus(str, enum.Enum):
    inbox = "inbox"
    extracted = "extracted"
    needs_review = "needs_review"
    pending_approval = "pending_approval"
    approved = "approved"
    rejected = "rejected"
    ordered = "ordered"
    closed_duplicate = "closed_duplicate"


# Master Data Models
class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    name_norm = Column(String, index=True)
    vat_id = Column(String, nullable=True)
    vat_norm = Column(String, nullable=True, index=True)
    country = Column(String)
    default_currency = Column(String)
    payment_terms_days = Column(Integer)
    preferred = Column(Boolean, default=False)
    status = Column(String, default="active")
    created_by_clerk = Column(Boolean, default=False)


class Department(Base):
    __tablename__ = "departments"
    
    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    head_employee_id = Column(String, ForeignKey("employees.id"))


class CostCenter(Base):
    __tablename__ = "cost_centers"
    
    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    owner_employee_id = Column(String, ForeignKey("employees.id"))
    department_code = Column(String, ForeignKey("departments.code"))


class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String)
    deputy_for = Column(String, ForeignKey("employees.id"), nullable=True)
    default_cost_center = Column(String, nullable=True)


class GLAccount(Base):
    __tablename__ = "gl_accounts"
    
    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class ApprovalBand(Base):
    __tablename__ = "approval_bands"
    
    id = Column(Integer, primary_key=True)
    from_chf = Column(Numeric(14, 4), nullable=False)
    to_chf = Column(Numeric(14, 4), nullable=True)
    required_roles = Column(JSON, nullable=False)


class FXRate(Base):
    __tablename__ = "fx_rates"
    
    currency = Column(String, primary_key=True)
    rate_to_chf = Column(Numeric(10, 4), nullable=False)


class Rule(Base):
    __tablename__ = "rules"
    
    key = Column(String, primary_key=True)
    value = Column(JSON, nullable=False)


# Transactional Models (Stubs for now)
class InboundEmail(Base):
    __tablename__ = "inbound_emails"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    message_id = Column(String)
    in_reply_to = Column(String, nullable=True)
    from_name = Column(String)
    from_email = Column(String)
    to = Column(String)
    subject = Column(String)
    sent_at = Column(DateTime)
    body_text = Column(Text)
    body_format = Column(String)
    raw_sha256 = Column(String, unique=True)
    received_at = Column(DateTime, server_default=func.now())


class Attachment(Base):
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey("inbound_emails.id"))
    filename = Column(String)
    content_type = Column(String)
    sha256 = Column(String)
    size = Column(Integer)
    extracted_text = Column(Text, nullable=True)
    page_count = Column(Integer, nullable=True)
    path = Column(String)


class Requisition(Base):
    __tablename__ = "requisitions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ref = Column(String, unique=True, nullable=False)
    email_id = Column(Integer, ForeignKey("inbound_emails.id"))
    status = Column(String, default="inbox")
    revision = Column(Integer, default=0)
    chain_version = Column(Integer, default=0)
    
    # Requester
    requester_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    requester_email = Column(String)
    requester_source = Column(String)
    
    # Supplier
    supplier_id = Column(String, ForeignKey("suppliers.id"), nullable=True)
    supplier_name_raw = Column(String)
    supplier_vat_raw = Column(String, nullable=True)
    supplier_match = Column(String, nullable=True)
    
    # Cost center
    cost_center_code = Column(String, ForeignKey("cost_centers.code"), nullable=True)
    cost_center_raw = Column(String, nullable=True)
    
    # Amounts
    currency = Column(String, nullable=True)
    net_total_computed = Column(Numeric(14, 4), nullable=True)
    net_total_stated = Column(Numeric(14, 4), nullable=True)
    vat_amount_stated = Column(Numeric(14, 4), nullable=True)
    gross_total_stated = Column(Numeric(14, 4), nullable=True)
    total_chf = Column(Numeric(14, 4), nullable=True)
    fx_rate_used = Column(Numeric(10, 4), nullable=True)
    band_id = Column(Integer, ForeignKey("approval_bands.id"), nullable=True)
    
    # Delivery and other
    requested_delivery_date = Column(Date, nullable=True)
    delivery_date_raw = Column(String, nullable=True)
    delivery_date_source = Column(String, nullable=True)
    gl_account_code = Column(String, ForeignKey("gl_accounts.code"), nullable=True)
    gl_suggested = Column(String, nullable=True)
    gl_confirmed = Column(Boolean, default=False)
    quote_number = Column(String, nullable=True)
    quote_valid_until = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    po_number = Column(String, nullable=True)
    po_warnings = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class RequisitionLine(Base):
    __tablename__ = "requisition_lines"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"))
    position = Column(Integer)
    description = Column(String)
    item_code = Column(String, nullable=True)
    quantity = Column(Numeric(14, 4), nullable=True)
    unit = Column(String, nullable=True)
    unit_price = Column(Numeric(14, 4), nullable=True)
    price_per = Column(Numeric(14, 4), default=1)
    unit_price_raw = Column(String, nullable=True)
    line_total_stated = Column(Numeric(14, 4), nullable=True)
    line_total_computed = Column(Numeric(14, 4), nullable=True)
    is_adjustment = Column(Boolean, default=False)
    source = Column(String)


class Issue(Base):
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"))
    code = Column(String)
    severity = Column(String)
    field = Column(String, nullable=True)
    message = Column(String)
    resolved_by = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolution_note = Column(Text, nullable=True)


class ApprovalStep(Base):
    __tablename__ = "approval_steps"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"))
    chain_version = Column(Integer)
    seq = Column(Integer)
    roles = Column(JSON)
    approver_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    status = Column(String, default="waiting")
    skipped_roles = Column(JSON, nullable=True)
    assigned_by_clerk = Column(Boolean, default=False)
    decided_at = Column(DateTime, nullable=True)
    comment = Column(Text, nullable=True)


class DuplicateLink(Base):
    __tablename__ = "duplicate_links"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"))
    candidate_requisition_id = Column(Integer, ForeignKey("requisitions.id"))
    kind = Column(String)
    score = Column(Numeric(5, 2))
    reasons = Column(JSON)
    resolution = Column(String, default="open")


class LLMRun(Base):
    __tablename__ = "llm_runs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"))
    attempt = Column(Integer)
    prompt_version = Column(String)
    model = Column(String)
    input_chars = Column(Integer)
    latency_ms = Column(Integer)
    valid = Column(Boolean)
    validation_errors = Column(JSON, nullable=True)
    output_json = Column(JSON, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"), nullable=True)
    at = Column(DateTime, server_default=func.now())
    actor = Column(String)
    action = Column(String)
    before = Column(JSON, nullable=True)
    after = Column(JSON, nullable=True)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    requisition_id = Column(Integer, ForeignKey("requisitions.id"))
    idempotency_key = Column(String, unique=True)
    request_json = Column(JSON)
    response_status = Column(Integer)
    response_json = Column(JSON, nullable=True)
    po_number = Column(String, nullable=True)
    sent_at = Column(DateTime, server_default=func.now())
