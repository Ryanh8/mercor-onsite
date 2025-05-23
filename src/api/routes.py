"""
API routes for the time tracking application
"""

from fastapi import APIRouter, HTTPException

from .models import ClockInRequest, ClockOutRequest
from ..services.data_manager import MockDataManager
from ..services.time_tracking_service import TimeTrackingService
from ..services.system_monitor import SystemMonitorService

# Initialize services
data_manager = MockDataManager()
time_service = TimeTrackingService(data_manager)

# Create router
router = APIRouter(prefix="/api")


@router.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    """Get employee by ID"""
    employee = data_manager.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.to_dict()


@router.get("/employees/{employee_id}/projects")
async def get_employee_projects(employee_id: str):
    """Get projects for an employee"""
    projects = data_manager.get_employee_projects(employee_id)
    return [project.to_dict() for project in projects]


@router.get("/employees/{employee_id}/active-session")
async def get_active_session(employee_id: str):
    """Get active time tracking session for employee"""
    session = time_service.get_active_session(employee_id)
    if session:
        return session.to_dict()
    return None


@router.post("/clock-in")
async def clock_in(request: ClockInRequest):
    """Clock in endpoint"""
    return time_service.clock_in(
        request.employee_id, 
        request.project_id, 
        request.task_id, 
        request.timestamp
    ).to_dict()


@router.post("/clock-out")
async def clock_out(request: ClockOutRequest):
    """Clock out endpoint"""
    return time_service.clock_out(request.employee_id, request.timestamp).to_dict()


@router.get("/system-info")
async def get_system_info():
    """Get current system information"""
    return SystemMonitorService.get_system_info()


@router.get("/time-tracking")
async def get_time_tracking():
    """Get all time tracking entries"""
    entries = data_manager.load_time_tracking()
    # Sort by start time, most recent first
    entries.sort(key=lambda x: x.start, reverse=True)
    return [entry.to_dict() for entry in entries]


@router.get("/employees")
async def list_employees():
    """List all active employees"""
    employees = data_manager.load_employees()
    active_employees = [emp for emp in employees if emp.is_active]
    return [emp.to_dict() for emp in active_employees]


@router.get("/projects")
async def list_projects():
    """List all active projects"""
    projects = data_manager.load_projects()
    active_projects = [proj for proj in projects if proj.is_active]
    return [proj.to_dict() for proj in active_projects] 