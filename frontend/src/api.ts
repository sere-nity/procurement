import { Supplier, CostCenter, Employee } from './types';

const API_BASE = '/api';

export async function fetchSuppliers(): Promise<Supplier[]> {
  const response = await fetch(`${API_BASE}/master/suppliers`);
  if (!response.ok) {
    throw new Error('Failed to fetch suppliers');
  }
  return response.json();
}

export async function fetchCostCenters(): Promise<CostCenter[]> {
  const response = await fetch(`${API_BASE}/master/cost-centers`);
  if (!response.ok) {
    throw new Error('Failed to fetch cost centers');
  }
  return response.json();
}

export async function fetchEmployees(): Promise<Employee[]> {
  const response = await fetch(`${API_BASE}/master/employees`);
  if (!response.ok) {
    throw new Error('Failed to fetch employees');
  }
  return response.json();
}
