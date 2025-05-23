"""Employee model schema for the application."""

from dataclasses import dataclass, field
from typing import List, Optional, Literal
from datetime import datetime


@dataclass
class Employee:
    """
    Employee model representing a user in the organization.
    
    Attributes:
        id: Unique identifier for the employee
        name: Full name of the employee
        email: Email address of the employee
        team_id: ID of the team the employee belongs to
        shared_settings_id: ID for shared settings configuration
        account_id: Account identifier
        identifier: Unique identifier (typically email)
        type: Type of employee account (personal, etc.)
        organization_id: ID of the organization
        projects: List of project IDs the employee is assigned to
        deactivated: Flag indicating if employee is deactivated (0=active, 1=deactivated)
        invited: Timestamp when the employee was invited (Unix timestamp in milliseconds)
        created_at: Timestamp when the employee record was created (Unix timestamp in milliseconds)
    """
    
    id: str
    name: str
    email: str
    team_id: str
    shared_settings_id: str
    account_id: str
    identifier: str
    type: Literal["personal", "business"] = "personal"
    organization_id: str = ""
    projects: List[str] = field(default_factory=list)
    deactivated: int = 0
    invited: Optional[int] = None
    created_at: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate employee data after initialization."""
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")
        
        if self.deactivated not in (0, 1):
            raise ValueError("Deactivated must be 0 (active) or 1 (deactivated)")
        
        # Set identifier to email if not provided
        if not self.identifier:
            self.identifier = self.email

    @property
    def is_active(self) -> bool:
        """Check if the employee is active (not deactivated)."""
        return self.deactivated == 0

    @property
    def invited_datetime(self) -> Optional[datetime]:
        """Convert invited timestamp to datetime object."""
        if self.invited:
            return datetime.fromtimestamp(self.invited / 1000)
        return None

    @property
    def created_datetime(self) -> Optional[datetime]:
        """Convert created_at timestamp to datetime object."""
        if self.created_at:
            return datetime.fromtimestamp(self.created_at / 1000)
        return None

    def add_project(self, project_id: str) -> None:
        """Add a project to the employee's project list."""
        if project_id not in self.projects:
            self.projects.append(project_id)

    def remove_project(self, project_id: str) -> None:
        """Remove a project from the employee's project list."""
        if project_id in self.projects:
            self.projects.remove(project_id)

    def deactivate(self) -> None:
        """Deactivate the employee."""
        self.deactivated = 1

    def activate(self) -> None:
        """Activate the employee."""
        self.deactivated = 0

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        """
        Create an Employee instance from a dictionary.
        
        Args:
            data: Dictionary containing employee data
            
        Returns:
            Employee instance
        """
        # Map camelCase keys to snake_case
        mapped_data = {
            "id": data.get("id"),
            "name": data.get("name"),
            "email": data.get("email"),
            "team_id": data.get("teamId"),
            "shared_settings_id": data.get("sharedSettingsId"),
            "account_id": data.get("accountId"),
            "identifier": data.get("identifier"),
            "type": data.get("type", "personal"),
            "organization_id": data.get("organizationId", ""),
            "projects": data.get("projects", []),
            "deactivated": data.get("deactivated", 0),
            "invited": data.get("invited"),
            "created_at": data.get("createdAt"),
        }
        
        # Remove None values
        mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
        
        return cls(**mapped_data)

    def to_dict(self) -> dict:
        """
        Convert Employee instance to dictionary with camelCase keys.
        
        Returns:
            Dictionary representation of the employee
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "teamId": self.team_id,
            "sharedSettingsId": self.shared_settings_id,
            "accountId": self.account_id,
            "identifier": self.identifier,
            "type": self.type,
            "organizationId": self.organization_id,
            "projects": self.projects,
            "deactivated": self.deactivated,
            "invited": self.invited,
            "createdAt": self.created_at,
        }
