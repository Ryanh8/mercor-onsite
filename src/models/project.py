"""Project model schema for the application."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


@dataclass
class Payroll:
    """
    Payroll configuration for a project.
    
    Attributes:
        bill_rate: Billing rate for regular hours
        overtime_bill_rate: Billing rate for overtime hours
    """
    
    bill_rate: float = 1.0
    overtime_bill_rate: float = 1.0

    @classmethod
    def from_dict(cls, data: dict) -> "Payroll":
        """Create Payroll instance from dictionary."""
        return cls(
            bill_rate=data.get("billRate", 1.0),
            overtime_bill_rate=data.get("overtimeBillRate", 1.0)
        )

    def to_dict(self) -> dict:
        """Convert Payroll instance to dictionary with camelCase keys."""
        return {
            "billRate": self.bill_rate,
            "overtimeBillRate": self.overtime_bill_rate
        }


@dataclass
class Project:
    """
    Project model representing a project in the organization.
    
    Attributes:
        id: Unique identifier for the project
        name: Name of the project
        archived: Whether the project is archived
        statuses: List of available task statuses
        priorities: List of available task priorities
        billable: Whether the project is billable
        payroll: Payroll configuration for the project
        employees: List of employee IDs assigned to the project
        creator_id: ID of the user who created the project
        organization_id: ID of the organization
        teams: List of team IDs assigned to the project
        created_at: Timestamp when the project was created (Unix timestamp in milliseconds)
    """
    
    id: str
    name: str
    creator_id: str
    organization_id: str
    archived: bool = False
    statuses: List[str] = field(default_factory=lambda: ["To do", "On hold", "In progress", "Done"])
    priorities: List[str] = field(default_factory=lambda: ["low", "medium", "high"])
    billable: bool = True
    payroll: Payroll = field(default_factory=Payroll)
    employees: List[str] = field(default_factory=list)
    teams: List[str] = field(default_factory=list)
    created_at: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate project data after initialization."""
        if not self.name.strip():
            raise ValueError("Project name cannot be empty")
        
        if not self.id:
            raise ValueError("Project ID is required")
        
        # Ensure payroll is a Payroll instance
        if isinstance(self.payroll, dict):
            self.payroll = Payroll.from_dict(self.payroll)

    @property
    def is_archived(self) -> bool:
        """Check if the project is archived."""
        return self.archived

    @property
    def is_active(self) -> bool:
        """Check if the project is active (not archived)."""
        return not self.archived

    @property
    def created_datetime(self) -> Optional[datetime]:
        """Convert created_at timestamp to datetime object."""
        if self.created_at:
            return datetime.fromtimestamp(self.created_at / 1000)
        return None

    @property
    def employee_count(self) -> int:
        """Get the number of employees assigned to the project."""
        return len(self.employees)

    @property
    def team_count(self) -> int:
        """Get the number of teams assigned to the project."""
        return len(self.teams)

    # Employee management methods
    def add_employee(self, employee_id: str) -> None:
        """Add an employee to the project."""
        if employee_id not in self.employees:
            self.employees.append(employee_id)

    def remove_employee(self, employee_id: str) -> None:
        """Remove an employee from the project."""
        if employee_id in self.employees:
            self.employees.remove(employee_id)

    def has_employee(self, employee_id: str) -> bool:
        """Check if an employee is assigned to the project."""
        return employee_id in self.employees

    # Team management methods
    def add_team(self, team_id: str) -> None:
        """Add a team to the project."""
        if team_id not in self.teams:
            self.teams.append(team_id)

    def remove_team(self, team_id: str) -> None:
        """Remove a team from the project."""
        if team_id in self.teams:
            self.teams.remove(team_id)

    def has_team(self, team_id: str) -> bool:
        """Check if a team is assigned to the project."""
        return team_id in self.teams

    # Status and priority management
    def add_status(self, status: str) -> None:
        """Add a new status to the project."""
        if status not in self.statuses:
            self.statuses.append(status)

    def remove_status(self, status: str) -> None:
        """Remove a status from the project."""
        if status in self.statuses:
            self.statuses.remove(status)

    def add_priority(self, priority: str) -> None:
        """Add a new priority to the project."""
        if priority not in self.priorities:
            self.priorities.append(priority)

    def remove_priority(self, priority: str) -> None:
        """Remove a priority from the project."""
        if priority in self.priorities:
            self.priorities.remove(priority)

    # Archive management
    def archive(self) -> None:
        """Archive the project."""
        self.archived = True

    def unarchive(self) -> None:
        """Unarchive the project."""
        self.archived = False

    # Billing management
    def set_billable(self, billable: bool) -> None:
        """Set the billable status of the project."""
        self.billable = billable

    def update_payroll(self, bill_rate: Optional[float] = None, 
                      overtime_bill_rate: Optional[float] = None) -> None:
        """Update payroll rates for the project."""
        if bill_rate is not None:
            self.payroll.bill_rate = bill_rate
        if overtime_bill_rate is not None:
            self.payroll.overtime_bill_rate = overtime_bill_rate

    # API-compatible methods for Insightful integration
    def get_project_details(self) -> Dict[str, Any]:
        """Get detailed project information for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "archived": self.archived,
            "billable": self.billable,
            "statuses": self.statuses.copy(),
            "priorities": self.priorities.copy(),
            "payroll": self.payroll.to_dict(),
            "employees": self.employees.copy(),
            "teams": self.teams.copy(),
            "creatorId": self.creator_id,
            "organizationId": self.organization_id,
            "createdAt": self.created_at,
            "employeeCount": self.employee_count,
            "teamCount": self.team_count,
            "isActive": self.is_active
        }

    def update_from_api(self, data: Dict[str, Any]) -> None:
        """Update project from API response data."""
        if "name" in data:
            self.name = data["name"]
        if "archived" in data:
            self.archived = data["archived"]
        if "billable" in data:
            self.billable = data["billable"]
        if "statuses" in data:
            self.statuses = data["statuses"]
        if "priorities" in data:
            self.priorities = data["priorities"]
        if "payroll" in data:
            self.payroll = Payroll.from_dict(data["payroll"])
        if "employees" in data:
            self.employees = data["employees"]
        if "teams" in data:
            self.teams = data["teams"]

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """
        Create a Project instance from a dictionary.
        
        Args:
            data: Dictionary containing project data
            
        Returns:
            Project instance
        """
        # Handle payroll data
        payroll_data = data.get("payroll", {})
        payroll = Payroll.from_dict(payroll_data) if payroll_data else Payroll()
        
        # Map camelCase keys to snake_case
        mapped_data = {
            "id": data.get("id"),
            "name": data.get("name"),
            "archived": data.get("archived", False),
            "statuses": data.get("statuses", ["To do", "On hold", "In progress", "Done"]),
            "priorities": data.get("priorities", ["low", "medium", "high"]),
            "billable": data.get("billable", True),
            "payroll": payroll,
            "employees": data.get("employees", []),
            "creator_id": data.get("creatorId"),
            "organization_id": data.get("organizationId"),
            "teams": data.get("teams", []),
            "created_at": data.get("createdAt"),
        }
        
        # Remove None values for required fields
        if mapped_data["id"] is None or mapped_data["name"] is None:
            raise ValueError("Project ID and name are required")
        
        return cls(**{k: v for k, v in mapped_data.items() if v is not None})

    def to_dict(self) -> dict:
        """
        Convert Project instance to dictionary with camelCase keys.
        
        Returns:
            Dictionary representation of the project
        """
        return {
            "id": self.id,
            "name": self.name,
            "archived": self.archived,
            "statuses": self.statuses,
            "priorities": self.priorities,
            "billable": self.billable,
            "payroll": self.payroll.to_dict(),
            "employees": self.employees,
            "creatorId": self.creator_id,
            "organizationId": self.organization_id,
            "teams": self.teams,
            "createdAt": self.created_at,
        }

    def __str__(self) -> str:
        """String representation of the project."""
        status = "archived" if self.archived else "active"
        return f"Project(id={self.id}, name='{self.name}', status={status})"

    def __repr__(self) -> str:
        """Detailed string representation of the project."""
        return (f"Project(id='{self.id}', name='{self.name}', "
                f"archived={self.archived}, billable={self.billable}, "
                f"employees={len(self.employees)}, teams={len(self.teams)})")
