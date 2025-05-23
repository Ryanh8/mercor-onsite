"""
Data management service for handling mock JSON data
"""

import json
from typing import List, Optional
from pathlib import Path

from ..models.employee import Employee
from ..models.project import Project
from ..models.task import Task
from ..models.time_tracking import TimeTracking
from ..models.screenshots import Screenshot


class MockDataManager:
    """Manages loading and saving mock data from JSON files"""
    
    def __init__(self, data_dir: str = "mock-db"):
        self.data_dir = Path(data_dir)
        self.employees_file = self.data_dir / "employee.json"
        self.projects_file = self.data_dir / "project.json"
        self.tasks_file = self.data_dir / "task.json"
        self.time_tracking_file = self.data_dir / "time_tracking.json"
        self.screenshots_file = self.data_dir / "screenshots.json"
    
    def load_employees(self) -> List[Employee]:
        """Load employees from JSON file"""
        try:
            with open(self.employees_file, 'r') as f:
                data = json.load(f)
            return [Employee.from_dict(emp_data) for emp_data in data]
        except FileNotFoundError:
            return []
    
    def load_projects(self) -> List[Project]:
        """Load projects from JSON file"""
        try:
            with open(self.projects_file, 'r') as f:
                data = json.load(f)
            return [Project.from_dict(proj_data) for proj_data in data]
        except FileNotFoundError:
            return []
    
    def load_tasks(self) -> List[Task]:
        """Load tasks from JSON file"""
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
            return [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            return []
    
    def load_time_tracking(self) -> List[TimeTracking]:
        """Load time tracking entries from JSON file"""
        try:
            with open(self.time_tracking_file, 'r') as f:
                data = json.load(f)
            return [TimeTracking.from_dict(entry_data) for entry_data in data]
        except FileNotFoundError:
            return []
    
    def save_time_tracking(self, time_entries: List[TimeTracking]) -> None:
        """Save time tracking entries to JSON file"""
        data = [entry.to_dict() for entry in time_entries]
        with open(self.time_tracking_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_screenshots(self) -> List[Screenshot]:
        """Load screenshots from JSON file"""
        try:
            with open(self.screenshots_file, 'r') as f:
                data = json.load(f)
            return [Screenshot.from_dict(screenshot_data) for screenshot_data in data]
        except FileNotFoundError:
            return []
    
    def save_screenshots(self, screenshots: List[Screenshot]) -> None:
        """Save screenshots to JSON file"""
        data = [screenshot.to_dict() for screenshot in screenshots]
        with open(self.screenshots_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        """Get employee by ID"""
        employees = self.load_employees()
        for emp in employees:
            if emp.id == employee_id:
                return emp
        return None
    
    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get project by ID"""
        projects = self.load_projects()
        for proj in projects:
            if proj.id == project_id:
                return proj
        return None
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_employee_projects(self, employee_id: str) -> List[Project]:
        """Get all projects for an employee"""
        projects = self.load_projects()
        return [proj for proj in projects if employee_id in proj.employees]
    
    def get_project_default_task(self, project_id: str) -> Optional[Task]:
        """Get the default task for a project"""
        tasks = self.load_tasks()
        for task in tasks:
            if task.project_id == project_id and "Default Task" in task.name:
                return task
        return None 