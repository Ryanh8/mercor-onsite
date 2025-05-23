"""Task model schema for the application."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Task:
    """
    Task model representing a task within a project.
        
    This means:
    - Each project should have one default task
    - All time tracking is done against this default task
    - The task becomes a pass-through entity rather than a meaningful work unit
    - This simplifies time tracking by removing the need to manage multiple tasks per project
    
    Attributes:
        id: Unique identifier for the task
        name: Name of the task
        status: Current status of the task (should match project statuses)
        priority: Priority level of the task (should match project priorities)
        billable: Whether time logged to this task is billable
        project_id: ID of the project this task belongs to
        employees: List of employee IDs assigned to the task
        description: Detailed description of the task
        creator_id: ID of the user who created the task
        organization_id: ID of the organization
        teams: List of team IDs assigned to the task
        created_at: Timestamp when the task was created (Unix timestamp in milliseconds)
    """
    
    id: str
    name: str
    project_id: str
    creator_id: str
    organization_id: str
    status: str = "To Do"
    priority: str = "low"
    billable: bool = True
    employees: List[str] = field(default_factory=list)
    description: str = ""
    teams: List[str] = field(default_factory=list)
    created_at: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        if not self.name.strip():
            raise ValueError("Task name cannot be empty")
        
        if not self.id:
            raise ValueError("Task ID is required")
        
        if not self.project_id:
            raise ValueError("Project ID is required")

    @property
    def created_datetime(self) -> Optional[datetime]:
        """Convert created_at timestamp to datetime object."""
        if self.created_at:
            return datetime.fromtimestamp(self.created_at / 1000)
        return None

    @property
    def employee_count(self) -> int:
        """Get the number of employees assigned to the task."""
        return len(self.employees)

    @property
    def team_count(self) -> int:
        """Get the number of teams assigned to the task."""
        return len(self.teams)

    @property
    def is_billable(self) -> bool:
        """Check if the task is billable."""
        return self.billable

    # Employee management methods
    def add_employee(self, employee_id: str) -> None:
        """Add an employee to the task."""
        if employee_id not in self.employees:
            self.employees.append(employee_id)

    def remove_employee(self, employee_id: str) -> None:
        """Remove an employee from the task."""
        if employee_id in self.employees:
            self.employees.remove(employee_id)

    def has_employee(self, employee_id: str) -> bool:
        """Check if an employee is assigned to the task."""
        return employee_id in self.employees

    # Team management methods
    def add_team(self, team_id: str) -> None:
        """Add a team to the task."""
        if team_id not in self.teams:
            self.teams.append(team_id)

    def remove_team(self, team_id: str) -> None:
        """Remove a team from the task."""
        if team_id in self.teams:
            self.teams.remove(team_id)

    def has_team(self, team_id: str) -> bool:
        """Check if a team is assigned to the task."""
        return team_id in self.teams

    # Task management methods
    def update_status(self, status: str) -> None:
        """Update the task status."""
        self.status = status

    def update_priority(self, priority: str) -> None:
        """Update the task priority."""
        self.priority = priority

    def set_billable(self, billable: bool) -> None:
        """Set the billable status of the task."""
        self.billable = billable

    def update_description(self, description: str) -> None:
        """Update the task description."""
        self.description = description

    # API-compatible methods for Insightful integration
    def get_task_details(self) -> Dict[str, Any]:
        """Get detailed task information for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "priority": self.priority,
            "billable": self.billable,
            "projectId": self.project_id,
            "employees": self.employees.copy(),
            "description": self.description,
            "creatorId": self.creator_id,
            "organizationId": self.organization_id,
            "teams": self.teams.copy(),
            "createdAt": self.created_at,
            "employeeCount": self.employee_count,
            "teamCount": self.team_count,
            "isBillable": self.is_billable
        }

    def update_from_api(self, data: Dict[str, Any]) -> None:
        """Update task from API response data."""
        if "name" in data:
            self.name = data["name"]
        if "status" in data:
            self.status = data["status"]
        if "priority" in data:
            self.priority = data["priority"]
        if "billable" in data:
            self.billable = data["billable"]
        if "description" in data:
            self.description = data["description"]
        if "employees" in data:
            self.employees = data["employees"]
        if "teams" in data:
            self.teams = data["teams"]

    @classmethod
    def create_default_task_for_project(cls, project_id: str, project_name: str, 
                                      creator_id: str, organization_id: str,
                                      task_id: Optional[str] = None) -> "Task":
        """
        Create a default task for a project (recommended 1:1 mapping).
        
        This follows Insightful's recommendation to have one default task per project
        to simplify time tracking and effectively nullify the task's separate purpose.
        
        Args:
            project_id: ID of the project
            project_name: Name of the project (used for task name)
            creator_id: ID of the user creating the task
            organization_id: ID of the organization
            task_id: Optional specific task ID, if not provided will use project_id
            
        Returns:
            Task instance configured as a default task for the project
        """
        import time
        
        return cls(
            id=task_id or f"default_{project_id}",
            name=f"Default Task - {project_name}",
            project_id=project_id,
            creator_id=creator_id,
            organization_id=organization_id,
            status="In progress",  # Default to active status
            priority="medium",
            billable=True,
            description=f"Default task for project {project_name}. All time tracking for this project should be logged here.",
            created_at=int(time.time() * 1000)
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """
        Create a Task instance from a dictionary.
        
        Args:
            data: Dictionary containing task data
            
        Returns:
            Task instance
        """
        # Map camelCase keys to snake_case
        mapped_data = {
            "id": data.get("id"),
            "name": data.get("name"),
            "status": data.get("status", "To Do"),
            "priority": data.get("priority", "low"),
            "billable": data.get("billable", True),
            "project_id": data.get("projectId"),
            "employees": data.get("employees", []),
            "description": data.get("description", ""),
            "creator_id": data.get("creatorId"),
            "organization_id": data.get("organizationId"),
            "teams": data.get("teams", []),
            "created_at": data.get("createdAt"),
        }
        
        # Remove None values for required fields
        if mapped_data["id"] is None or mapped_data["name"] is None:
            raise ValueError("Task ID and name are required")
        
        return cls(**{k: v for k, v in mapped_data.items() if v is not None})

    def to_dict(self) -> dict:
        """
        Convert Task instance to dictionary with camelCase keys.
        
        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "priority": self.priority,
            "billable": self.billable,
            "projectId": self.project_id,
            "employees": self.employees,
            "description": self.description,
            "creatorId": self.creator_id,
            "organizationId": self.organization_id,
            "teams": self.teams,
            "createdAt": self.created_at,
        }

    def __str__(self) -> str:
        """String representation of the task."""
        return f"Task(id={self.id}, name='{self.name}', status='{self.status}', project={self.project_id})"

    def __repr__(self) -> str:
        """Detailed string representation of the task."""
        return (f"Task(id='{self.id}', name='{self.name}', "
                f"status='{self.status}', priority='{self.priority}', "
                f"billable={self.billable}, project='{self.project_id}')")
