export interface Supplier {
  id: string;
  name: string;
  vat_id: string | null;
  country: string;
  default_currency: string;
  payment_terms_days: number;
  preferred: boolean;
  status: string;
}

export interface CostCenter {
  code: string;
  name: string;
  owner_employee_id: string;
  department_code: string;
}

export interface Employee {
  id: string;
  name: string;
  email: string;
  role?: string;
  deputy_for?: string;
  default_cost_center?: string;
}
