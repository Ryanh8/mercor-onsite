"""
Time tracking service for managing employee work sessions
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException

from ..models.time_tracking import TimeTracking
from .data_manager import MockDataManager
from .screenshot_service import ScreenshotService
from .system_monitor import SystemMonitorService


class TimeTrackingService:
    """Service for managing employee time tracking sessions"""
    
    def __init__(self, data_manager: MockDataManager):
        self.data_manager = data_manager
        self.screenshot_service = ScreenshotService()
        self.system_monitor = SystemMonitorService()
    
    def clock_in(self, employee_id: str, project_id: Optional[str] = None, 
                task_id: Optional[str] = None, timestamp: Optional[datetime] = None) -> TimeTracking:
        """Clock in an employee"""
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        
        # Validate employee exists and is active
        employee = self.data_manager.get_employee_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        if not employee.is_active:
            raise HTTPException(status_code=400, detail="Employee is not active")
        
        # Check if already clocked in
        time_entries = self.data_manager.load_time_tracking()
        for entry in time_entries:
            if entry.employeeId == employee_id and entry.is_active_session:
                raise HTTPException(status_code=400, detail="Employee already clocked in")
        
        # If no project specified, use the first project the employee is assigned to
        if not project_id:
            employee_projects = self.data_manager.get_employee_projects(employee_id)
            if not employee_projects:
                raise HTTPException(status_code=400, detail="Employee not assigned to any projects")
            project_id = employee_projects[0].id
        
        # Validate project
        project = self.data_manager.get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if employee_id not in project.employees:
            raise HTTPException(status_code=400, detail="Employee not assigned to this project")
        
        # If no task specified, use the default task for the project
        if not task_id:
            default_task = self.data_manager.get_project_default_task(project_id)
            if default_task:
                task_id = default_task.id
            else:
                raise HTTPException(status_code=400, detail="No default task found for project")
        
        # Validate task
        task = self.data_manager.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Create active time tracking session
        start_timestamp = int(timestamp.timestamp() * 1000)
        time_entry = TimeTracking.create_active_session(
            start=start_timestamp,
            employeeId=employee_id,
            projectId=project_id,
            taskId=task_id,
            teamId=employee.team_id,
            timezone="UTC"
        )
        
        # Save time entry
        time_entries.append(time_entry)
        self.data_manager.save_time_tracking(time_entries)
        
        # Capture initial screenshot
        screenshot = self.screenshot_service.capture_screenshot(employee_id, project_id, task_id)
        if screenshot:
            screenshots = self.data_manager.load_screenshots()
            screenshots.append(screenshot)
            self.data_manager.save_screenshots(screenshots)
        
        return time_entry
    
    def clock_out(self, employee_id: str, timestamp: Optional[datetime] = None) -> TimeTracking:
        """Clock out an employee"""
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        
        # Find active time entry
        time_entries = self.data_manager.load_time_tracking()
        active_entry = None
        for entry in time_entries:
            if entry.employeeId == employee_id and entry.is_active_session:
                active_entry = entry
                break
        
        if not active_entry:
            raise HTTPException(status_code=400, detail="Employee not currently clocked in")
        
        # Clock out using the TimeTracking method
        end_timestamp = int(timestamp.timestamp() * 1000)
        active_entry.clock_out(end_timestamp)
        
        # Save updated time entries
        self.data_manager.save_time_tracking(time_entries)
        
        # Capture final screenshot
        screenshot = self.screenshot_service.capture_screenshot(
            employee_id, active_entry.projectId, active_entry.taskId
        )
        if screenshot:
            screenshots = self.data_manager.load_screenshots()
            screenshots.append(screenshot)
            self.data_manager.save_screenshots(screenshots)
        
        return active_entry
    
    def get_active_session(self, employee_id: str) -> Optional[TimeTracking]:
        """Get active time tracking session for employee"""
        time_entries = self.data_manager.load_time_tracking()
        for entry in time_entries:
            if entry.employeeId == employee_id and entry.is_active_session:
                return entry
        return None 