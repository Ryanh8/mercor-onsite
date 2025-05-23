"""
API routes for the time tracking application
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

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


# Insightful API compatible endpoints
@router.get("/v1/analytics/window")
async def get_analytics_window(
    start: int = Query(..., description="Start timestamp in milliseconds"),
    end: int = Query(..., description="End timestamp in milliseconds"),
    timezone: Optional[str] = Query(None, description="Timezone string"),
    employeeId: Optional[str] = Query(None, description="Employee ID"),
    teamId: Optional[str] = Query(None, description="Team ID"),
    projectId: Optional[str] = Query(None, description="Project ID"),
    taskId: Optional[str] = Query(None, description="Task ID"),
    shiftId: Optional[str] = Query(None, description="Shift ID")
):
    """
    Get window analytics - returns full detailed time tracking entries
    Compatible with Insightful API: /api/v1/analytics/window
    """
    entries = data_manager.load_time_tracking()
    
    # Filter entries based on time range and optional filters
    filtered_entries = []
    for entry in entries:
        # Time range filter
        entry_start = entry.start
        entry_end = entry.end if entry.end != 0 else entry.start  # For active sessions, use start time
        
        # Check if entry overlaps with requested time range
        if entry_start <= end and entry_end >= start:
            # Apply optional filters
            if employeeId and entry.employeeId != employeeId:
                continue
            if teamId and entry.teamId != teamId:
                continue
            if projectId and entry.projectId != projectId:
                continue
            if taskId and entry.taskId != taskId:
                continue
            if shiftId and entry.shiftId != shiftId:
                continue
            if timezone and entry.timezone != timezone:
                continue
                
            filtered_entries.append(entry)
    
    # Sort by start time, most recent first
    filtered_entries.sort(key=lambda x: x.start, reverse=True)
    
    # Return full detailed format
    return [entry.to_dict() for entry in filtered_entries]


@router.get("/v1/analytics/project-time")
async def get_analytics_project_time(
    start: int = Query(..., description="Start timestamp in milliseconds"),
    end: int = Query(..., description="End timestamp in milliseconds"),
    timezone: Optional[str] = Query(None, description="Timezone string"),
    employeeId: Optional[str] = Query(None, description="Employee ID"),
    teamId: Optional[str] = Query(None, description="Team ID"),
    projectId: Optional[str] = Query(None, description="Project ID"),
    taskId: Optional[str] = Query(None, description="Task ID"),
    shiftId: Optional[str] = Query(None, description="Shift ID")
):
    """
    Get project time analytics - returns simple project summaries
    Compatible with Insightful API: /api/v1/analytics/project-time
    """
    entries = data_manager.load_time_tracking()
    
    # Filter entries based on time range and optional filters
    filtered_entries = []
    for entry in entries:
        # Time range filter
        entry_start = entry.start
        entry_end = entry.end if entry.end != 0 else entry.start
        
        # Check if entry overlaps with requested time range
        if entry_start <= end and entry_end >= start:
            # Apply optional filters
            if employeeId and entry.employeeId != employeeId:
                continue
            if teamId and entry.teamId != teamId:
                continue
            if projectId and entry.projectId != projectId:
                continue
            if taskId and entry.taskId != taskId:
                continue
            if shiftId and entry.shiftId != shiftId:
                continue
            if timezone and entry.timezone != timezone:
                continue
                
            filtered_entries.append(entry)
    
    # Aggregate by project
    project_summaries = {}
    
    for entry in filtered_entries:
        if not entry.projectId:
            continue
            
        project_id = entry.projectId
        
        # Initialize project summary if not exists
        if project_id not in project_summaries:
            project_summaries[project_id] = {
                "id": project_id,
                "time": 0,  # in milliseconds
                "costs": 0.0,
                "income": 0.0
            }
        
        # Calculate time duration within the requested range
        entry_start = max(entry.start, start)
        if entry.is_active_session:
            # For active sessions, use current time or end of range
            import time
            current_time = int(time.time() * 1000)
            entry_end = min(current_time, end)
        else:
            entry_end = min(entry.end, end)
        
        # Only count time if there's actual overlap
        if entry_end > entry_start:
            duration_ms = entry_end - entry_start
            
            # Add to total time
            project_summaries[project_id]["time"] += duration_ms
            
            # Calculate income (billable hours * bill rate)
            if entry.billable and entry.billRate > 0:
                duration_hours = duration_ms / (1000 * 60 * 60)
                income = duration_hours * entry.billRate
                project_summaries[project_id]["income"] += income
            
            # Calculate costs (hours * pay rate)
            if entry.payRate > 0:
                duration_hours = duration_ms / (1000 * 60 * 60)
                costs = duration_hours * entry.payRate
                project_summaries[project_id]["costs"] += costs
    
    # Return as list of summaries, sorted by project ID
    summaries = list(project_summaries.values())
    summaries.sort(key=lambda x: x["id"])
    return summaries


# Legacy endpoints (for backward compatibility)
@router.get("/time-tracking")
async def get_time_tracking():
    """Get all time tracking entries (full detailed format) - Legacy endpoint"""
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