"""
Contractor Time Tracker - Main Application
Clean, organized structure with separated concerns
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.api.routes import router
from src.ui.dashboard import generate_dashboard_html
from src.services.data_manager import MockDataManager


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Contractor Time Tracker",
        description="Clock in/out application with mock data integration - Compatible with Insightful.io API",
        version="2.0.0"
    )
    
    # Include API routes
    app.include_router(router)
    
    # Dashboard route
    @app.get("/", response_class=HTMLResponse)
    async def dashboard():
        """Main dashboard for contractors"""
        return generate_dashboard_html()
    
    return app


# Create app instance for uvicorn
app = create_app()


def main():
    """Main entry point"""
    print("🚀 Starting Contractor Time Tracker v2.0...")
    print("📊 Integrated with Mock JSON Data")
    print("🔗 Dashboard: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    
    # Load and display available employees
    data_manager = MockDataManager()
    employees = data_manager.load_employees()
    active_employees = [emp for emp in employees if emp.is_active]
    print(f"\n👥 Available Employees ({len(active_employees)} active):")
    for emp in active_employees[:5]:  # Show first 5
        projects = data_manager.get_employee_projects(emp.id)
        print(f"  - {emp.name} ({emp.id}) - {len(projects)} projects")
    
    # Run the app
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
