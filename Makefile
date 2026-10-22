.PHONY: help setup backend frontend erp dev clean

help:
	@echo "Purchase Requisition System - Build Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup     - Install backend and frontend dependencies"
	@echo "  make backend   - Run the FastAPI backend on port 8000"
	@echo "  make frontend  - Run the Vite frontend on port 5173"
	@echo "  make erp       - Run the mock ERP API on port 8080"
	@echo "  make dev       - Run backend and frontend in parallel (requires tmux)"
	@echo "  make clean     - Remove database and build artifacts"

setup:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✓ Setup complete"

backend:
	@echo "Starting backend on http://localhost:8000"
	cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	@echo "Starting frontend on http://localhost:5173"
	cd frontend && npm run dev

erp:
	@echo "Starting mock ERP API on http://localhost:8080"
	python3 data/mock_po_api.py

dev:
	@echo "Starting backend and frontend in parallel..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "Make sure to run 'make erp' in another terminal for the mock ERP"
	@make -j2 backend frontend

clean:
	@echo "Cleaning up..."
	rm -f backend/requisitions.db
	rm -rf backend/app/__pycache__
	rm -rf frontend/dist
	rm -rf frontend/node_modules
	@echo "✓ Cleaned"
